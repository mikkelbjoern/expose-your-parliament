# graph2json: exports graph as typescript-file
# node-attributes: 'id' (name), 'group' (party)
# link-attributes: 'weight' (link-strength)

import networkx as nx
from networkx.readwrite import json_graph

def graph2json(G: nx.Graph, name: str):
    # Rename nodes to integers and keep original name as 'name' attribute
    names = dict(enumerate(G.nodes()))
    mapping = dict([(n,i) for i,n in names.items()])
    H = nx.relabel_nodes(G, mapping)
    nx.set_node_attributes(H,names,'name')
    
    # Save degrees
    degrees = dict(H.degree())
    nx.set_node_attributes(H,degrees,'degree')
    
    # Save json    
    json = json_graph.node_link_data(H)
    f = open('app/public/data/' + name + '.json', 'w', encoding='utf8')
    f.write(str({ "nodes": json['nodes'], "links": json['links'] }).replace("'",'"'))
    f.close()
        