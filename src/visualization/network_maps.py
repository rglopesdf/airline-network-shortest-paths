import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np

def plot_airline_network_map(airports_df, routes_df, title="Airline Network Map"):
    """
    Create geographic visualization of airline network
    
    Args:
        airports_df: DataFrame with airport coordinates
        routes_df: DataFrame with route information
        title: Title for the plot
    """
    fig, ax = plt.subplots(figsize=(16, 12))
    
    # Plot airports
    ax.scatter(airports_df['longitude'], airports_df['latitude'], 
               c='blue', s=30, alpha=0.7, zorder=3)
    
    # Plot sample routes (to avoid overcrowding)
    sample_routes = routes_df.sample(min(50, len(routes_df)), random_state=42)
    
    for _, route in sample_routes.iterrows():
        origem_data = airports_df[airports_df['code'] == route['origem']].iloc[0]
        destino_data = airports_df[airports_df['code'] == route['destino']].iloc[0]
        
        ax.plot([origem_data['longitude'], destino_data['longitude']], 
                [origem_data['latitude'], destino_data['latitude']], 
                'gray', alpha=0.3, linewidth=0.5, zorder=1)
    
    # Highlight major hubs
    major_hubs = ['GRU', 'BSB', 'VCP', 'CNF', 'FOR', 'POA']
    hub_data = airports_df[airports_df['code'].isin(major_hubs)]
    
    ax.scatter(hub_data['longitude'], hub_data['latitude'], 
               c='red', s=100, marker='*', edgecolors='black', 
               linewidth=1, label='Major Hubs', zorder=4)
    
    # Add hub labels
    for _, airport in hub_data.iterrows():
        ax.annotate(airport['code'], 
                    (airport['longitude'], airport['latitude']),
                    xytext=(5, 5), textcoords='offset points',
                    fontsize=10, fontweight='bold')
    
    ax.set_xlabel('Longitude', fontsize=12)
    ax.set_ylabel('Latitude', fontsize=12)
    ax.set_title(title, fontsize=16, fontweight='bold')
    ax.grid(True, alpha=0.3)
    ax.legend()
    
    return fig, ax

def plot_network_statistics(network_stats, opportunities_df):
    """
    Create statistical visualizations of network analysis
    """
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(16, 12))
    
    # Plot 1: Network composition
    labels = ['Gol Only', 'Azul Only', 'Both Airlines']
    sizes = [network_stats['gol_only'], network_stats['azul_only'], network_stats['both']]
    colors = ['red', 'blue', 'purple']
    
    ax1.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', startangle=90)
    ax1.set_title('Airport Distribution by Operator', fontweight='bold')
    
    # Plot 2: Codeshare opportunities by type
    if len(opportunities_df) > 0:
        type_counts = opportunities_df['tipo'].value_counts()
        ax2.bar(type_counts.index, type_counts.values, color=['skyblue', 'lightcoral'])
        ax2.set_title('Codeshare Opportunities by Type', fontweight='bold')
        ax2.set_ylabel('Number of Opportunities')
    
    # Plot 3: Distance distribution
    if len(opportunities_df) > 0:
        ax3.hist(opportunities_df['distancia'], bins=20, color='gold', alpha=0.7, edgecolor='black')
        ax3.set_title('Distribution of Route Distances', fontweight='bold')
        ax3.set_xlabel('Distance (km)')
        ax3.set_ylabel('Frequency')
        ax3.axvline(opportunities_df['distancia'].mean(), color='red', linestyle='--', 
                   label=f'Mean: {opportunities_df["distancia"].mean():.0f} km')
        ax3.legend()
    
    # Plot 4: Top routes by efficiency
    if len(opportunities_df) > 0:
        top_routes = opportunities_df.nsmallest(10, 'distancia')
        route_labels = [f"{row['origem']}→{row['destino']}" for _, row in top_routes.iterrows()]
        
        ax4.barh(range(len(top_routes)), top_routes['distancia'], color='lightgreen')
        ax4.set_yticks(range(len(top_routes)))
        ax4.set_yticklabels(route_labels)
        ax4.set_xlabel('Distance (km)')
        ax4.set_title('Top 10 Most Efficient Routes', fontweight='bold')
        ax4.invert_yaxis()
    
    plt.tight_layout()
    return fig

def create_interactive_network_visualization(G, output_file='network.html'):
    """
    Create interactive network visualization using pyvis
    """
    try:
        from pyvis.network import Network
        
        net = Network(height="600px", width="100%", bgcolor="#222222", font_color="white")
        
        # Add nodes
        for node, data in G.nodes(data=True):
            operator = data.get('operator', 'Unknown')
            color = {'Gol': 'red', 'Azul': 'blue', 'Both': 'purple'}.get(operator, 'gray')
            
            net.add_node(node, 
                        label=node,
                        color=color,
                        title=f"{data.get('name', node)}<br>{data.get('city', '')}<br>Operator: {operator}")
        
        # Add edges (sample to avoid overcrowding)
        edges_sample = list(G.edges(data=True))[:200]  # Limit to 200 edges
        
        for u, v, data in edges_sample:
            airlines = data.get('airlines_str', '')
            color = 'purple' if ',' in airlines else 'red' if 'Gol' in airlines else 'blue'
            
            net.add_edge(u, v, 
                        color=color,
                        title=f"Distance: {data.get('distance_km', 0):.0f} km<br>Airlines: {airlines}")
        
        net.save_graph(output_file)
        return output_file
        
    except ImportError:
        print("pyvis not available. Install with: pip install pyvis")
        return None

