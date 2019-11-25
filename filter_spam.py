import pandas as pd
from helpers import filter_spam

df = pd.read_csv('./YInt.csv')
print(filter_spam(df))