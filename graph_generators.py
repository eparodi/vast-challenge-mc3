import pandas as pd
import re

def get_account_nodes(df):
    nodes = df.groupby(["account"]).size().reset_index(name='counts')
    nodes["id"] = nodes.index
    return nodes

def generate_mention_edges(df, nodes):
    edges = {}
    for _, row in df.iterrows():
        words = re.split(r"(?<=[.!?])\s+", str(row["message"]))
        words = [w for word in words for w in word.split()]
        for word in words:
            if word.startswith("@"):
                to_id = nodes.index[nodes["account"] == word[1:]]
                if (len(to_id) == 0):
                    nodes = nodes.append({'account' : word[1:] , 'counts' : 0} , ignore_index=True)
                    to_id = nodes.index[nodes["account"] == word[1:]]
                from_id = nodes.index[nodes["account"] == row["account"]]
                key = (from_id[0], to_id[0])
                if not key in edges:
                    edges[key] = 0
                edges[key] += 1
    edges = [{"from": key[0], "to": key[1], "count": value} for key, value in edges.items()]
    return pd.DataFrame(edges)

def cut_graph(nodes, edges, n):
    accounts = edges.drop(["to"], axis=1).groupby("from").sum().sort_values(
        by=['count'],
        ascending=False
    ).reset_index()
    accounts = accounts.head(n)
    ids = accounts["from"]
    edges = edges.loc[edges['from'].isin(ids) & edges['to'].isin(ids)]
    nodes = nodes.loc[nodes['id'].isin(edges['from']) | nodes['id'].isin(edges['to'])]
    return nodes, edges

# def generate_account_nodes(df):
#     accounts = get_accounts(df)
#     print(pd.DataFrame(accounts))