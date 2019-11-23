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

df = pd.read_csv('./YInt.csv')

# Repeated messages
retweets = df.loc[df["message"].apply(get_retweets)]
tweets = df.loc[df["message"].apply(get_tweets)]
duplicated = df.loc[df.duplicated(['message'])]
duplicated = duplicated.loc[duplicated['message'].apply(get_tweets)]

duplicated_messages_acounts = duplicated['account'].unique()
all_accounts = df["account"].unique()

# print(get_hashtags(df))
print(get_mentions(df))
# print(get_word_count(df))
# print(get_word_count(tweets))
# print(get_word_count(retweets))
# print(get_word_count(duplicated))
