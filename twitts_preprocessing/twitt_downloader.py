import tweepy
import pandas as pd
import csv

# ###########https://gist.github.com/vickyqian/f70e9ab3910c7c290d9d715491cde44c

# how many tweets to download
no_of_tweets = 50
q_filter = "#potus -#BackfireTrump -filter:retweets"
# # define filename when using .txt
# file_name = 'txt1.txt'
pd_to_csv_file = "pdtocsv.csv"

# ###input credentials here
consumer_key = 'nRR5hPY7iZexRzOw77DcYD8Vj'
consumer_secret = 'sdrdaIn1gqzZyA0kJCcWY7Z0huVAAiUjG3SobwbSXnvLpzxHf9'
access_token = '1056251527478816769-9hAcdn591PlLokxQfKeWQUqwNbsLp0'
access_token_secret = 'MZ2Q0i6RIJI2MA4lE6Ct9n9u8neHUlx2njB0sROp53Lsi'

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth, wait_on_rate_limit=True)


#create pandas dataframe object
df = pd.DataFrame(columns=["datetime", "tweet_text"])

# # Use csv Writer
# csvFile = open('csv1.csv', 'w', encoding='utf-8')
# csvWriter = csv.writer(csvFile)

# # Open/Create a file to append data
# text_file = open(file_name, "w", encoding='utf-8')

for tweet in tweepy.Cursor(api.search,
                           q=q_filter,
                           count=500,
                           lang="en",
                           tweet_mode='extended',
                           since="2018-12-27").items(no_of_tweets):

    # stringed_datetime = tweet.created_at.strftime("%Y-%m-%d %H:%M:%S")

    df = df.append({
        "datetime": tweet.created_at,
        "tweet_text": tweet.full_text
    }, ignore_index=True)

    # text_file.write("%s %s\n\n" % (stringed_datetime, tweet.full_text))

    print(tweet.created_at, tweet.full_text)

    # csvWriter.writerow([tweet.full_text]) # tweet.full_text.encode('utf-8')])
    # csvWriter.writerow([tweet.created_at, tweet.full_text]) # tweet.full_text.encode('utf-8')])


print(df)
print('\n')

df.to_csv(pd_to_csv_file, encoding='utf-8', index=False, sep='\t')

# #reading form csv file to pd dataframe
# new_df = pd.read_csv(pd_to_csv_file, encoding='utf-8', sep='\t')
# print(new_df)