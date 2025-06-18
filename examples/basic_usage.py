"""
Basic usage examples for the airline network analysis toolkit
"""

import pandas as pd
import networkx as nx
from src.algorithms.johnson import johnson_algorithm, calculate_network_metrics
from src.analysis.codeshare_detector import find_codeshare_opportunities
from src.visualization.network_maps import plot_airline_network_map

def basic_network_analysis():
    """
    Example of basic network analysis workflow
    """
    print("Loading airline network data...")
    
    # Load the combined network
    G = nx.read_graphml('data/processed/combined_network.graphml')
    airports_df = pd.read_csv('data/processed/combined_airports_coordinates.csv')
    
    print(f"Network loaded: {len(G.nodes())} airports, {len(G.edges())} routes")
    
    # Calculate network metrics
    metrics = calculate_network_metrics(G)
    print(f"Network density: {metrics['density']:.4f}")
    print(f"Average degree: {metrics['avg_degree']:.2f}")
    print(f"Is connected: {metrics['is_connected']}")
    
    # Run Johnson's algorithm
    print("Running Johnson's algorithm...")
    distances, paths = johnson_algorithm(G)
    print("✓ Johnson's algorithm completed successfully")
    
    return G, distances, paths, airports_df

def find_shortest_path_example():
    """
    Example of finding shortest path between specific airports
    """
    G, distances, paths, airports_df = basic_network_analysis()
    
    # Example: Find path from São Paulo (GRU) to Miami (MIA)
    origin = 'GRU'
    destination = 'MIA'
    
    if origin in distances and destination in distances[origin]:
        distance = distances[origin][destination]
        path = paths[origin][destination]
        
        print(f"\nShortest path from {origin} to {destination}:")
        print(f"Distance: {distance:.0f} km")
        print(f"Path: {' → '.join(path)}")
        print(f"Number of stops: {len(path) - 2}")
    else:
        print(f"No path found from {origin} to {destination}")

def codeshare_analysis_example():
    """
    Example of codeshare opportunity analysis
    """
    G, distances, paths, airports_df = basic_network_analysis()
    
    # Load airline codes
    gol_codes = set(pd.read_csv('data/processed/gol_airports_coordinates.csv')['code'])
    azul_codes = set(pd.read_csv('data/processed/azul_airports_coordinates.csv')['code'])
    
    print("Searching for codeshare opportunities...")
    
    # Find opportunities (using smaller sample for demo)
    gol_sample = list(gol_codes - azul_codes)[:5]  # 5 Gol-exclusive airports
    azul_sample = list(azul_codes - gol_codes)[:10]  # 10 Azul-exclusive airports
    
    opportunities = []
    for gol_airport in gol_sample:
        for azul_airport in azul_sample:
            # Check both directions
            for orig, dest in [(gol_airport, azul_airport), (azul_airport, gol_airport)]:
                if orig in paths and dest in paths[orig]:
                    path = paths[orig][dest]
                    distance = distances[orig][dest]
                    
                    if len(path) > 2 and distance < 10000:  # Multi-hop routes under 10,000 km
                        opportunities.append({
                            'origin': orig,
                            'destination': dest,
                            'distance': distance,
                            'stops': len(path) - 2,
                            'path': ' → '.join(path)
                        })
    
    # Sort by distance and show top 10
    opportunities.sort(key=lambda x: x['distance'])
    
    print(f"\nTop 10 codeshare opportunities found:")
    for i, opp in enumerate(opportunities[:10], 1):
        print(f"{i:2d}. {opp['origin']} → {opp['destination']}: {opp['distance']:.0f} km, {opp['stops']} stops")
        print(f"    Path: {opp['path']}")

if __name__ == "__main__":
    print("=== Airline Network Analysis Examples ===\n")
    
    print("1. Basic Network Analysis")
    basic_network_analysis()
    
    print("\n2. Shortest Path Example")
    find_shortest_path_example()
    
    print("\n3. Codeshare Analysis Example")
    codeshare_analysis_example()
    
    print("\n=== Examples completed ===")

