from helpers import get_retweets, get_tweets, functions
import os

def generate_datasets(df):
    retweets = df.loc[df["message"].apply(get_retweets)]
    tweets = df.loc[df["message"].apply(get_tweets)]

    duplicated = df.loc[df.duplicated(['message'], keep=False)]
    duplicated = duplicated.loc[duplicated['message'].apply(get_tweets)]

    not_duplicated = df.drop_duplicates(['message'], keep=False)
    return (
        retweets,
        tweets,
        duplicated,
        not_duplicated,
    )

def get_account_info(df):
    duplicated = df.loc[df.duplicated(['message'], keep=False)]
    duplicated = duplicated.loc[duplicated['message'].apply(get_tweets)]
    duplicated_messages_acounts = duplicated['account'].unique()
    all_accounts = df["account"].unique()
    return (
        all_accounts,
        duplicated_messages_acounts,
    )

def generate_csv(datasets, path):
    if not os.path.exists(path):
        os.makedirs(path)

    for dataset in datasets:
        for function in functions:
            data = function[1](dataset[1])
            filename = os.path.join(path, "{dataset}_{function}.csv".format(
                path=path,
                dataset=dataset[0],
                function=function[0],
            ))
            data.to_csv(filename)