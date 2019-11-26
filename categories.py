import pandas as pd

from data_generators import get_categories, generate_datasets

df = pd.read_csv('./YInt.csv')

retweets, tweets, duplicated, not_duplicated = generate_datasets(df)

tweets = get_categories(tweets)
df = get_categories(df)

tweets.to_csv("datasets/keyword_tweets.csv")
df.to_csv("datasets/keyword_total.csv")