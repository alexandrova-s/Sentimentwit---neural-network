# https://machinelearningmastery.com/deep-learning-bag-of-words-model-sentiment-analysis/
# https://medium.com/analytics-vidhya/simplifying-social-media-sentiment-analysis-using-vader-in-python-f9e6ec6fc52f

import string
import pandas as pd
from nltk.corpus import stopwords
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

# define inpt file name (file generated by twitt_downloader.py)
filename = 'twitt_downloader_output_example.csv'
# define output file name
pd_to_csv_file = 'vadered_tweets_example.csv'


analyser = SentimentIntensityAnalyzer()
# obtain the VADER compound polarity index for the given sentence
def vader_sentiment_score(sentence):
    score = analyser.polarity_scores(sentence)
    return score.get('compound')


# obtain the VADER polarity index for the given dataframe containing column 'tweet_text'
def pd_vader_sentiment(df, col, val):
    try:
        list = df[col].tolist()
        list = [round((vader_sentiment_score(tweet)+1)*5) for tweet in list]
        df.insert(len(df.columns), 'VADER_%s'%val, list)
        return df
    except:
        print("Czy tabela na pewno zawiera kolumne 'tweet_text?/ew inny error")


#######

def load_tweets_for_preprocessing(filename):
    df = pd.read_csv(filename, encoding='utf-8', sep='\t')
    list = df['tweet_text'].tolist()
    return list

def preprocess(tokens):
    # remove punctuation from each tweet
    table = str.maketrans('', '', string.punctuation)
    tokens = [tweet.translate(table) for tweet in tokens]
    # to lowercase
    tokens = [tweet.lower() for tweet in tokens]
    stop_words = set(stopwords.words('english'))
    newtokens = []
    for tweet in tokens:
        words = tweet.split()
        # remove remaining tokens that are not alphabetic
        words = [word for word in words if word.isalpha()]
        # filter out stop words
        words = [w for w in words if not w in stop_words]
        # filter out short tokens
        words = [word for word in words if len(word) > 1]
        tweet = str(" ".join(words))
        newtokens.append(str(tweet))
    return newtokens

################################################


#reading form csv file to pd dataframe
df = pd.read_csv(filename, encoding='utf-8', sep='\t')

# load tweets from dataframe
tweets_raw = load_tweets_for_preprocessing(filename)

print('\n')
print('Przyklady surowych tweetow:')
print(tweets_raw[:10])

# preprocessing raw tweets
tweets_preprocessed = preprocess(tweets_raw)
df.insert(len(df.columns), 'tweet_proc', tweets_preprocessed)

print('Przyklady obrobionych tweetow:')
print(tweets_preprocessed[:10])

# VADER sentiment score for raw tweet
pd_vader_sentiment(df,'tweet_text', 'raw')
# VADER sentiment score for preprocessed tweet
pd_vader_sentiment(df,'tweet_proc', 'proc')

print('VADER dla twittow surowych:')
vader_raw_score = df['VADER_raw'].tolist()
print(vader_raw_score [:10])

print('VADER dla twittow obrobonych:')
vader_proc_score = df['VADER_proc'].tolist()
print(vader_proc_score[:10])


# header = ["tweet_text", "tweet_proc", "VADER_raw", "VADER_proc"]
header = ["tweet_proc", "VADER_raw", "VADER_proc"]
df.to_csv(pd_to_csv_file,columns = header, encoding='utf-8', index=False, sep='\t')

