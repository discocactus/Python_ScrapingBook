import os

import tweepy  # pip install tweepy

# 環境変数から認証情報を取得する。
CONSUMER_KEY = os.environ['CONSUMER_KEY']
CONSUMER_SECRET = os.environ['CONSUMER_SECRET']
ACCESS_TOKEN = os.environ['ACCESS_TOKEN']
ACCESS_TOKEN_SECRET = os.environ['ACCESS_TOKEN_SECRET']

# 認証情報を設定する。
auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

api = tweepy.API(auth)  # APIクライアントを取得する。
public_tweets = api.home_timeline()  # ユーザーのタイムラインを取得する。

for status in public_tweets:
    print('@' + status.user.screen_name, status.text)  # ユーザー名とツイートを表示する。
