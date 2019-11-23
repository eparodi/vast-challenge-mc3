import pandas as pd
import os

def get_retweets(x: str):
    return str(x).startswith("re:")

def get_tweets(x: str):
    return not str(x).startswith("re:")

def flat_series(series):
    slist =[]
    for x in series:
        if type(x) is list:
            slist.extend(x)
    return pd.Series(slist).value_counts()

def get_word_count(df):
    words = df['message'].str.lower().str.split()
    return flat_series(words)

def get_hashtags(df):
    words = get_word_count(df)
    return words.where(words.index.to_series().str.startswith("#")).dropna()

def get_mentions(df):
    words = get_word_count(df)
    return words.where(words.index.to_series().str.startswith("@")).dropna()

df = pd.read_csv('./YInt.csv')

# Repeated messages
retweets = df.loc[df["message"].apply(get_retweets)]
tweets = df.loc[df["message"].apply(get_tweets)]

duplicated = df.loc[df.duplicated(['message'], keep=False)]
duplicated = duplicated.loc[duplicated['message'].apply(get_tweets)]

not_duplicated = df.drop_duplicates(['message'], keep=False)

duplicated_messages_acounts = duplicated['account'].unique()
all_accounts = df["account"].unique()

datasets = [
    ("total", df),
    ("tweets", tweets),
    ("retweets", tweets),
    ("not_duplicated", not_duplicated)
]

functions = [
    ("word_count", get_word_count),
    ("mentions", get_mentions),
    ("hashtags", get_hashtags)
]

if not os.path.exists("./datasets"):
    os.makedirs("./datasets")

for dataset in datasets:
    for function in functions:
        data = function[1](dataset[1])
        data.to_csv("./datasets/{dataset}_{function}.csv".format(
            dataset=dataset[0],
            function=function[0],
        ))
