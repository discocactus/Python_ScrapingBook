import os

import tweepy

# 環境変数から認証情報を取得する。
CONSUMER_KEY = os.environ['CONSUMER_KEY']
CONSUMER_SECRET = os.environ['CONSUMER_SECRET']
ACCESS_TOKEN = os.environ['ACCESS_TOKEN']
ACCESS_TOKEN_SECRET = os.environ['ACCESS_TOKEN_SECRET']

# 認証情報を設定する。
auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)


class MyStreamListener(tweepy.StreamListener):
    """
    Streaming APIで取得したツイートを処理するためのクラス。
    """

    def on_status(self, status):
        """
        ツイートを受信したときに呼び出されるメソッド。引数はツイートを表すStatusオブジェクト。
        """
        print('@' + status.author.screen_name, status.text)

# 認証情報とStreamListenerを指定してStreamオブジェクトを取得する。
stream = tweepy.Stream(auth, MyStreamListener())
# 公開されているツイートをサンプリングしたストリームを受信する。
# キーワード引数languagesで、日本語のツイートのみに絞り込む。
stream.sample(languages=['ja'])
