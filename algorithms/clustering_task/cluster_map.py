import matplotlib.pyplot as plt
import json
import shapely
import math
import networkx as nx
from networkx import minimum_spanning_tree

def draw_graph(graph): 
    pos = nx.spring_layout(graph)
    plt.figure(figsize=(7, 6))
    nx.draw_networkx_nodes(graph, pos)
    nx.draw_networkx_edges(graph, pos, graph.edges)
    nx.draw_networkx_labels(graph, pos, font_size=20)
    plt.show()

def distance(site1, site2): #дистанция между точками
    loc1 = site1["location"]
    loc2 = site2["location"]
    r = 6371 #радиус Земли
    phi1 = math.radians(loc1["lat"])
    phi2 = math.radians(loc2["lat"])
    dphi = math.radians(loc2["lat"] - loc1["lat"])
    dlambda = math.radians(loc2["lon"] - loc1["lon"])
    a = math.sin(dphi/2) ** 2 + (math.cos(phi1) * math.cos(phi2) * math.sin(dlambda/2) ** 2)
    c = 2 * math.atan2(a**0.5, (1-a) ** 0.5)
    return int(r * c)

def make_graph(sites, max_distance=50): #строим граф 
    #соединяем точки в радиусе max_distance км, если точек нет, ищем ближайшую
    edges = []
    nodes = []
    for i, site in enumerate(sites[:-1]):
        nodes.append(site["code"])
        min_distance = 10 ** 16 
        min_dest = None
        min_dest_flag = True
        for dest in sites[i+1:]:
            d = distance(site, dest)
            if d <= max_distance:
                edges.append((site["code"], dest["code"], d))
                min_dest_flag = False
            if d < min_distance: #ищем ближайшую
                min_dest = dest
                min_distance = d 
        if min_dest_flag:
            edges.append((site["code"], min_dest["code"], min_distance))
    return edges, nodes

def get_spanning_trees(graph): 
    graph2 = graph
    edges, nodes = [], []
    for node in graph2.nodes:
        nodes.append(node)
        connected_edges = list(filter(lambda edge: edge[1] not in nodes,
                                 graph2.edges(node)))
        min_edge = sorted(connected_edges, key=lambda e: graph2.get_edge_data(*e)["weight"])
        if (len(min_edge) != 0):
            min_edge = min_edge[0]
        else:
            continue
        edges.append(min_edge + (graph2.get_edge_data(*min_edge)["weight"], ))
        graph2.remove_edges
    result = nx.Graph()
    result.add_weighted_edges_from(edges)
    result.add_nodes_from(nodes) 
    return result

def get_clusters(graph: nx.Graph, n_clusters: int): 
    spanning_tree = minimum_spanning_tree(graph)
    sorted_edges = sorted(spanning_tree.edges(data=True),
                           key=lambda x: x[2]['weight'], reverse=True)
    copy_tree = spanning_tree.copy()
    for i in range(n_clusters - 1):
        if len(sorted_edges) > i:
            copy_tree.remove_edge(*sorted_edges[i][:2])
    return list(nx.connected_components(copy_tree))


with open("base.json", "r") as f:
    sites = json.load(f)
    lons = []
    lats = []
    for site in sites:
        lons.append(site["location"]["lon"])
        lats.append(site["location"]["lat"])

with open("continents.json", "r") as f:
    continents = json.load(f)
    north_america_polygon = continents["features"][1]["geometry"]["coordinates"]

max_polygon = []
max_area = 0

for i in range(len(north_america_polygon)):
    points = north_america_polygon[i][0]
    area = shapely.Polygon(points).area
    if area > max_area:
        max_polygon = points
        max_area = area

xs, ys = zip(*max_polygon)

north_america = shapely.Polygon(max_polygon)
north_america_sites = []
for site in sites:
    p = shapely.Point((site["location"]["lon"]), (site["location"]["lat"]))
    if north_america.contains(p):
        north_america_sites.append(site)

flons = []
flats = []
for site in north_america_sites:
    flons.append(site["location"]["lon"])
    flats.append(site["location"]["lat"])

#plt.scatter(lons, lats)
#plt.scatter(flons, flats)
#plt.plot(xs, ys)
#plt.show()
edges, nodes = make_graph(north_america_sites)
graph = nx.Graph()
graph.add_weighted_edges_from(edges)
graph.add_nodes_from(nodes)

result = get_clusters(graph, 40)
print(result)
print("Number of clusters: ", len(result))
