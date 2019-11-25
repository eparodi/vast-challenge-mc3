import pandas as pd
from helpers import get_retweets, get_tweets
from data_generators import generate_csv

df = pd.read_csv('./YInt.csv')

def get_accounts(data):
    data_without_retweets = data.loc[data['message'].apply(get_tweets)]
    data_retweets_only = data.loc[data['message'].apply(get_retweets)]
    grouped_by_account = data_without_retweets.groupby('account')['message'].count()
    ret = pd.DataFrame({'account':[], 'tweets': [], 'mentions': [], 'times_retweeted': []})
    i = 1
    for account, tweet_count in grouped_by_account.iteritems():
        print("{account}: {i} of {total}".format(
            account=account,
            i=i,
            total=grouped_by_account.count()
        ))
        i += 1
        mentions = data.loc[(data['account'] != account) & (data['message'].str.contains('@' + account))]
        tweets = data_without_retweets.loc[data_without_retweets['account'] == account]
        tweets['message'] = tweets['message'].apply(lambda x: 're: {msg}'.format(msg=x))
        retweets = data_retweets_only.loc[(data_retweets_only['account'] != account) & (data_retweets_only['message'].isin(tweets['message']))]
        ret = ret.append(
            {'account': account,
            'tweets': tweet_count,
            'mentions': mentions['message'].count(),
            'times_retweeted': retweets['message'].count()}, ignore_index=True)
    ret = ret[['account', 'tweets', 'mentions', 'times_retweeted']]
    return ret

get_accounts(df).to_csv("datasets/accounts.csv")
