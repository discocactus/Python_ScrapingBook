import os

from apiclient.discovery import build  # pip install google-api-python-cliet

YOUTUBE_API_KEY = os.environ['YOUTUBE_API_KEY']  # 環境変数からAPIキーを取得する。

# YouTubeのAPIクライアントを組み立てる。build()関数の第1引数にはAPI名を、
# 第2引数にはAPIのバージョンを指定し、キーワード引数developerKeyでAPIキーを指定する。
# この関数は、内部的に https://www.googleapis.com/discovery/v1/apis/youtube/v3/rest という
# URLにアクセスし、APIのリソースやメソッドの情報を取得する。
youtube = build('youtube', 'v3', developerKey=YOUTUBE_API_KEY)

# キーワード引数で引数を指定し、search.listメソッドを呼び出す。
# list()メソッドでgoogleapiclient.http.HttpRequestオブジェクトが得られ、
# execute()メソッドを実行すると実際にHTTPリクエストが送られて、APIのレスポンスが得られる。
search_response = youtube.search().list(
    part='snippet',
    q='手芸',
    type='video',
).execute()

# search_responseはAPIのレスポンスのJSONをパースしたdict。
for item in search_response['items']:
    print(item['snippet']['title'])  # 動画のタイトルを表示する。
