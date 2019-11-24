import pandas as pd
import os

from graph_generators import get_account_nodes, generate_mention_edges, cut_graph
from data_generators import generate_datasets, generate_csv

df = pd.read_csv('./YInt.csv')
nodes = get_account_nodes(df)
edges = generate_mention_edges(df, nodes)

nodes, edges = cut_graph(nodes, edges, 50)

nodes["label"] = nodes["account"]
nodes["value"] = nodes["counts"]
nodes = nodes.drop(["account", "counts"], axis=1)

edges["value"] = edges["count"]
edges = edges.drop(["count"], axis=1)

path = "./datasets/graph"
if not os.path.exists(path):
    os.makedirs(path)

nodes.to_json(os.path.join(path, "nodes.json"), orient='records')
edges.to_json(os.path.join(path, "edges.json"), orient='records')