import pandas as pd
import re

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
    words = df['message'].str.lower().apply(
        lambda x : re.compile('[\W_]+').sub(' ', str(x)).split()
    )
    return flat_series(words)

def get_word_count_altered(df):
    words = df['message'].str.lower().str.split()
    return flat_series(words)

def get_hashtags(df):
    words = get_word_count_altered(df)
    return words.where(words.index.to_series().str.startswith("#")).dropna()

def get_mentions(df):
    words = get_word_count_altered(df)
    return words.where(words.index.to_series().str.startswith("@")).dropna()

def filter_spam(df):
    return df.loc[~df["account"].isin(SPAM_ACCOUNTS)]

SPAM_ACCOUNTS = [
    "______3333_____",
    "CantonCoordon2",
    "Cheryl_MeeksFish82",
    "CookWhatWhen81",
    "handle",
    "J0rdanWantsBacon",
    "JordanWantsBac0n",
    "Opportunities1",
    "Opportunities2",
    "Syndicated4",
    "Syndicated5",
    "Syndicated348",
]

functions = [
    ("word_count", get_word_count),
    ("mentions", get_mentions),
    ("hashtags", get_hashtags)
]

sewer_and_water = ['discharged', 'discharge', 'drain', 'drainage', 'flood', 'hygiene', 'irrigation', 'pipes', 'pump', 'river', 'sanitary', 'sewage', 'sewer', 'stream', 'underground', 'wash', 'waste', 'water']
power = ['valve', 'heat', 'gas', 'power', 'electric', 'candle', 'flashlight', 'generator', 'black out', 'blackout', 'dark', 'radiation', 'radio rays', 'energy', 'nuclear', 'fuel', 'battery', 'radiant']
roads_and_bridges = ['airport', 'avenue', 'bridge', 'bus', 'congestion', 'drive', 'flight', 'jam', 'logistic', 'metro', 'mta', 'road', 'street', 'subway', 'traffic', 'train', 'transit', 'transportation', 'highway', 'route', 'lane']
medical = ['medical', 'red cross', 'food', 'emergency', 'urgent', 'evacuate', 'evacuating', 'evacuation', 'protection', 'ambulance', 'escape', 'first aid', 'rescue', 'rescuing', 'dead', 'death', 'kill', 'help', 'volunteer', 'volunteering', 'explosion', 'exploding', 'explode', 'victim', 'fatalities']
buildings = ['collapse', 'housing', 'house']
earth_quake = ['shake', 'wobble', 'quiver', 'earthquake', 'quake', 'seismic', 'emergency', 'rumble']

categories = {
    "sewer_and_water": sewer_and_water,
    "power": power,
    "roads_and_bridges": roads_and_bridges,
    "medical": medical,
    "buildings": buildings,
    "earth_quake": earth_quake,
}