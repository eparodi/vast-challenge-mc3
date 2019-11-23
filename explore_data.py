import pandas as pd

from data_generators import generate_datasets, generate_csv

df = pd.read_csv('./YInt.csv')

retweets, tweets, duplicated, not_duplicated = generate_datasets(df)

datasets = [
    ("total", df),
    ("tweets", tweets),
    ("retweets", tweets),
    ("not_duplicated", not_duplicated)
]

generate_csv(datasets, "./datasets")
