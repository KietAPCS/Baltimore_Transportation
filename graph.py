import networkx as nx
import csv
import json
from tqdm import tqdm
import numpy as np
import matplotlib.pyplot as plt
import pickle

class Graph:
    def __init__(self, nodes_file, edges_file, buses_file, cached=""):
        """Initialize an empty graph."""
        self.graph = nx.DiGraph()
        self.buses = {}
        
        if cached:
            self.load_graph(cached)
        else:
            self.load_nodes(nodes_file)
            self.load_edges(edges_file)
            self.load_buses(buses_file)

    def load_nodes(self, nodes_file):
        """Load nodes from a CSV file."""
        with open(nodes_file, 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                node_id = row['osmid']
                self.graph.add_node(node_id, **row)
                
    def load_buses(self, buses_file):
        """Load buses from a CSV file."""
        with open(buses_file, 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                stop_id = row['stop_id']
                # Correct the key from 'ï»¿y' to 'y'
                if 'ï»¿y' in row:
                    row['y'] = row.pop('ï»¿y')
                self.buses[stop_id] = row

    def load_edges(self, edges_file):
        """Load edges from a CSV file."""
        with open(edges_file, 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                source = row['u']
                target = row['v']
                
                # if source == str(49548197):
                #     print("CATCH")
                
                length_m = float(row['length'])
                
                self.graph.add_edge(source, target, weight=length_m, **row)
                
    
    def to_geojson_node(self, nodes):
        """Convert a list of nodes to GeoJSON format."""
        features = []
        for node in nodes:
            data = self.graph.nodes[node]
            if 'geometry' in data and data['geometry'].startswith("POINT"):
                coordinates = [float(coord) for coord in data['geometry'].strip("POINT ()").split()]
                features.append({
                    "type": "Feature",
                    "properties": {
                        "node_id": data['osmid'],
                    },
                    "geometry": {
                        "type": "Point",
                        "coordinates": coordinates
                    }
                })
        
        with open("nodes.geojson", "w") as file:
            json.dump({
                "type": "FeatureCollection",
                "features": features
            }, file)
            
            print("GeoJSON file created.")
            
        return {
            "type": "FeatureCollection",
            "features": features
        }
                
                
    def to_geojson_path(self, path):
        """Convert a path (list of nodes) to GeoJSON format."""
        features = []
        for i in range(len(path) - 1):
            source = path[i]
            target = path[i + 1]
            data = self.graph.get_edge_data(source, target)
            if 'geometry' in data and data['geometry'].startswith("LINESTRING"):
                coordinates = [
                    [float(coord.split()[0]), float(coord.split()[1])]
                    for coord in data['geometry'].strip("LINESTRING ()").split(", ")
                ]
                features.append({
                    "type": "Feature",
                    "properties": {
                        "highway_type": data['highway'],
                    }, 
                    "geometry": {
                        "type": "LineString",
                        "coordinates": coordinates
                    }
                })
        
        with open("path.geojson", "w") as file:
            json.dump({
                "type": "FeatureCollection",
                "features": features
            }, file)
            
            print("GeoJSON file created.")
            
        return {
            "type": "FeatureCollection",
            "features": features
        }
        

    def to_geojson_all(self, nodes=True, edges=True, buses=True):
        """Convert only edges (LineStrings) to GeoJSON format."""
        features = []
        
        if (nodes):
            for node_id, data in self.graph.nodes(data=True):
                if 'geometry' in data and data['geometry'].startswith("POINT"):
                    coordinates = [float(coord) for coord in data['geometry'].strip("POINT ()").split()]
                    features.append({
                        "type": "Feature",
                        "properties": {
                            "node_id": data['osmid'],
                        },
                        "geometry": {
                            "type": "Point",
                            "coordinates": coordinates
                        }
                    })
                
        if (buses):
            for stop_id, data in self.buses.items():
                # print(data)
                coordinates = [float(data['X']), float(data['ï»¿Y'])]
                features.append({
                    "type": "Feature",
                    "properties": {
                        "stop_id": stop_id,
                    },
                    "geometry": {
                        "type": "Point",
                        "coordinates": coordinates
                    }
                })
        
        if (edges):
            for source, target, data in self.graph.edges(data=True):
                if 'geometry' in data and data['geometry'].startswith("LINESTRING"):
                    coordinates = [
                        [float(coord.split()[0]), float(coord.split()[1])]
                        for coord in data['geometry'].strip("LINESTRING ()").split(", ")
                    ]
                    features.append({
                        "type": "Feature",
                        "properties": {
                            "highway_type": data['highway'],
                        }, 
                        "geometry": {
                            "type": "LineString",
                            "coordinates": coordinates
                        }
                    })
        
        with open("graph.geojson", "w") as file:
            json.dump({
                "type": "FeatureCollection",
                "features": features
            }, file)
            
            print("GeoJSON file created.")

        return {
            "type": "FeatureCollection",
            "features": features
        }
        
    def all_pairs_shortest_paths(self):
        all_paths = {}
        for source in tqdm(self.graph.nodes):
            all_paths[source] = {}
            for target in self.graph.nodes:
                if source != target:
                    try:
                        path = nx.shortest_path(self.graph, source, target, weight="weight")
                        length = nx.shortest_path_length(self.graph, source, target, weight="weight")
                        all_paths[source][target] = {"path": path, "length": length}
                    except nx.NetworkXNoPath:
                        all_paths[source][target] = {"path": None, "length": float("inf")}
        return all_paths

    def shortest_path(self, source, target):
        try:
            path = nx.shortest_path(self.graph, source, target, weight="weight")
            length = nx.shortest_path_length(self.graph, source, target, weight="weight")
            return {"path": path, "length": length}
        except nx.NetworkXNoPath:
            return {"path": None, "length": float("inf")}
        
    def calculate_network_metrics(self):
        """
        Calculate comprehensive network metrics for a directed graph.

        Returns:
            dict: Network analysis results
        """
        in_degrees = [d for n, d in self.graph.in_degree()]
        out_degrees = [d for n, d in self.graph.out_degree()]
        
        # Checking for strongly connected components before calculating diameter or shortest path
        strongly_connected = list(nx.strongly_connected_components(self.graph))
        is_strongly_connected = len(strongly_connected) == 1 and len(strongly_connected[0]) == self.graph.number_of_nodes()

        return {
            'total_nodes': self.graph.number_of_nodes(),
            'total_edges': self.graph.number_of_edges(),
            'average_node_degree': np.mean([d for n, d in self.graph.degree()]),
            'average_in_degree': np.mean(in_degrees),
            'average_out_degree': np.mean(out_degrees),
            'max_in_degree': max(in_degrees) if in_degrees else 0,
            'max_out_degree': max(out_degrees) if out_degrees else 0,
            'average_clustering_coefficient': nx.average_clustering(self.graph),
            'density': nx.density(self.graph),
            'diameter': nx.diameter(self.graph) if is_strongly_connected else float('inf'),
            'average_shortest_path_length': nx.average_shortest_path_length(self.graph) if is_strongly_connected else float('inf'),
            'assortativity': nx.degree_assortativity_coefficient(self.graph),
            'transitivity': nx.transitivity(self.graph),
            'strongly_connected_components': len(strongly_connected),
            'weakly_connected_components': len(list(nx.weakly_connected_components(self.graph))),
    }
    

    def load_SHA(self, SHA_file):
        """Load SHA data from a CSV file."""

        with open(SHA_file, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            
            i = 1

            for row in tqdm(reader):
                # Fix column name encoding issues
                if 'ï»¿node start' in row:
                    row['node start'] = row.pop('ï»¿node start')
                    
                if '\ufeffnode start' in row:
                    row['node start'] = row.pop('\ufeffnode start')
                    
                if 'node(s) end' in row:
                    row['node end'] = row.pop('node(s) end')

                # Skip rows with missing data
                if row['node start'] == '' and row['node end'] == '':
                    continue

                # Parse AADT values and calculate the average
                average_aadt = 0
                cnt = 0
                for key in row:
                    if key.startswith("AADT"):
                        if key[5].isdigit() or key == 'AADT (Current)':
                            if row[key].strip():
                                average_aadt += float(row[key])
                                cnt += 1

                average_aadt = average_aadt / cnt if cnt > 0 else 0

                # Initialize graph node attributes if not already set
                for node in self.graph.nodes(data=True):
                    if 'average_aadt' not in node[1]:
                        node[1]['average_aadt'] = 0

                # Update the graph nodes' average_aadt
                if row['node start']:
                    node_start_values = eval(row['node start'])  # Convert string like "{49511130, 49524262}" 
                
                if row['node end']:    
                    node_end_values = eval(row['node end'])

                for edge in self.graph.edges(data=True):
                    if float(edge[0]) in node_start_values:
                        # print("CATCH")
                        self.graph.nodes[edge[0]]['average_aadt'] += average_aadt

                    if float(edge[1]) in node_end_values:
                        # print("CATCH")
                        self.graph.nodes[edge[1]]['average_aadt'] += average_aadt

                
    def save_graph(self, filename):
        with open(filename, 'wb') as f:
            pickle.dump(self.graph, f)
        
        print("Graph saved to", filename)

    def load_graph(self, filename):
        with open(filename, 'rb') as f:
            self.graph = pickle.load(f)
            
        print("Graph loaded from", filename)

all_files = {}

all_files['nodes_all'] = "2025_Problem_D_Data/nodes_all.csv"
all_files['edges_all'] = "2025_Problem_D_Data/edges_all.csv"
all_files['nodes_drive'] = "2025_Problem_D_Data/nodes_drive.csv"
all_files['edges_drive'] = "2025_Problem_D_Data/edges_drive.csv"
all_files['Bus_Stops'] = "2025_Problem_D_Data/Bus_Stops.csv"
all_files['SHA'] = "2025_Problem_D_Data/MDOT_SHA_Annual_Average_Daily_Traffic_Baltimore.csv"
all_files['Cache'] = "saved_graphs/network_graph.pkl"

if __name__ == "__main__":
    
    # Load all the data to graph and save it
    G = Graph(all_files['nodes_drive'], all_files['edges_drive'], all_files['Bus_Stops'])
    
    G.to_geojson_all(nodes=True, edges=True, buses=True)
    

    
    
    

    
    
                
    
    
    