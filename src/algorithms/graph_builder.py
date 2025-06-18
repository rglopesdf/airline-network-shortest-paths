import pandas as pd
import networkx as nx
from math import radians, cos, sin, asin, sqrt

def haversine_distance(lat1, lon1, lat2, lon2):
    """
    Calculate the great circle distance between two points 
    on the earth (specified in decimal degrees)
    """
    # Convert decimal degrees to radians
    lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])
    
    # Haversine formula
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a))
    r = 6371  # Radius of earth in kilometers
    return c * r

def build_combined_network(gol_airports, azul_airports, combined_airports):
    """
    Build combined airline network with both Gol and Azul routes
    
    Args:
        gol_airports: DataFrame with Gol airport data
        azul_airports: DataFrame with Azul airport data  
        combined_airports: DataFrame with combined airport data
        
    Returns:
        NetworkX DiGraph
    """
    G = nx.DiGraph()
    
    # Get airport codes for each airline
    gol_codes = set(gol_airports['code'])
    azul_codes = set(azul_airports['code'])
    both_codes = gol_codes.intersection(azul_codes)
    
    # Add nodes with operator information
    for _, airport in combined_airports.iterrows():
        operates_gol = airport['code'] in gol_codes
        operates_azul = airport['code'] in azul_codes
        
        if operates_gol and operates_azul:
            operator = 'Both'
        elif operates_gol:
            operator = 'Gol'
        else:
            operator = 'Azul'
        
        G.add_node(airport['code'], 
                   name=airport['name'],
                   city=airport['city'],
                   country=airport['country'],
                   latitude=airport['latitude'],
                   longitude=airport['longitude'],
                   operator=operator)
    
    return G

def add_airline_routes(G, airports_df, airline_codes, airline_name, hubs):
    """
    Add routes for a specific airline to the graph
    
    Args:
        G: NetworkX graph
        airports_df: DataFrame with airport coordinates
        airline_codes: Set of airport codes for this airline
        airline_name: Name of the airline
        hubs: List of hub airports for this airline
    """
    # Connect hubs to each other
    for i, hub1 in enumerate(hubs):
        for hub2 in hubs[i+1:]:
            if hub1 in airline_codes and hub2 in airline_codes:
                add_bidirectional_route(G, hub1, hub2, airports_df, airline_name)
    
    # Connect non-hub airports to nearest hub
    for airport in airline_codes:
        if airport not in hubs:
            nearest_hub = find_nearest_hub(airport, hubs, airports_df)
            if nearest_hub:
                add_bidirectional_route(G, airport, nearest_hub, airports_df, airline_name)

def add_bidirectional_route(G, airport1, airport2, airports_df, airline):
    """
    Add bidirectional route between two airports
    """
    if airport1 in airports_df['code'].values and airport2 in airports_df['code'].values:
        coord1 = airports_df[airports_df['code'] == airport1].iloc[0]
        coord2 = airports_df[airports_df['code'] == airport2].iloc[0]
        
        distance = haversine_distance(coord1['latitude'], coord1['longitude'],
                                    coord2['latitude'], coord2['longitude'])
        
        # Check if edge already exists
        if G.has_edge(airport1, airport2):
            existing_airlines = G[airport1][airport2].get('airlines_str', '')
            if airline not in existing_airlines:
                new_airlines = existing_airlines + ',' + airline if existing_airlines else airline
                G[airport1][airport2]['airlines_str'] = new_airlines
                G[airport2][airport1]['airlines_str'] = new_airlines
        else:
            G.add_edge(airport1, airport2, weight=distance, distance_km=distance, airlines_str=airline)
            G.add_edge(airport2, airport1, weight=distance, distance_km=distance, airlines_str=airline)

def find_nearest_hub(airport, hubs, airports_df):
    """
    Find the nearest hub to a given airport
    """
    if airport not in airports_df['code'].values:
        return None
        
    airport_coord = airports_df[airports_df['code'] == airport].iloc[0]
    min_distance = float('inf')
    nearest_hub = None
    
    for hub in hubs:
        if hub in airports_df['code'].values:
            hub_coord = airports_df[airports_df['code'] == hub].iloc[0]
            distance = haversine_distance(airport_coord['latitude'], airport_coord['longitude'],
                                        hub_coord['latitude'], hub_coord['longitude'])
            
            if distance < min_distance:
                min_distance = distance
                nearest_hub = hub
    
    return nearest_hub

