import pandas as pd
import networkx as nx
import numpy as np

class BusStopImportance:
    def __init__(self):
        self.stops_df = pd.read_csv('2025_Problem_D_Data/Bus_Stops.csv')
        self.routes_df = pd.read_csv('2025_Problem_D_Data/Bus_Routes.csv')
        self.G = self._create_network()

    def _create_network(self):
        """Create network of bus stops"""
        G = nx.Graph()
        
        # Add nodes (stops)
        for _, stop in self.stops_df.iterrows():
            G.add_node(stop['stop_name'],
                      ridership=stop['Rider_Tota'],
                      routes=str(stop['Routes_Ser']).split(','),
                      pos=(stop['y'], stop['x']))
            
        # Add edges between stops on same route
        for _, stop1 in self.stops_df.iterrows():
            for _, stop2 in self.stops_df.iterrows():
                routes1 = set(str(stop1['Routes_Ser']).split(','))
                routes2 = set(str(stop2['Routes_Ser']).split(','))
                if routes1.intersection(routes2):
                    G.add_edge(stop1['stop_name'], stop2['stop_name'])
                    
        return G

    def calculate_stop_importance(self):
        """Calculate importance score for each stop"""
        importance = {}
        
        # Calculate network centrality metrics
        degree_cent = nx.degree_centrality(self.G)
        between_cent = nx.betweenness_centrality(self.G)
        
        for node in self.G.nodes():
            # Get stop data
            stop_data = self.G.nodes[node]
            
            # Components of importance score:
            ridership = stop_data['ridership'] / self.stops_df['Rider_Tota'].max()
            num_routes = len(stop_data['routes'])
            degree = degree_cent[node] 
            betweenness = between_cent[node]
            
            # Combined score (weighted sum)
            score = (0.4 * ridership + 
                    0.3 * num_routes/10 +
                    0.15 * degree +
                    0.15 * betweenness)
            
            importance[node] = score
            
        return importance

def main():
    analyzer = BusStopImportance()
    scores = analyzer.calculate_stop_importance()
    
    # Sort stops by importance
    sorted_stops = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    
    print("\nTop 20 Most Important Bus Stops:")
    print("-"*50)
    for stop, score in sorted_stops[:20]:
        print(f"Stop: {stop}")
        print(f"Importance Score: {score:.4f}\n")

if __name__ == "__main__":
    main()