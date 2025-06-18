import pandas as pd
import networkx as nx
from collections import defaultdict

def find_codeshare_opportunities(graph, distances, paths, airports_df, 
                                gol_codes, azul_codes, min_distance=1000, max_stops=3):
    """
    Identify codeshare opportunities where optimal path uses both airlines
    
    Args:
        graph: NetworkX graph
        distances: Distance matrix from Johnson's algorithm
        paths: Path matrix from Johnson's algorithm
        airports_df: DataFrame with airport information
        gol_codes: Set of Gol airport codes
        azul_codes: Set of Azul airport codes
        min_distance: Minimum route distance to consider
        max_stops: Maximum number of stops allowed
        
    Returns:
        List of codeshare opportunities
    """
    opportunities = []
    both_codes = gol_codes.intersection(azul_codes)
    gol_only = gol_codes - both_codes
    azul_only = azul_codes - both_codes
    
    # Check routes between exclusive airports
    for gol_airport in gol_only:
        for azul_airport in azul_only:
            # Check both directions
            for origin, destination in [(gol_airport, azul_airport), (azul_airport, gol_airport)]:
                opportunity = analyze_route_codeshare(
                    origin, destination, paths, graph, airports_df, 
                    gol_codes, azul_codes, min_distance, max_stops
                )
                
                if opportunity:
                    opportunities.append(opportunity)
    
    return opportunities

def analyze_route_codeshare(origin, destination, paths, graph, airports_df, 
                           gol_codes, azul_codes, min_distance, max_stops):
    """
    Analyze a specific route for codeshare potential
    """
    if origin not in paths or destination not in paths[origin]:
        return None
    
    path = paths[origin][destination]
    if len(path) < 2 or len(path) - 2 > max_stops:
        return None
    
    # Analyze each segment
    segments = []
    uses_gol = False
    uses_azul = False
    total_distance = 0
    
    for i in range(len(path) - 1):
        seg_origin = path[i]
        seg_destination = path[i + 1]
        
        if graph.has_edge(seg_origin, seg_destination):
            edge_data = graph[seg_origin][seg_destination]
            airlines_str = edge_data.get('airlines_str', '')
            
            if 'Gol' in airlines_str:
                uses_gol = True
            if 'Azul' in airlines_str:
                uses_azul = True
            
            segment_distance = edge_data.get('distance_km', 0)
            total_distance += segment_distance
            
            segments.append({
                'origin': seg_origin,
                'destination': seg_destination,
                'distance': segment_distance,
                'airlines': airlines_str
            })
    
    # Check if it's a real codeshare opportunity
    is_codeshare = uses_gol and uses_azul and len(path) > 2 and total_distance >= min_distance
    
    if is_codeshare:
        # Determine direction type
        if origin in gol_codes and destination in azul_codes:
            route_type = 'Gol→Azul'
        elif origin in azul_codes and destination in gol_codes:
            route_type = 'Azul→Gol'
        else:
            route_type = 'Mixed'
        
        return {
            'origin': origin,
            'destination': destination,
            'type': route_type,
            'distance': total_distance,
            'stops': len(path) - 2,
            'path': ' → '.join(path),
            'segments': segments,
            'uses_gol': uses_gol,
            'uses_azul': uses_azul
        }
    
    return None

def analyze_hub_importance(graph, distances):
    """
    Analyze hub importance based on various centrality metrics
    """
    # Calculate centrality measures
    degree_centrality = nx.degree_centrality(graph)
    betweenness_centrality = nx.betweenness_centrality(graph)
    closeness_centrality = nx.closeness_centrality(graph)
    
    # Calculate average distance from each airport
    avg_distances = {}
    for airport in distances:
        valid_distances = [d for d in distances[airport].values() 
                          if d != float('inf') and d > 0]
        if valid_distances:
            avg_distances[airport] = sum(valid_distances) / len(valid_distances)
        else:
            avg_distances[airport] = float('inf')
    
    # Combine metrics into DataFrame
    hub_data = []
    for airport in graph.nodes():
        airport_data = graph.nodes[airport]
        hub_data.append({
            'airport_code': airport,
            'name': airport_data.get('name', ''),
            'city': airport_data.get('city', ''),
            'country': airport_data.get('country', ''),
            'operator': airport_data.get('operator', ''),
            'degree': graph.degree(airport),
            'degree_centrality': degree_centrality.get(airport, 0),
            'betweenness_centrality': betweenness_centrality.get(airport, 0),
            'closeness_centrality': closeness_centrality.get(airport, 0),
            'avg_distance': avg_distances.get(airport, float('inf'))
        })
    
    return pd.DataFrame(hub_data)

def identify_connection_hubs(opportunities_df):
    """
    Identify which airports serve as connection hubs in codeshare routes
    """
    hub_connections = defaultdict(int)
    
    for _, opportunity in opportunities_df.iterrows():
        path_airports = opportunity['path'].split(' → ')
        # Count intermediate airports (excluding origin and destination)
        for hub in path_airports[1:-1]:
            hub_connections[hub] += 1
    
    return dict(hub_connections)

def calculate_route_efficiency(opportunities_df, direct_distances=None):
    """
    Calculate efficiency metrics for codeshare routes
    """
    if direct_distances is None:
        return opportunities_df
    
    efficiency_data = []
    
    for _, opportunity in opportunities_df.iterrows():
        origin = opportunity['origin']
        destination = opportunity['destination']
        codeshare_distance = opportunity['distance']
        
        # Get direct distance if available
        direct_distance = direct_distances.get(origin, {}).get(destination, None)
        
        if direct_distance and direct_distance != float('inf'):
            efficiency = direct_distance / codeshare_distance
            detour_factor = codeshare_distance / direct_distance
        else:
            efficiency = None
            detour_factor = None
        
        efficiency_data.append({
            'origin': origin,
            'destination': destination,
            'codeshare_distance': codeshare_distance,
            'direct_distance': direct_distance,
            'efficiency': efficiency,
            'detour_factor': detour_factor
        })
    
    return pd.DataFrame(efficiency_data)

