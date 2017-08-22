import os
import sys
from datetime import timezone

import tweepy
import bigquery

# Twitterの認証情報を読み込む。
CONSUMER_KEY = os.environ['CONSUMER_KEY']
CONSUMER_SECRET = os.environ['CONSUMER_SECRET']
ACCESS_TOKEN = os.environ['ACCESS_TOKEN']
ACCESS_TOKEN_SECRET = os.environ['ACCESS_TOKEN_SECRET']

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

# BigQueryの認証情報（credentials.json）を指定してBigQueryのクライアントを作成する。
# 明示的にreadonly=Falseとしないと書き込みができない。
client = bigquery.get_client(json_key_file='credentials.json', readonly=False)

DATASET_NAME = 'twitter'  # BigQueryのデータセット名
TABLE_NAME = 'tweets'  # BigQueryのテーブル名

# テーブルが存在しない場合は作成する。
if not client.check_table(DATASET_NAME, TABLE_NAME):
    print('Creating table {0}.{1}'.format(DATASET_NAME, TABLE_NAME), file=sys.stderr)
    # create_table()の第3引数にはスキーマを指定する。
    client.create_table(DATASET_NAME, TABLE_NAME, [
        {'name': 'id',          'type': 'string',    'description': 'ツイートのID'},
        {'name': 'lang',        'type': 'string',    'description': 'ツイートの言語'},
        {'name': 'screen_name', 'type': 'string',    'description': 'ユーザー名'},
        {'name': 'text',        'type': 'string',    'description': 'ツイートの本文'},
        {'name': 'created_at',  'type': 'timestamp', 'description': 'ツイートの日時'},
    ])


class MyStreamListener(tweepy.streaming.StreamListener):
    """
    Streaming APIで取得したツイートを処理するためのクラス。
    """

    status_list = []
    num_imported = 0

    def on_status(self, status):
        """
        ツイートを受信したときに呼び出されるメソッド。
        引数: ツイートを表すStatusオブジェクト。
        """
        self.status_list.append(status)  # Statusオブジェクトをstatus_listに追加する。

        if len(self.status_list) >= 500:
            # status_listに500件溜まったらBigQueryにインポートする。
            if not push_to_bigquery(self.status_list):
                # インポートに失敗した場合はFalseが返ってくるのでエラーを出して終了する。
                print('Failed to send to bigquery', file=sys.stderr)
                return False

            # num_importedを増やして、status_listを空にする。
            self.num_imported += len(self.status_list)
            self.status_list = []
            print('Imported {0} rows'.format(self.num_imported), file=sys.stderr)

            # 料金が高額にならないように、5000件をインポートしたらFalseを返して終了する。
            # 継続的にインポートしたいときは次の2行をコメントアウトしてください。
            if self.num_imported >= 5000:
                return False


def push_to_bigquery(status_list):
    """
    ツイートのリストをBigQueryにインポートする。
    """

    # TweepyのStatusオブジェクトのリストからdictのリストに変換する。
    rows = []
    for status in status_list:
        rows.append({
            'id': status.id_str,
            'lang': status.lang,
            'screen_name': status.author.screen_name,
            'text': status.text,
            # datetimeオブジェクトをUTCのPOSIXタイムスタンプに変換する。
            'created_at': status.created_at.replace(tzinfo=timezone.utc).timestamp(),
        })

    # dictのリストをBigQueryにインポートする。
    # 引数は順に、データセット名、テーブル名、行のリスト、行を一意に識別する列名を表す。
    # insert_id_keyはエラーでリトライしたときに重複しないようにするために使われるが、必須ではない。
    return client.push_rows(DATASET_NAME, TABLE_NAME, rows, insert_id_key='id')

# Streaming APIの読み込みを開始する。
print('Collecting tweets...', file=sys.stderr)
stream = tweepy.Stream(auth, MyStreamListener())
# 公開されているツイートをサンプリングしたストリームを受信する。
# 言語を指定していないので、あらゆる言語のツイートを取得できる。
stream.sample()
