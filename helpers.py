import pandas as pd

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

functions = [
    ("word_count", get_word_count),
    ("mentions", get_mentions),
    ("hashtags", get_hashtags)
]