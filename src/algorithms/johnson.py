import pandas as pd
import networkx as nx
import numpy as np
from math import radians, cos, sin, asin, sqrt

def haversine(lon1, lat1, lon2, lat2):
    """
    Calculate the great circle distance between two points 
    on the earth (specified in decimal degrees)
    Returns distance in kilometers
    """
    # Convert decimal degrees to radians
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
    
    # Haversine formula
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a))
    r = 6371  # Radius of earth in kilometers
    return c * r

def johnson_algorithm(G):
    """
    Implementation of Johnson's algorithm for all-pairs shortest paths
    
    Args:
        G: NetworkX directed graph with 'weight' edge attribute
        
    Returns:
        tuple: (distances, paths) dictionaries
    """
    # Create auxiliary graph with additional vertex q
    G_aux = G.copy()
    G_aux.add_node('q')
    for node in G.nodes():
        G_aux.add_edge('q', node, weight=0)

    try:
        # Run Bellman-Ford from auxiliary vertex
        h = nx.single_source_bellman_ford_path_length(G_aux, 'q', weight='weight')
    except nx.NetworkXUnbounded:
        raise Exception("Graph contains negative cycle!")

    # Reweight edges
    G_reweighted = nx.DiGraph()
    for u, v, data in G.edges(data=True):
        w = data['weight']
        w_prime = w + h[u] - h[v]
        G_reweighted.add_edge(u, v, weight=w_prime)

    # Run Dijkstra from each vertex
    distances = dict()
    paths = dict()
    for node in G_reweighted.nodes():
        d, p = nx.single_source_dijkstra(G_reweighted, node, weight='weight')
        distances[node] = d
        paths[node] = p

    # Correct distances back to original graph
    for u in distances:
        for v in distances[u]:
            distances[u][v] = distances[u][v] + h[v] - h[u]

    return distances, paths

def build_airline_network(airports_df, routes_df):
    """
    Build airline network graph from airports and routes data
    
    Args:
        airports_df: DataFrame with airport information
        routes_df: DataFrame with route information
        
    Returns:
        NetworkX DiGraph
    """
    G = nx.DiGraph()
    
    # Add airport nodes
    for _, airport in airports_df.iterrows():
        G.add_node(airport['code'], 
                   name=airport['name'],
                   city=airport['city'],
                   country=airport['country'],
                   latitude=airport['latitude'],
                   longitude=airport['longitude'])
    
    # Add route edges
    for _, route in routes_df.iterrows():
        if route['origem'] in G.nodes() and route['destino'] in G.nodes():
            G.add_edge(route['origem'], route['destino'],
                      weight=route['distancia_km'],
                      distance=route['distancia_km'],
                      airlines=route['companhias'])
    
    return G

def calculate_network_metrics(G):
    """
    Calculate various network metrics
    
    Args:
        G: NetworkX graph
        
    Returns:
        dict: Network metrics
    """
    metrics = {
        'num_nodes': len(G.nodes()),
        'num_edges': len(G.edges()),
        'density': nx.density(G),
        'is_connected': nx.is_weakly_connected(G),
        'avg_degree': sum(dict(G.degree()).values()) / len(G.nodes())
    }
    
    # Calculate centrality measures
    degree_centrality = nx.degree_centrality(G)
    betweenness_centrality = nx.betweenness_centrality(G)
    closeness_centrality = nx.closeness_centrality(G)
    
    metrics['centrality'] = {
        'degree': degree_centrality,
        'betweenness': betweenness_centrality,
        'closeness': closeness_centrality
    }
    
    return metrics

