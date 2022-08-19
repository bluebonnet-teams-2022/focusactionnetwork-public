import tweepy
import pandas as pd
import sys

twitterHandle = sys.argv[1]

api = tweepy.Client(
    bearer_token="")

userName = twitterHandle
user = api.get_user(username=userName)
userID = user.data.id

tweet_data = pd.DataFrame(columns=['url', 'tweet text'])
tweets = api.get_users_tweets(userID, exclude=["retweets"], max_results=100)


p = tweepy.Paginator(api.get_users_tweets, userID, max_results=100).flatten(limit=1000) # exclude=["retweets"]

ct = 0
remaining_tweets = True
while remaining_tweets:
    until_tweet = None
    remaining_tweets = False
    for response in p:
        remaining_tweets = True
        ct += 1
        # print(info)
        tweet_id = response.id
        url = f"https://twitter.com/{userName}/status/{tweet_id}"
        text = response.text
        tweet_data = tweet_data.append({"url": url, "tweet text": text}, ignore_index=True)
        print(ct, text, url)
    # assign last responded tweet to until-tweet
    until_tweet = response.id
    if remaining_tweets:
        p = tweepy.Paginator(api.get_users_tweets, userID, exclude=["retweets"], until_id=until_tweet,
                             max_results=100).flatten(limit=1000)

tweet_data.to_csv(f"{twitterHandle}TweetsRetweets.csv", index=False)