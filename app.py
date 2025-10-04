"""
app.py
Purpose: Main Streamlit application for the Traffic Congestion Predictor.
Provides UI for route selection, prediction, and visualization.
"""

import streamlit as st
import matplotlib.pyplot as plt
import networkx as nx
from data_loader import get_road_network, get_locations, get_edge_list, update_traffic_weight
from utils import dijkstra_shortest_path, get_path_edges, format_path_display


# Page configuration
st.set_page_config(
    page_title="Traffic Congestion Predictor",
    page_icon="🚦",
    layout="wide"
)


def initialize_session_state():
    """Initialize session state variables for the app."""
    if 'road_network' not in st.session_state:
        st.session_state.road_network = get_road_network()
    if 'show_traffic_editor' not in st.session_state:
        st.session_state.show_traffic_editor = False


def create_network_graph(road_network, highlight_path=None):
    """
    Creates a NetworkX graph from the road network and visualizes it.
    
    Args:
        road_network: Dictionary representing the road network
        highlight_path: List of edges to highlight (shortest path)
    """
    # Create a new graph
    G = nx.Graph()
    
    # Add all edges with weights
    for source, neighbors in road_network.items():
        for destination, weight in neighbors.items():
            G.add_edge(source, destination, weight=weight)
    
    # Set up the plot
    fig, ax = plt.subplots(figsize=(14, 10))
    
    # Use spring layout for better visualization
    pos = nx.spring_layout(G, k=2, iterations=50, seed=42)
    
    # Draw all nodes
    nx.draw_networkx_nodes(
        G, pos, 
        node_color='lightblue', 
        node_size=2000,
        alpha=0.9,
        ax=ax
    )
    
    # Draw all edges in gray
    nx.draw_networkx_edges(
        G, pos,
        edge_color='gray',
        width=2,
        alpha=0.5,
        ax=ax
    )
    
    # Highlight the shortest path if provided
    if highlight_path:
        nx.draw_networkx_edges(
            G, pos,
            edgelist=highlight_path,
            edge_color='red',
            width=4,
            alpha=0.8,
            ax=ax
        )
    
    # Draw node labels
    nx.draw_networkx_labels(
        G, pos,
        font_size=9,
        font_weight='bold',
        font_color='darkblue',
        ax=ax
    )
    
    # Draw edge labels (weights)
    edge_labels = nx.get_edge_attributes(G, 'weight')
    nx.draw_networkx_edge_labels(
        G, pos,
        edge_labels,
        font_size=8,
        font_color='green',
        ax=ax
    )
    
    ax.set_title("Road Network Graph (Weights = Travel Time in Minutes)", 
                 fontsize=14, fontweight='bold', pad=20)
    ax.axis('off')
    plt.tight_layout()
    
    return fig


def main():
    """Main application function."""
    
    # Initialize session state
    initialize_session_state()
    
    # Header
    st.title("🚦 Traffic Congestion Predictor")
    st.markdown("""
    Welcome to the *Traffic Congestion Predictor*! This app helps you find the fastest route 
    between locations considering current traffic conditions. Select your source and destination 
    to get started.
    """)
    
    st.divider()
    
    # Main content area
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.subheader("📍 Route Selection")
        
        # Get locations for dropdowns
        locations = get_locations()
        
        # Source and destination selection
        source = st.selectbox(
            "Select Source Location:",
            options=locations,
            index=0,
            key="source"
        )
        
        destination = st.selectbox(
            "Select Destination Location:",
            options=locations,
            index=min(5, len(locations)-1),
            key="destination"
        )
        
        # Predict button
        predict_button = st.button("🚀 Predict Fastest Route", type="primary", use_container_width=True)
        
        st.divider()
        
        # Results section
        if predict_button:
            if source == destination:
                st.warning("⚠ Source and destination cannot be the same!")
            else:
                with st.spinner("Calculating optimal route..."):
                    # Calculate shortest path
                    path, total_weight = dijkstra_shortest_path(
                        st.session_state.road_network,
                        source,
                        destination
                    )
                    
                    # Store results in session state
                    st.session_state.current_path = path
                    st.session_state.current_weight = total_weight
                    st.session_state.path_edges = get_path_edges(path) if path else None
        
        # Display results if available
        if 'current_path' in st.session_state:
            st.subheader("📊 Route Results")
            
            result_text = format_path_display(
                st.session_state.current_path,
                st.session_state.current_weight
            )
            
            if st.session_state.current_path:
                st.success(result_text)
                
                # Additional stats
                st.metric("Number of Stops", len(st.session_state.current_path) - 1)
                st.metric("Total Travel Time", f"{st.session_state.current_weight:.1f} min")
            else:
                st.error(result_text)
        
        st.divider()
        
        # Traffic simulation toggle
        st.subheader("🔧 Advanced Options")
        if st.button("Toggle Traffic Editor", use_container_width=True):
            st.session_state.show_traffic_editor = not st.session_state.show_traffic_editor
    
    with col2:
        st.subheader("🗺 Network Visualization")
        
        # Visualize the graph
        highlight_edges = st.session_state.get('path_edges', None)
        fig = create_network_graph(st.session_state.road_network, highlight_edges)
        st.pyplot(fig)
        plt.close()
        
        # Legend
        st.markdown("""
        *Legend:*
        - 🔵 Blue circles = Locations
        - Gray lines = Available roads
        - 🔴 *Red lines = Fastest route*
        - Green numbers = Travel time (minutes)
        """)
    
    # Traffic editor section (expandable)
    if st.session_state.show_traffic_editor:
        st.divider()
        st.subheader("🚧 Traffic Simulation Editor")
        st.info("Modify traffic conditions by updating edge weights. Higher values = more congestion.")
        
        # Get all edges
        edges = get_edge_list()
        
        # Create columns for edge editing
        cols = st.columns(3)
        
        for idx, (src, dst, weight) in enumerate(edges):
            with cols[idx % 3]:
                new_weight = st.number_input(
                    f"{src} ↔ {dst}",
                    min_value=1,
                    max_value=100,
                    value=int(weight),
                    step=1,
                    key=f"edge_{src}_{dst}"
                )
                
                # Update if changed
                if new_weight != weight:
                    st.session_state.road_network = update_traffic_weight(
                        st.session_state.road_network,
                        src, dst, new_weight
                    )
        
        if st.button("🔄 Reset to Default Traffic", use_container_width=True):
            st.session_state.road_network = get_road_network()
            st.success("Traffic conditions reset to default!")
            st.rerun()
    
    # Footer
    st.divider()
    st.markdown("""
    <div style='text-align: center; color: gray; padding: 20px;'>
        <p>🚦 Traffic Congestion Predictor | Powered by Dijkstra's Algorithm</p>
        <p style='font-size: 12px;'>This app uses graph theory to find optimal routes considering traffic conditions.</p>
    </div>
    """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()