
# coding: utf-8

# # chapter 5-1 データセットの取得と活用
# Wikipediaのデータセットのダウンロード# !wget https://dumps.wikimedia.org/jawiki/latest/jawiki-latest-pages-articles1.xml-p1p168815.bz2
# Wikipediaのデータセット(ダンプファイル)の取得# ! bzcat jawiki-latest-pages-articles1.xml-p1p168815.bz2 | less
# 解凍せず中身を閲覧可能
# j: 下スクロール, k: 上スクロール, q: 終了# !wget https://github.com/attardi/wikiextractor/raw/master/WikiExtractor.py
# WikiExtractor.py スクリプトをインストール# !python WikiExtractor.py --no-templates -o articles -b 100M jawiki-latest-pages-articles1.xml-p1p168815.bz2
# スクリプトを用いてダンプファイルのマークアップを取り除きテキストに変換# !tree articles/
# ディレクトリの確認
# # 自然言語処理技術を用いた頻出単語の抽出
# !brew install mecab-ipadic
# MeCabのインストール# !mecav -v
# バージョンの確認# !pip install mecab-python3
# Python3対応バインディングのインストール(MeCab公式ではない。公式は未対応?)# MeCabをPythonから使う
# In[ ]:


get_ipython().run_cell_magic('writefile', 'mecab_sample.py', "\n# MeCabをPythonから使う\n\nimport MeCab\n\ntagger = MeCab.Tagger()\ntagger.parse('') # これは.parseToNode()の不具合を回避するのに必要\n\n# .parseToNode()で最初の形態素を表すNodeオブジェクトを取得する\nnode = tagger.parseToNode('すもももももももものうち')\n\nwhile node:\n    # .surfaceは形態素の文字列、.featureは品詞などを含む文字列をそれぞれ表す\n    print(node.surface, node.feature)\n    node = node.next # .nextで次のNodeを取得する")


# In[ ]:


get_ipython().system('python mecab_sample.py')

# 以下でもほぼ同様の結果が得られる
# !echo すもももももももものうち | mecab
# # 文章から頻出単語を抽出する
# Wikipediaの文章から頻出単語を抜き出す
# In[ ]:


get_ipython().run_cell_magic('writefile', 'word_frequency.py', '\n# Wikipediaの文章から頻出単語を抜き出す\n\nimport sys\nimport os\nfrom glob import glob\nfrom collections import Counter\nimport MeCab\n\ndef main():\n    """\n    コマンドライン引数で指定したディレクトリ内のファイルを読み込んで頻出単語を抽出する\n    """\n    \n    input_dir = sys.argv[1] # コマンドラインの第1引数でWikiExtractorの出力先のディレクトリを指定する\n    \n    tagger = MeCab.Tagger(\'\')\n    tagger.parse(\'\') # .parseToNode()の不具合を回避するのに必要\n    # 単語の頻度を格納するCounterオブジェクトを作成する\n    # Counterクラスはdictを継承しており、値としてキーの出現回数を保持する\n    frequency = Counter()\n    count_proccessed = 0\n    \n    # glob()でワイルドカードにマッチするファイルのリストを取得し、マッチしたすべてのファイルを処理する\n    for path in glob(os.path.join(input_dir, \'*\', \'wiki_*\')):\n        print(\'Proccessing {0}...\'.format(path), file=sys.stderr)\n        \n        with open(path) as file: # ファイルを開く\n            for content in iter_docs(file): # ファイル内の全記事について反復処理する\n                tokens = get_tokens(tagger, content) # ページから名詞のリストを取得する\n                # Counterのupdate()メソッドにリストなどの反復可能オブジェクトを指定すると、\n                # リストに含まれる値の出現回数を一度に増やせる\n                frequency.update(tokens)\n                \n                # 10,000件ごとに進捗を表示\n                count_proccessed += 1\n                if count_proccessed % 10000 == 0:\n                    print(\'{0} documents were proccessed.\'.format(count_proccessed),\n                         file=sys.stderr)\n                    \n    # 全記事の処理が完了したら上位30件の名詞と出現回数を表示する\n    for token, count in frequency.most_common(30):\n        print(token, count)\n        \n        \ndef iter_docs(file):\n    """\n    ファイルオブジェクトを読み込んで、記事の中身(開始タグ<doc ...>と終了タグ</doc>の間のテキスト)を\n    順に返すジェネレーター関数\n    """\n    \n    for line in file:\n        if line.startswith(\'<doc \'):\n            buffer = [] # 開始タグが見つかったらバッファを初期化する\n        elif line.startswith(\'</doc>\'):\n            # 終了タグが見つかったらバッファの中身を結合してyieldする\n            content = \'\'.join(buffer)\n            yield content\n        else:\n            buffer.append(line) # 開始タグ・終了タグ以外の業はバッファに追加する\n            \n            \ndef get_tokens(tagger, content):\n    """\n    文書内に出現した名詞のリストを取得する関数\n    """\n    \n    tokens = [] # この記事で出現した名詞を格納するリスト\n    \n    node = tagger.parseToNode(content)\n    while node:\n        # node.featureはカンマで区切られた文字列なので、split() で分割して\n        # 最初の2項目をcategoryとsub_categoryに代入する\n        category, sub_category = node.feature.split(\',\')[:2]\n        # 固有名詞または一般名詞の場合のみtokensに追加する\n        if category == \'名詞\' and sub_category in (\'固有名詞\', \'一般\'):\n            tokens.append(node.surface)\n        node = node.next\n        \n    return tokens\n\n\nif __name__ == \'__main__\':\n    main()')


# In[ ]:


get_ipython().system('python word_frequency.py articles')


# # chapter 5-2 APIによるデータの収集と活用

# # Twitterからのデータの収集

# # Requests-OAuthlibを使ったTwitter REST APIの利用
# 認証情報は環境変数に記述して、そこから取得するようにする
# In[ ]:


get_ipython().run_cell_magic('writefile', 'rest_api_with_requests_oauthlib.py', "\n# Requests-OAuthlibを使ってタイムラインを取得する\n\nimport os\nfrom requests_oauthlib import OAuth1Session\n\n# 環境変数から認証情報を取得する\nCONSUMER_KEY = os.environ['CONSUMER_KEY']\nCONSUMER_SECRET = os.environ['CONSUMER_SECRET']\nACCESS_TOKEN = os.environ['ACCESS_TOKEN']\nACCESS_TOKEN_SECRET = os.environ['ACCESS_TOKEN_SECRET']\n\n# 認証情報を使ってOAuth1Sessionオブジェクトを得る\ntwitter = OAuth1Session(CONSUMER_KEY,\n                       client_secret=CONSUMER_SECRET,\n                       resource_owner_key=ACCESS_TOKEN,\n                       resource_owner_secret=ACCESS_TOKEN_SECRET)\n\n# ユーザーのタイムラインを取得する\nresponse = twitter.get('https://api.twitter.com/1.1/statuses/home_timeline.json')\n\n# APIのレスポンスはJSON形式なので、response.json()でパースしてlistを取得できる\n# statusはツイート(Twitter APIではStatusと呼ばれる)を表すdict\nfor status in response.json():\n    print('@' + status['user']['screen_name'], status['text']) # ユーザー名とツイートを表示する")


# In[ ]:


get_ipython().system('forego run python rest_api_with_requests_oauthlib.py')


# # TweepyによるTwitter REST APIの利用

# In[ ]:


get_ipython().run_cell_magic('writefile', 'rest_api_withtweepy.py', "\n# Tweepyを使ってタイムラインを取得する\n\nimport os\nimport tweepy\n\n# 環境変数から認証情報を取得する\nCONSUMER_KEY = os.environ['CONSUMER_KEY']\nCONSUMER_SECRET = os.environ['CONSUMER_SECRET']\nACCESS_TOKEN = os.environ['ACCESS_TOKEN']\nACCESS_TOKEN_SECRET = os.environ['ACCESS_TOKEN_SECRET']\n\n# 認証情報を設定する\nauth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)\nauth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)\n\napi = tweepy.API(auth) # APIクライアントを取得する\npublic_tweets = api.home_timeline() # ユーザーのタイムラインを取得する\n\n# 得られるツイートのオブジェクトはTweepyのStatusオブジェクト\nfor status in public_tweets:\n    print('@' + status.user.screen_name, status.text) # ユーザー名とツイートを取得する")


# In[ ]:


get_ipython().system('forego run python rest_api_withtweepy.py')


# # code 5.5 TweepyによるTwitter Streaming APIの利用

# In[ ]:


get_ipython().run_cell_magic('writefile', 'streaming_api_with_tweepy.py', '\n# TweepyによるStreaming APIの利用\n\nimport os\nimport tweepy\n\n# 環境変数から認証情報を取得する\nCONSUMER_KEY = os.environ[\'CONSUMER_KEY\']\nCONSUMER_SECRET = os.environ[\'CONSUMER_SECRET\']\nACCESS_TOKEN = os.environ[\'ACCESS_TOKEN\']\nACCESS_TOKEN_SECRET = os.environ[\'ACCESS_TOKEN_SECRET\']\n\n# 認証情報を設定する\nauth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)\nauth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)\n\n\nclass MyStreamListener(tweepy.StreamListener):\n    """\n    Streaming APIで取得したツイートを処理するためのクラス\n    """\n    \n    def on_status(self, status):\n        """\n        ツイートを受信した時に呼び出されるメソッド\n        引数はツイートを表すStatusオブジェクト\n        """\n        print(\'@\' + status.author.screen_name, status.text)\n        \n        \n# 認証情報とStreamListenerを指定してStreamオブジェクトを取得する\nstream = tweepy.Stream(auth, MyStreamListener())\n# 公開されているツイートをサンプリングしたストリームを受信する\n# キーワード引数languagesで日本語のツイートのみに絞り込む\nstream.sample(languages=[\'ja\'])')

# !forego run python streaming_api_with_tweepy.py
# 次々にツイートが表示されるので、実行はターミナルで
# キャンセルは ctrl + C
# # Amazonの商品情報の収集
# Amazonアソシエイト・プログラムに登録するのが面倒なので後回し
# # YouTubeからの動画情報の収集
# ターミナル上のcurlコマンドでYouTube Data APIを使う
# 面倒なので後回し
# # Google API Client for Pythonを使う

# In[ ]:


get_ipython().run_cell_magic('writefile', 'search_youtube_videos.py', "\n# YouTubuの動画を検索する\n\nimport os\nfrom apiclient.discovery import build\n\nYOUTUBE_API_KEY = os.environ['YOUTUBE_API_KEY'] # 環境変数からAPIキーを取得する\n\n# YouTubeのAPIクライアントを組み立てる\n# build()関数の第1引数にはAPI名を、第2引数にはAPIのバージョンを指定し、\n# キーワード引数developerKeyでAPIキーを指定する\n# この関数には内部的にYouTube API用のURLにアクセスし、APIのリソースやメソッドの情報を取得する\nyoutube = build('youtube', 'v3', developerKey=YOUTUBE_API_KEY)\n\n# キーワード引数で引数を指定し、search.listメソッドを呼び出す\n# list()メソッドでgoogleapiclient.http.HttpRequestオブジェクトが得られ、\n# execute()メソッドを実行すると実際にHTTPリクエストが送られて、APIのレスポンスが得られる\nsearch_response = youtube.search().list(\n    part='snippet',\n    q='手芸',\n    type='video',\n).execute()\n\n# search_responseはAPIのレスポンスのJSONをパースしたdict\nfor item in search_response['items']:\n    print(item['snippet']['title']) # 動画のタイトルを表示する")


# In[ ]:


get_ipython().system('forego run python search_youtube_videos.py')


# # 動画情報(メタデータ含む)をMongoDBに格納して検索する

# In[ ]:


get_ipython().run_cell_magic('writefile', 'save_youtube_video_metadata.py', '\n# 動画の情報をMongoDBに格納し検索可能にする\n\nimport os\nimport sys\nfrom apiclient.discovery import build\nfrom pymongo import MongoClient, DESCENDING\n\nYOUTUBE_API_KEY = os.environ[\'YOUTUBE_API_KEY\'] # 環境変数からAPIキーを取得する\n\n\ndef main():\n    """\n    メインの処理\n    """\n    mongo_client = MongoClient(\'localhost\', 27017) # MongoDBのクライアントオブジェクトを作成する\n    collection = mongo_client.youtube.videos # youtubeデータベースのvideosコレクションを取得する\n    collection.delete_many({}) # 既存のすべてのドキュメントを削除しておく\n    \n    # 動画を検索しページ単位でアイテム一覧を保存する\n    for item_per_page in search_videos(\'手芸\'):\n        save_to_mongodb(collection, item_per_page)\n        \n    show_top_videos(collection) # ビュー数の多い動画を表示する\n    \n    \ndef search_videos(query, max_pages=5):\n    """\n    動画を検索してページ単位でlistをyieldする\n    """\n    \n    youtube = build(\'youtube\', \'v3\', developerKey=YOUTUBE_API_KEY) # YouTubeのAPIクライアントを組み立てる\n    \n    # search.listで最初のページを取得するためのリクエストを得る\n    search_request = youtube.search().list(\n        part=\'id\', # search.listでは動画IDだけを取得できればよい\n        q=query,\n        type=\'video\',\n        maxResults = 50, # 1ページあたり最大50件の動画を取得する\n    )\n    \n    # リクエストが有効かつページ数がmax_pages以内の間、繰り返す\n    # ページ数を制限しているのは実行時間が長くなり過ぎないようにするためなので、\n    # 実際にはもっと多くのページを取得してもよい\n    i = 0\n    while search_request and i < max_pages:\n        search_response = search_request.execute() # リクエストを送信する\n        video_ids = [item[\'id\'][\'videoId\'] for item in search_response[\'items\']] # 動画IDのリストを得る\n        \n        # videos.listメソッドで動画の詳細な情報を得る\n        videos_response = youtube.videos().list(\n            part=\'snippet,statistics\',\n            id=\',\'.join(video_ids)\n        ).execute()\n        \n        yield videos_response[\'items\'] # ページに対応するitemsをyieldする\n        \n        # list_next()メソッドで次のページを取得するためのリクエスト(次のページがない場合はNone)を得る\n        search_request = youtube.search().list_next(search_request, search_response)\n        i += 1\n        \n        \ndef save_to_mongodb(collection, items):\n    """\n    MongoDBにアイテムのリストを保存する\n    """\n    # MongoDBに保存する前に、後で使いやすいようにアイテムを書き換える\n    for item in items:\n        item[\'_id\'] = item[\'id\'] # 各アイテムのid属性を_id属性として使う\n        \n        # statisticsに含まれるviewCountプロパティなどの値が文字列になっているので、数値に変換する\n        for key, value in item[\'statistics\'].items():\n            item[\'statistics\'][key] = int(value)\n            \n    result = collection.insert_many(items) # コレクションに挿入する\n    print(\'Inserted {0} documents\'.format(len(result.inserted_ids)), file=sys.stderr)\n    \n    \ndef show_top_videos(collection):\n    """\n    MongoDBのコレクション内でビュー数の上位5件を表示する\n    """\n    for item in collection.find().sort(\'statistics.viewCount\', DESCENDING).limit(5):\n        print(item[\'statistics\'][\'viewCount\'], item[\'snippet\'][\'title\'])\n        \n        \nif __name__ == \'__main__\':\n    main()')


# In[ ]:


get_ipython().system('forego run python save_youtube_video_metadata.py')


# # chapter 5-3 時系列データの活用と収集

# # pandasの基礎知識

# In[ ]:


import pandas as pd

# pandasのデータ構造にはSeriesとDataFrameがある# Seriesは1次元のラベル付きの配列
# In[ ]:


s1 = pd.Series([4, -2, 5]) # Seriesのコストラクターにlistを渡してインスタンスを生成する


# In[ ]:


# インデックスはデフォルトで数値の連番、最終行のdtypeは含まれるデータの型を表す
s1


# In[ ]:


s1.index # index属性でインデックスの配列を取得する


# In[ ]:


list(s1.index) # インデックスの配列は反復可能オブジェクト


# In[ ]:


s1.values # values属性で値の配列を取得する


# In[ ]:


list(s1.values) # 値の配列は反復可能オブジェクト


# In[ ]:


s2 = pd.Series([4, -2, 5], index=['a', 'b', 'c']) # インデックスを指定してシリーズを作成できる


# In[ ]:


s2


# In[ ]:


s2.index


# In[ ]:


s2['a'] # インデックスの値をキーとして、dictのように値を取得できる

# DataFrameは2次元の表形式のデータ
# キーが列ラベル、値が列を表すシリーズの辞書型のオブジェクト
# In[ ]:


df = pd.DataFrame({'math': [78, 64, 53], 'english': [45, 87, 67]}, index=['001', '002', '003'], columns=['math', 'english'])


# In[ ]:


df


# In[ ]:


df['math'] # dictのように[]内にラベル名を指定することで列を笑わすシリーズを取得できる


# In[ ]:


df.english # ラベル名の属性でもシリーズを取得できる


# In[ ]:


df.ix['001'] # ix属性にインデックスのラベルを指定することで行を取得できる


# In[ ]:


df.ix[0] # ix属性に行番号を指定して行を取得することも可能


# In[ ]:


df.english['001'] # 列はシリーズなので添字でセルの値を取得できる


# In[ ]:


# describe()メソッドで個数、平均値、標準偏差、最小値、パーセンタイル、最大値などの統計量を一度に得られる
df.describe()


# # CSVファイルの読み込み(為替データ)

# In[ ]:


# read_csv()関数の第1引数にはファイルパス、URL、ファイルオブジェクトのいずれかを指定できる
# キーワード引数encodingでファイルのエンコーディングを指定できる
pd.read_csv('exchange.csv', encoding='cp932')

# そのままではデータとして扱いづらいので修正する
# In[ ]:


df_exchange = pd.read_csv('exchange.csv', encoding='cp932', header=1, names=['date', 'USD', 'rate'],
                         skipinitialspace=True, index_col=0, parse_dates=True)


# In[ ]:


df_exchange


# In[ ]:


df_exchange.rate[0]


# In[ ]:


# read_csv()関数では型推論によって、例えば列USDや列rateの値はnumpy.float64に変換される
type(df_exchange.rate[0])


# # csvファイルの読み込み(国債金利データ)
# 和暦の文字列をdatetimeオブジェクトに変換する関数parse_japanese_date()を定義する
# In[ ]:


from datetime import datetime


# In[ ]:


def parse_japanese_date(s):
    base_years = {'S': 1925, 'H': 1988} #昭和・平成の0年に相当する年を定義しておく
    era = s[0] # 元号を表すアルファベット1文字を取得
    year, month, day = s[1:].split('.') # 2文字目以降を.()で分割して年月日に分ける
    year = base_years[era] + int(year) # 元号の0年に相当する年と数値に変換した年を足して西暦の年を得る
    return datetime(year, int(month), int(day)) # datetimeオブジェクトを作成する


# In[ ]:


parse_japanese_date('S49.9.24')


# In[ ]:


parse_japanese_date('H27.8.31')


# In[ ]:


# キーワード引数date_parserに関数parse_japanese_dateを指定、na_valuesで「-」と書かれたセルがNaNとみなされるように指定
df_jgbcm = pd.read_csv('jgbcm_all.csv', encoding='cp932', index_col=0, parse_dates=True,
                      date_parser=parse_japanese_date, na_values=['-'], header=1)


# In[ ]:


df_jgbcm


# # Excelファイルの読み込み(有効求人倍率データ)

# In[ ]:


# read_excel関数の引数で不要な行と列をスキップ、西暦の列をインデックスとして使うためにindex_col=0を指定
df_jobs = pd.read_excel('jobs.xls', skiprows=3, skip_footer=2, parse_cols='W,Y:AJ', index_col=0)


# In[ ]:


df_jobs


# In[ ]:


# 縦軸が年、横軸が月になっており月ごとの変動を見るには扱いづらいので、
# データフレームのstack()メソッドで2次元のデータフレームを1次元のシリーズに変換する
s_jobs = df_jobs.stack()


# In[ ]:


s_jobs


# In[ ]:


# このシリーズのインデックスは年と月という階層を持つ階層型インデックス
# このインデックスを反復すると、年と月の2要素からなるタプルが得られる
list(s_jobs.index)

# このままでは扱いづらいので、インデックスを日付に変換するparse_year_and_month()関数を定義する
# In[ ]:


from datetime import datetime


# In[ ]:


def parse_year_and_month(year, month):
    year = int(year[:-1]) # "年"を除去して数値に変換
    month = int(month[:-1]) # "月"を除去して数値に変換
    year += (1900 if year >= 63 else 2000) # 63年以降は19xx年、63年より前は20xx年
    return datetime(year, month, 1) # datetimeオブジェクトを作成する

# Excelファイルでは1〜9月は全角文字になっているがPythonでは問題なくintに変換できる
# In[ ]:


parse_year_and_month('63年', '1月')


# In[ ]:


parse_year_and_month('14年', '12月')


# In[ ]:


# シリーズのindex属性にリストを代入してインデックスを置き換える
s_jobs.index = [parse_year_and_month(y, m) for y, m in s_jobs.index]


# In[ ]:


s_jobs


# # グラフによる可視化

# # matplotlibnの使い方

# In[ ]:


import matplotlib.pyplot as plt


# In[ ]:


# plot()関数にX軸のリストとY軸のリストを指定するとグラフを描画できる
plt.plot([1, 2, 3, 4, 5], [1, 4, 9, 16, 25])


# In[ ]:


plt.show() # show()関数でグラフをウインドウに表示する


# In[ ]:


# 引数にリストを1つだけ指定した場合、そのリストはY軸の値として使用され、X軸の値はリストのインデックスの値となる
plt.plot([1, 2, 3, 4, 5])


# In[ ]:


plt.show()


# # 様々なパラメーターを指定してグラフを描画、ファイルに出力する
# P.168 P.169, macOS Sierraのフォント指定
# macOS Sierraでは，matplotlibから使用できる.ttf形式の日本語フォントファイルがなくなってしまったため，
# 以下の手順でMigMix 1Pフォントをインストールしてください。

# http://mix-mplus-ipa.osdn.jp/migmix/ から migmix-1p-20150712.zip をダウンロード・展開する。
# ZIPファイルに含まれているmigmix-1p-regular.ttfを~/Library/Fontsにコピーする。
# 以下のコマンドでmatplotlibのフォントのキャッシュファイルを削除する。
# ※ P.166 脚注39のパスはLinuxのもので，macOSでは異なるので注意してください。

# rm ~/.matplotlib/fontList.py3k.cache
# In[ ]:


get_ipython().run_cell_magic('writefile', 'plot_advanced_graph_to_file.py', "\n# 様々なパラメーターを指定してグラフを描画、ファイルに出力する\n\nimport matplotlib\nmatplotlib.use('Agg') # 描画のバックエンドとしてデスクトップ環境が不要なAggを使う\n# 日本語を描画できるようフォントを指定する\n# デフォルトでは英語用のフォントが指定され、日本語が表示できない\n# OS XとUbuntu用に2種類のフォントを列挙している\nmatplotlib.rcParams['font.sans-serif'] = 'Hiragino Kaku Gothic Pro, MigMix 1P'\nimport matplotlib.pyplot as plt\n\n# plot()の第3引数には系列のスタイルを表す文字列を指定できる\n# 'b'は青色、’x’はバツ印のマーカー、'-'はマーカーを実線で繋ぐことを意味する\n# キーワード引数labelで指定した系列の名前は、凡例で使用される\nplt.plot([1, 2, 3, 4, 5], [1, 2, 3, 4, 5], 'bx-', label='1次関数')\n# スタイルの'r'は赤色、'o'は丸印のマーカー、'--'は点線を意味する\nplt.plot([1, 2, 3, 4, 5], [1, 4, 9, 16, 25], 'ro--', label='2次関数')\nplt.xlabel('Xの値') # xlabel関数でX軸のラベルを指定する\nplt.ylabel('Yの値') # ylabel関数でY軸のラベルを指定する\nplt.title('matplotlibのサンプル') # title()関数でグラフのタイトルを指定する\nplt.legend(loc='best') # legend関数で判例を表示する。loc='best'は最適な位置に表示することを意味する\nplt.xlim(0, 6) # X軸の値の範囲を0〜6とする。ylim()関数で同様にY軸の範囲を指定できる\nplt.savefig('advanced_graph.png', dpi=300) # グラフを画像ファイルに保存する")


# In[ ]:


get_ipython().system('python plot_advanced_graph_to_file.py')


# # 読み込んだデータをグラフとして描画

# # 時系列データを可視化する

# In[ ]:


get_ipython().run_cell_magic('writefile', 'plot_historical_data.py', '\n# 時系列データを可視化する\n\nfrom datetime import datetime\nimport pandas as pd\nimport matplotlib\nmatplotlib.use(\'Agg\') # 描画のバックエンドとしてデスクトップ環境が不要なAggを使う\n# 日本語を描画できるようフォントを指定する\n# デフォルトでは英語用のフォントが指定され、日本語が表示できない\n# OS XとUbuntu用に2種類のフォントを列挙している\nmatplotlib.rcParams[\'font.sans-serif\'] = \'Hiragino Kaku Gothic Pro, MigMix 1P\'\nimport matplotlib.pyplot as plt\n\n\ndef main():\n    # 為替データの読み込み\n    df_exchange = pd.read_csv(\n        \'exchange.csv\', encoding=\'cp932\', header=1, names=[\'date\', \'USD\', \'rate\'],\n        skipinitialspace=True, index_col=0, parse_dates=True)\n    # 国債金利データの読み込み\n    # キーワード引数date_parserに関数parse_japanese_dateを指定、na_valuesで「-」と書かれたセルがNaNとみなされるように指定\n    df_jgbcm = pd.read_csv(\n        \'jgbcm_all.csv\', encoding=\'cp932\', index_col=0, parse_dates=True,\n        date_parser=parse_japanese_date, na_values=[\'-\'], header=1)\n    # 有効求人倍率の読み込み\n    # read_excel関数の引数で不要な行と列をスキップ、西暦の列をインデックスとして使うためにindex_col=0を指定\n    df_jobs = pd.read_excel(\'jobs.xls\', skiprows=3, skip_footer=2, parse_cols=\'W,Y:AJ\', index_col=0)\n    # 縦軸が年、横軸が月になっており月ごとの変動を見るには扱いづらいので、\n    # データフレームのstack()メソッドで2次元のデータフレームを1次元のシリーズに変換する\n    s_jobs = df_jobs.stack()\n    # シリーズのindex属性にリストを代入してインデックスを置き換える\n    s_jobs.index = [parse_year_and_month(y, m) for y, m in s_jobs.index]\n    \n    min_date = datetime(1973, 1, 1) # X軸の最小値\n    max_date = datetime.now() # X軸の最大値\n    \n    # 1つ目のサブプロット(為替データ)\n    plt.subplot(3, 1, 1) # 3行1列の1番目のサブプロットを作成\n    plt.plot(df_exchange.index, df_exchange.USD, label=\'ドル・円\')\n    plt.xlim(min_date, max_date) # X軸の範囲を指定\n    plt.ylim(50, 350) # Y軸の範囲を指定\n    plt.legend(loc=\'best\') # 凡例を最適な位置に表示\n    # 2つ目のサブプロット(国債金利データ)\n    plt.subplot(3, 1, 2) # 3行1列の2番目のサブプロットを作成\n    plt.plot(df_jgbcm.index, df_jgbcm[\'1年\'], label=\'1年国債金利\')  \n    plt.plot(df_jgbcm.index, df_jgbcm[\'5年\'], label=\'5年国債金利\')  \n    plt.plot(df_jgbcm.index, df_jgbcm[\'10年\'], label=\'10年国債金利\')\n    plt.xlim(min_date, max_date) # X軸の範囲を指定\n    plt.legend(loc=\'best\') # 凡例を最適な位置に表示\n    # 3つ目のサブプロット(有効求人倍率)\n    plt.subplot(3, 1, 3) # 3行1列の3番目のサブプロットを作成\n    plt.plot(s_jobs.index, s_jobs, label=\'有効求人倍率 (季節調整値)\')\n    plt.xlim(min_date, max_date) # X軸の範囲を指定\n    plt.ylim(0.0, 2.0) # Y軸の範囲を指定\n    plt.axhline(y=1, color=\'gray\') # y=1の水平線を引く\n    plt.legend(loc=\'best\') # 凡例を最適な位置に表示\n    \n    plt.savefig(\'historical_data.png\', dpi=300) # 画像を保存\n    \n    \ndef parse_japanese_date(s):\n    """\n    和暦の日付をdatetimeオブジェクトに変換する\n    """\n    base_years = {\'S\': 1925, \'H\': 1988} #昭和・平成の0年に相当する年を定義しておく\n    era = s[0] # 元号を表すアルファベット1文字を取得\n    year, month, day = s[1:].split(\'.\') # 2文字目以降を.()で分割して年月日に分ける\n    year = base_years[era] + int(year) # 元号の0年に相当する年と数値に変換した年を足して西暦の年を得る\n    return datetime(year, int(month), int(day)) # datetimeオブジェクトを作成する\n\n\ndef parse_year_and_month(year, month):\n    """\n    (\'X年\', \'Y月\')の組をdatetimeオブジェクトに変換する\n    """\n    year = int(year[:-1]) # "年"を除去して数値に変換\n    month = int(month[:-1]) # "月"を除去して数値に変換\n    year += (1900 if year >= 63 else 2000) # 63年以降は19xx年、63年より前は20xx年\n    return datetime(year, month, 1) # datetimeオブジェクトを作成する\n\n\nif __name__ == \'__main__\':\n    main()')


# In[ ]:


get_ipython().system('python plot_historical_data.py')

# スクリプトファイルで複雑なグラフをプロットする時には、
# グローバルに1つだけ状態を保持する関数ベースのAPIの性質が扱いづらいこともある
# そのような場合に、matplotlibのオブジェクト指向のAPIを使う例
# 図全体はFigureクラス、サブプロットはAxesクラスとしてモデル化されている
# In[ ]:


# 日本語フォントを指定するにはどうしたらいいのかわからない・・・

import matplotlib
matplotlib.rcParams['font.sans-serif'] = 'Hiragino Kaku Gothic Pro, Osaka, MigMix 1P' # 書籍ではOsakaが抜けておりwebで訂正
import matplotlib.pyplot as plt

min_date = datetime(1973, 1, 1) # X軸の最小値
max_date = datetime.now() # X軸の最大値

fig = plt.figure() # figはFigureクラスのオブジェクト
ax1 = fig.add_subplot(3, 1, 1) # ax1はAxesクラスのオブジェクト
ax1.plot(df_exchange.index, df_exchange.USD, label='ドル・円')
ax1.set_xlim(min_date, max_date) # X軸の範囲を指定
ax1.set_ylim(50, 350) # Y軸の範囲を指定
ax1.legend(loc='best')
fig.savefig('historical_data_OOP.png', dpi=300)


# # chapter 5-4 オープンデータの収集と活用

# # PDFからのデータの抽出
# PDFMiner.sixのPythonインターフェイス
# PDFをパースしてテキストボックスを表示する
# In[ ]:


get_ipython().run_cell_magic('writefile', 'print_pdf_textboxes.py', '\n# PDFをパースしてテキストボックスを表示する\n\nimport sys\nfrom pdfminer.converter import PDFPageAggregator\nfrom pdfminer.layout import LAParams, LTContainer, LTTextBox\nfrom pdfminer.pdfinterp import PDFPageInterpreter, PDFResourceManager\nfrom pdfminer.pdfpage import PDFPage\n\n\ndef find_textboxes_recursively(layout_obj):\n    """\n    再帰的にテキストボックス(LTTextBox)を探して、テキストボックスのリストを取得する\n    """\n    # LTTextBoxを継承するオブジェクトの場合は1要素のリストを返す\n    if isinstance(layout_obj, LTTextBox):\n        return[layout_obj]\n    \n    # LTContainerを継承するオブジェクトは子要素を含むので、再帰的に探す\n    if isinstance(layout_obj, LTContainer):\n        boxes = []\n        for child in layout_obj:\n            boxes.extend(find_textboxes_recursively(child))\n            \n        return(boxes)\n    \n    return [] # その他の場合は空のリストを返す\n\n\nlaparams = LAParams(detect_vertical=True) # Layout Analysisのパラメーターを設定。縦書きの検出を有効にする\nresource_manager = PDFResourceManager() # 共有のリソースを管理するリソースマネージャーを作成\n# ページを集めるPageAggregatorオブジェクトを作成\ndevice = PDFPageAggregator(resource_manager, laparams=laparams)\ninterpreter = PDFPageInterpreter(resource_manager, device) # Interpreterオブジェクトを作成\n\nwith open(sys.argv[1], \'rb\') as f: # ファイルをバイナリ形式で開く\n    # PDFPage.get_pages()にファイルオブジェクトを指定して、PDFPageオブジェクトを順に取得する\n    # 時間がかかるファイルは、キーワード引数pagenosで処理するページ番号(0始まり)のリストを指定するとよい\n    for page in PDFPage.get_pages(f):\n        interpreter.process_page(page) # ページを処理する\n        layout = device.get_result() # LTPageオブジェクトを取得\n        \n        boxes = find_textboxes_recursively(layout) # ページないのテキストボックスのリストを取得する\n        # テキストボックスの左上の座標の順でテキストボックスをソートする\n        # y1(y座標の値)は上に行くほど大きくなるので、正負を反転させている\n        boxes.sort(key=lambda b: (-b.y1, b.x0))\n        \n        for box in boxes:\n            print(\'-\' * 10) # 読みやすいように区切り線を表示する\n            print(box.get_text().strip()) # テキストボックス内のテキストを表示する')


# In[ ]:


get_ipython().system('python print_pdf_textboxes.py /Users/Really/Python_ScrapingBook/000232384.pdf')


# # Linked Open Dataからのデータ収集

# # SPARQLでデータを収集する
# PythonスクリプトからSPARQLクエリを実行する
# SPARQLを使って日本の美術館を取得するスクリプト
# In[ ]:


get_ipython().run_cell_magic('writefile', 'get_museum.py', '\n# SPARQLを使って日本の美術館を取得するスクリプト\n\nfrom SPARQLWrapper import SPARQLWrapper\n\n# SPARQLエンドポイントのURLを指定してインスタンスを作成する\nsparql = SPARQLWrapper(\'http://ja.dbpedia.org/sparql\')\n# 日本の美術館を取得するクエリを設定する。\n# バックスラッシュを含むので、rで始まるraw文字列を使用している\nsparql.setQuery(r\'\'\'\nSELECT * WHERE {\n    ?s rdf:type dbpedia-owl:Museum ;\n        prop-ja:所在地 ?address .\n    FILTER REGEX(?address, "^\\\\p{Han}{2,3}[都道府県]")\n} ORDER BY ?s\n\'\'\')\nsparql.setReturnFormat(\'json\') # 取得するフォーマットとしてJSONを指定する\n# query()でクエリを実行し、convert()でレスポンスをパースしてdictを得る\nresponse = sparql.query().convert()\n\nfor result in response[\'results\'][\'bindings\']:\n    print(result[\'s\'][\'value\'], result[\'address\'][\'value\']) # 抽出した変数の値を表示する')


# # chapter 5-5 Webページの自動操作

# # RoboBrowserでGoogle検索する

# In[ ]:


get_ipython().run_cell_magic('writefile', 'robobrowser_google.py', "\n# RoboBrowserでGoogle検索する\n\nfrom robobrowser import RoboBrowser\n\n# RoboBrowserオブジェクトを作成する\n# キーワード引数parserはBeautifulSoup()の第2引数として扱われる\nbrowser = RoboBrowser(parser='html.parser')\n\nbrowser.open('https://google.co.jp/') # open()メソッドでGoogleのトップページを開く\n\n# 検索語を入力して送信する\nform = browser.get_form(action='/search') # フォーム取得\nform['q'] = 'Python' # フォームのqという名前のフィールドに検索語を入力\nbrowser.submit_form(form, list(form.submit_fields.values())[0]) # 一つ目のボタン(Google検索)を押す\n\n# 検索結果のタイトルとURLを抽出して表示する\n# select()メソッドはBeautiful Soupのselect()メソッドと同じものであり、\n# 引数のCSSセレクターにマッチする要素に対応するTagオブジェクトのリストを取得できる\nfor a in browser.select('h3 > a'):\n    print(a.text)\n    print(a.get('href'))")


# In[ ]:


get_ipython().system('python robobrowser_google.py')


# # Amazon.co.jpの注文履歴を取得する

# In[ ]:


get_ipython().run_cell_magic('writefile', 'amazon_order_history.py', '\n# Amazon.co.jpの注文履歴を取得する\n\nimport sys\nimport os\nfrom robobrowser import RoboBrowser\n\n# 認証の情報は環境変数から取得する\nAMAZON_EMAIL = os.environ[\'AMAZON_EMAIL\']\nAMAZON_PASSWORD = os.environ[\'AMAZON_PASSWORD\']\n\n# RoboBrowserオブジェクトを作成する\nbrowser = RoboBrowser(\n    parser=\'html.parser\', # Beatiful Soupで使用するパーサーを指定\n    # Cookieが使用できないと表示されてログインできない問題を回避するため\n    # 通常のブラウザーのUser-Agent(ここではFirefoxのもの)を使う\n    user_agent=\'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.10; rv:45.0) Gecko/20100101 Firefox/45.0\')\n\n\ndef main():\n    # 注文履歴のページを開く\n    print(\'Navigating...\', file=sys.stderr)\n    browser.open(\'https://www.amazon.co.jp/gp/css/order-history\')\n    \n    # サインインページにリダイレクトされていることを確認する\n    assert \'Amazonサインイン\' in browser.parsed.title.string\n    \n    # name="signIn" というサインインフォームを埋める。\n    # フォームのname属性の値はブラウザーの開発者ツールで確認できる。\n    form = browser.get_form(attrs={\'name\': \'signIn\'})\n    form[\'email\'] = AMAZON_EMAIL\n    form[\'password\'] = AMAZON_PASSWORD\n    \n    # フォームを送信する。正常にログインするにはRefererヘッダーとAccept-Languageヘッダーが必要。\n    print(\'Signing in...\', file=sys.stderr)\n    browser.submit_form(form, headers={\n        \'Referer\': browser.url,\n        \'Accept-Language\': \'ja,en-US;q=0.7,en;q=0.3\',\n    })\n    \n    # ログインに失敗する場合は、次の行のコメントを外してHTMLのソースを確認すると良い。\n    # print(browser.parsed.prettify())\n\n    # ページャーをたどる。\n    while True:\n        assert \'注文履歴\' in browser.parsed.title.string # 注文履歴画面が表示されていることを確認する。\n        \n        print_order_history() # 注文履歴を表示する。\n        \n        link_to_next = browser.get_link(\'次へ\') #「次へ」というテキストを持つリンクを取得する。\n        if not link_to_next:\n            break #「次へ」のリンクがない場合はループを抜けて終了する。\n            \n        print(\'Following link to next page...\', file=sys.stderr)\n        browser.follow_link(link_to_next) # 次へ」というリンクをたどる。\n        \n        \ndef print_order_history():\n    """\n    現在のページのすべての注文履歴を表示する\n    """\n    for line_item in browser.select(\'.order-info\'):\n        order = {} # 注文の情報を格納するためのdict\n        # ページ内のすべての注文履歴について反復する。ブラウザーの開発者ツールでclass属性の値を確認できる\n        # 注文の情報のすべての列について反復する\n        for column in line_item.select(\'.a-column\'):\n            label_element = column.select_one(\'.label\')\n            value_element = column.select_one(\'.value\')\n            # ラベルと値がない列は無視する。\n            if label_element and value_element:\n                label = label_element.get_text().strip()\n                value = value_element.get_text().strip()\n                order[label] = value\n        print(order[\'注文日\'], order[\'合計\']) # 注文の情報を表示する。\n        \n\nif __name__ == \'__main__\':\n    main()')


# In[ ]:


get_ipython().system('forego run python amazon_order_history.py')


# # chapter 5-6 JavaScriptを使ったページのスクレイピング
# !pip install selenium# !brew install phantomjs
# # SeleniumでGoogle検索を行う

# In[ ]:


get_ipython().run_cell_magic('writefile', 'selenium_google.py', "\n# SeleniumでGoogle検索を行う\n\nfrom selenium import webdriver\nfrom selenium.webdriver.common.keys import Keys\n\n# PhantomJSのWebDriverオブジェクトを作成する\ndriver = webdriver.PhantomJS()\n\n# Googleのトップ画面を開く\ndriver.get('https://www.google.co.jp/')\n\n# タイトルに'Google'が含まれていることを確認する\nassert 'Google' in driver.title\n\n# 検索語を入力して送信する\ninput_element = driver.find_element_by_name('q')\ninput_element.send_keys('Python')\ninput_element.send_keys(Keys.RETURN)\n\n# タイトルに'Python'が含まれていることを確認する\nassert 'Python' in driver.title\n\n# スクリーンショットを撮る\ndriver.save_screenshot('search_results.png')\n\n# 検索結果を表示する\nfor a in driver.find_elements_by_css_selector('h3 > a'):\n    print(a.text)\n    print(a.get_attribute('href'))")


# In[ ]:


get_ipython().system('python selenium_google.py')


# # noteのおすすめコンテンツを取得する

# # Seleniumで試行錯誤しながら読み込んでみる

# In[ ]:


from selenium import webdriver


# In[ ]:


driver = webdriver.PhantomJS()


# In[ ]:


driver.get('https://note.mu/')


# In[ ]:


driver.title


# In[ ]:


driver.save_screenshot('note-1.png')

# ウインドウサイズがスマートフォンに最適化されているようなので、
# set_window_size()メソッドで変更する
# In[ ]:


driver.set_window_size(800, 600)


# In[ ]:


driver.save_screenshot('note-2.png')

# 最初の画面からデータを抜き出す
# (ブラウザーの開発者ツールでコンテンツ情報の要素を調査する)
# In[ ]:


driver.find_elements_by_css_selector('a.p-post--basic')

# 最初のコンテンツのボックスに対応するa要素を取得
# In[ ]:


a = driver.find_elements_by_css_selector('a.p-post--basic')[0]

# SeleniumでDOM要素に対応するオブジェクトは、WebElementオブジェクト
# In[ ]:


a

# WebElementオブジェクトのget_attribute()メソッドで属性を取得できる
# In[ ]:


a.get_attribute('href')

# WebDriverクラスと同じようにfind_element_by_css_selector()などのメソッドでこの要素内部の要素を取得できる
# In[ ]:


a.find_element_by_css_selector('h4').text # タイトルを取得


# In[ ]:


a.find_element_by_css_selector('.c-post__description').text # 概要を取得

# 問題なく取得できているようならスクリプト化する
# # noteのコンテンツを取得する

# In[ ]:


get_ipython().run_cell_magic('writefile', 'get_note_contents.py', '\n# noteのコンテンツを取得する (Ajax通信完了待機対応版)\n\nimport sys\nimport time # ← 追加\nfrom selenium import webdriver\n\n\ndef main():\n    """\n    メインの処理\n    """\n    \n    driver = webdriver.PhantomJS() # PhantomJSのWebDriverオブジェクトを作成する\n    driver.set_window_size(800, 600) # ウインドウサイズを設定する\n    \n    navigate(driver) # noteのトップページに遷移する\n    posts = scrape_posts(driver) # 文章コンテンツのリストを取得する\n    \n    # コンテンツの情報を表示する\n    for post in posts:\n        print(post)\n        \n        \ndef navigate(driver):\n    """\n    目的のページに遷移する\n    """\n    \n    print(\'Navigating...\', file=sys.stderr)\n    driver.get(\'https://note.mu/\') # noteのトップページを開く\n    assert \'note\' in driver.title # タイトルに\'note\'が含まれていることを確認する\n    time.sleep(2)  # 2秒間待つ。 ← この行を追加\n    \n    \ndef scrape_posts(driver):\n    """\n    文章コンテンツのURL、タイトル、概要を含むdictのリストを取得する\n    """\n    \n    posts = []\n    \n    # すべての文章コンテンツを表すa要素について反復する\n    for a in driver.find_elements_by_css_selector(\'a.p-post--basic\'):\n        # URL、タイトル、概要を取得して、dictとしてリストに追加する\n        posts.append({\n            \'url\': a.get_attribute(\'href\'),\n            \'title\': a.find_element_by_css_selector(\'h4\').text,\n            \'description\': a.find_element_by_css_selector(\'.c-post__description\').text,\n        })\n        \n    return posts\n\n\nif __name__ == \'__main__\':\n    main()    ')


# In[ ]:


get_ipython().system('python get_note_contents.py')


# # おすすめノートのページから続きを読み込む処理

# In[ ]:


get_ipython().run_cell_magic('writefile', 'get_more_note_contents.py', '\n# notenのおすすめノートのページから続きを読み込む処理を追加\n\nimport sys\nimport time # ← 追加\nfrom selenium import webdriver\nfrom selenium.webdriver.common.by import By\nfrom selenium.webdriver.support import expected_conditions as EC\nfrom selenium.webdriver.support.ui import WebDriverWait\n\n\ndef main():\n    """\n    メインの処理\n    """\n    \n    driver = webdriver.PhantomJS() # PhantomJSのWebDriverオブジェクトを作成する\n    driver.set_window_size(800, 600) # ウインドウサイズを設定する\n    \n    navigate(driver) # noteのトップページに遷移する\n    posts = scrape_posts(driver) # 文章コンテンツのリストを取得する\n    \n    # コンテンツの情報を表示する\n    for post in posts:\n        print(post)\n        \n        \ndef navigate(driver):\n    """\n    目的のページに遷移して続きのコンテンツを読み込む\n    """\n    \n    print(\'Navigating...\', file=sys.stderr)\n    driver.get(\'https://note.mu/\') # noteのトップページを開く\n    assert \'note\' in driver.title # タイトルに\'note\'が含まれていることを確認する\n    time.sleep(2)  # 2秒間待つ ← この行を追加\n    \n    # ページの一番下までスクロールする\n    driver.execute_script(\'scroll(0, document.body.scrollHeight)\')\n    \n    print(\'Waiting for contents to be loaded...\', file=sys.stderr)\n    time.sleep(2)  # 2秒間待つ\n    \n    # ページの一番下までスクロールする\n    driver.execute_script(\'scroll(0, document.body.scrollHeight)\')\n    \n    # 10秒でタイムアウトするWebDriverWaitオブジェクトを作成する\n    wait = WebDriverWait(driver, 10)\n    \n    print(\'Waiting for the more button to be clickable...\', file=sys.stderr)\n    # もっとみるボタンがクリック可能になるまで待つ\n    button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, \'.btn-more\')))\n    \n    button.click() # もっとみるボタンをクリックする\n    \n    print(\'Waiting for contents to be loaded...\', file=sys.stderr)\n    time.sleep(2)  # 2秒間待つ\n    \n\ndef scrape_posts(driver):\n    """\n    文章コンテンツのURL、タイトル、概要を含むdictのリストを取得する\n    """\n    \n    posts = []\n    \n    # すべての文章コンテンツを表すa要素について反復する\n    for a in driver.find_elements_by_css_selector(\'a.p-post--basic\'):\n        # URL、タイトル、概要を取得して、dictとしてリストに追加する\n        posts.append({\n            \'url\': a.get_attribute(\'href\'),\n            \'title\': a.find_element_by_css_selector(\'h4\').text,\n            \'description\': a.find_element_by_css_selector(\'.c-post__description\').text,\n        })\n        \n    return posts\n\n\nif __name__ == \'__main__\':\n    main()    ')


# In[ ]:


get_ipython().system('python get_more_note_contents.py')


# # おすすめノートのページからRSSフィードを作成する

# In[ ]:


get_ipython().run_cell_magic('writefile', 'note_rss.py', '\n# おすすめノートのページからRSSフィードを作成する\n# カレントディレクトリにrecommend.rss(RSS2.0に従ったXML)が生成される\n\nimport sys\nimport time # ← 追加\nfrom selenium import webdriver\nfrom selenium.webdriver.common.by import By\nfrom selenium.webdriver.support import expected_conditions as EC\nfrom selenium.webdriver.support.ui import WebDriverWait\nimport feedgenerator\n\n\ndef main():\n    """\n    メインの処理\n    """\n    \n    driver = webdriver.PhantomJS() # PhantomJSのWebDriverオブジェクトを作成する\n    driver.set_window_size(800, 600) # ウインドウサイズを設定する\n    \n    navigate(driver) # noteのトップページに遷移する\n    posts = scrape_posts(driver) # 文章コンテンツのリストを取得する\n    \n    # RSSフィードとして保存する\n    with open(\'recommend.rss\', \'w\') as f:\n        save_as_feed(f, posts)\n        \n        \ndef navigate(driver):\n    """\n    目的のページに遷移して続きのコンテンツを読み込む\n    """\n    \n    print(\'Navigating...\', file=sys.stderr)\n    driver.get(\'https://note.mu/\') # noteのトップページを開く\n    assert \'note\' in driver.title # タイトルに\'note\'が含まれていることを確認する\n    time.sleep(2)  # 2秒間待つ ← この行を追加\n    \n    # ページの一番下までスクロールする\n    driver.execute_script(\'scroll(0, document.body.scrollHeight)\')\n    \n    print(\'Waiting for contents to be loaded...\', file=sys.stderr)\n    time.sleep(2)  # 2秒間待つ\n    \n    # ページの一番下までスクロールする\n    driver.execute_script(\'scroll(0, document.body.scrollHeight)\')\n    \n    # 10秒でタイムアウトするWebDriverWaitオブジェクトを作成する\n    wait = WebDriverWait(driver, 10)\n    \n    print(\'Waiting for the more button to be clickable...\', file=sys.stderr)\n    # もっとみるボタンがクリック可能になるまで待つ\n    button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, \'.btn-more\')))\n    \n    button.click() # もっとみるボタンをクリックする\n    \n    print(\'Waiting for contents to be loaded...\', file=sys.stderr)\n    time.sleep(2)  # 2秒間待つ\n    \n\ndef scrape_posts(driver):\n    """\n    文章コンテンツのURL、タイトル、概要を含むdictのリストを取得する\n    """\n    \n    posts = []\n    \n    # すべての文章コンテンツを表すa要素について反復する\n    for a in driver.find_elements_by_css_selector(\'a.p-post--basic\'):\n        # URL、タイトル、概要を取得して、dictとしてリストに追加する\n        posts.append({\n            \'url\': a.get_attribute(\'href\'),\n            \'title\': a.find_element_by_css_selector(\'h4\').text,\n            \'description\': a.find_element_by_css_selector(\'.c-post__description\').text,\n        })\n        \n    return posts\n\n\ndef save_as_feed(f, posts):\n    """\n    文章コンテンツのリストをフィードとして保存する\n    """\n    \n    # フィードを表すRss201rev2Feedオブジェクトを作成する\n    feed = feedgenerator.Rss201rev2Feed(\n        title=\'おすすめノート\', # フィードのタイトル\n        link=\'https://note.mu/\',  # \u3000フィードに対応するwebサイトのURL\n        description=\'おすすめノート\') # フィードの概要\n    \n    for post in posts:\n        # フィードにアイテムを追加する\n        # キーワード引数unique_idは、アイテムを一意に識別するユニークなIDを指定する\n        # 必須ではないが、このIDを指定しておくとRSSリーダーがアイテムの重複なく扱える\n        # 可能性が高まるので、ここではコンテンツのURLを指定している\n        feed.add_item(title=post[\'title\'], link=post[\'url\'],\n                     description=post[\'description\'], unique_id=post[\'url\'])\n        \n    feed.write(f, \'utf-8\') # ファイルオブジェクトに書き込む。第2引数にエンコーディングを指定する\n    \n\nif __name__ == \'__main__\':\n    main()    ')


# In[ ]:


get_ipython().system('python note_rss.py')

# ファイルを生成したディレクトリでHTTPサーバーを起動する
# In[ ]:


# !python -m http.server

# ブラウザーで http://localhost:8000/recommend.rss にアクセスすると
# RSSリーダーに登録するための画面が表示される
# # chapter 5-7 取得したデータの活用

# # ジオコーディングによる位置情報の取得
# ジオコーディングAPIを使用して住所から位置情報を取得することができる
# ここでは使用目的の制限が少ないYahoo!のものを使用する
# 常時SSL（AOSSL）対応にともないリクエストURLが書籍記載のものから変更されている
# デフォルトはXMLだが、PythonではJSON形式の方が扱いやすいので、output=jsonとしている
# In[ ]:


# jqコマンドはJSONに対してクエリを実行して一部を抽出できるコマンド
# jq . を実行すると標準入力に与えたJSON文字列が整形して表示される
# brew install jq

# 「\」(バックスラッシュ)は改行記号
# In[ ]:


# jq . あり
get_ipython().system("curl -s 'https://map.yahooapis.jp/geocode/V1/geoCoder?appid=dj00aiZpPTgxQUZmbUZBcWx2TCZzPWNvbnN1bWVyc2VjcmV0Jng9ZjE-&output=json&query=東京都台東区上野公園7番7号' | jq .")


# In[ ]:


# jq . なし
get_ipython().system("curl -s 'https://map.yahooapis.jp/geocode/V1/geoCoder?appid=dj00aiZpPTgxQUZmbUZBcWx2TCZzPWNvbnN1bWVyc2VjcmV0Jng9ZjE-&output=json&query=東京都台東区上野公園7番7号'")

# jqの引数に「.」以外のフィルターを記述してJSONの一部だけを抽出することもできる
# In[ ]:


# 結果の数だけを抽出する
get_ipython().system("curl -s 'https://map.yahooapis.jp/geocode/V1/geoCoder?appid=dj00aiZpPTgxQUZmbUZBcWx2TCZzPWNvbnN1bWVyc2VjcmV0Jng9ZjE-&output=json&query=東京都台東区上野公園7番7号' | jq .ResultInfo.Count")


# In[ ]:


# 結果と緯度だけを抽出する
get_ipython().system("curl -s 'https://map.yahooapis.jp/geocode/V1/geoCoder?appid=dj00aiZpPTgxQUZmbUZBcWx2TCZzPWNvbnN1bWVyc2VjcmV0Jng9ZjE-&output=json&query=東京都台東区上野公園7番7号' | jq .Feature[0].Geometry.Coordinates")


# # code 5.27 SPARQLとジオコーダAPIを使って日本の美術館の位置情報を取得する

# In[ ]:


get_ipython().run_cell_magic('writefile', 'get_museum_with_location.py', '\n# 日本の美術館の位置情報を取得する\n\nimport sys\nimport os\nimport json\nimport dbm\nfrom urllib.request import urlopen\nfrom urllib.parse import urlencode\nfrom SPARQLWrapper import SPARQLWrapper\n\n\ndef main():\n    features = [] # 美術館の情報を格納するためのリスト\n    \n    for museum in get_museums():\n        # ラベルがある場合はラベルを、ない場合はsの値を取得\n        label = museum.get(\'label\', museum[\'s\'])\n        address = museum[\'address\']\n        \n        if \'lon_degree\' in museum:\n            # 位置情報が含まれている場合は、経度と緯度を60度数(度分秒)から10進数に変換する\n            # 10進数の度 = 60進数の度 + 60進数の分 / 60 + 60進数の秒 / 3600\n            lon = float(museum[\'lon_degree\']) + float(museum[\'lon_minute\']) / 60 + \\\n                float(museum[\'lon_second\']) / 3600\n            lat = float(museum[\'lat_degree\']) + float(museum[\'lat_minute\']) / 60 + \\\n                float(museum[\'lat_second\']) / 3600\n                \n        else:\n            # 位置情報が含まれない場合は、住所をジオコーディングして経度と緯度を取得する\n            lon, lat = geocode(address)\n            \n        print(label, address, lon, lat) # 変数の値を表示\n        \n        # ジオコーディングしても位置情報を取得できなかった場合はfeaturesに含めない\n        if lon is None:\n            continue\n            \n        # featuresに美術館の情報をGeoJSONのFeatureの形式で追加する\n        features.append({\n            \'type\': \'Feature\',\n            \'geometry\': {\'type\': \'Point\', \'coordinates\': [lon, lat]},\n            \'properties\': {\'label\': label, \'address\': address},\n        })\n    \n    # GeoJSONのFeatureCollectionの形式でdictを作成する\n    feature_collection = {\n        \'type\': \'FeatureCollection\',\n        \'features\': features,\n    }\n    # FeatureCollectionを.geojsonという拡張子のファイルに書き出す\n    # GeoJSON対応ソフトウェアで表示できる\n    # GitHubやGistのプレビューでは操作可能な地図上に表示される\n    with open(\'museums.geojson\', \'w\') as f:\n        json.dump(feature_collection, f)\n    \n    \ndef get_museums():\n    """\n    SPARQLを使ってDBPedia Japaneseから美術館の情報を取得する\n    """\n    \n    print(\'Executing SPARQL query...\', file=sys.stderr)\n    \n    # SPARQLエンドポイントのURLを指定してインスタンスを作成する\n    sparql = SPARQLWrapper(\'http://ja.dbpedia.org/sparql\')\n    # 日本の美術館を取得するクエリを設定する。\n    # バックスラッシュを含むので、rで始まるraw文字列を使用している\n    sparql.setQuery(r\'\'\'\n    SELECT * WHERE {\n        ?s rdf:type dbpedia-owl:Museum ;\n        prop-ja:所在地 ?address .\n        OPTIONAL { ?s rdfs:label ?label . }\n        OPTIONAL {\n        ?s prop-ja:経度度 ?lon_degree ;\n            prop-ja:経度分 ?lon_minute ;\n            prop-ja:経度秒 ?lon_second ;\n            prop-ja:緯度度 ?lat_degree ;\n            prop-ja:緯度分 ?lat_minute ;\n            prop-ja:緯度秒 ?lat_second .\n        }\n        FILTER REGEX(?address, "^\\\\p{Han}{2,3}[都道府県]")\n    } ORDER BY ?s\n    \'\'\')\n    # 取得するフォーマットとしてJSONを指定する\n    sparql.setReturnFormat(\'json\')\n    # query()でクエリを実行し、convert()でレスポンスをパースしてdictを得る\n    response = sparql.query().convert()\n    \n    print(\'Got {0} results\'.format(len(response[\'results\'][\'bindings\']), file=sys.stderr))\n    \n    # クエリの実行結果を反復処理する\n    for result in response[\'results\'][\'bindings\']:\n        # 扱いやすいように{変数名1: 値1, 変数名2: 値2, ...}という形式のdictをyieldする\n        # resultを加工した辞書を得るために、辞書内包表記というリスト内包表記に似た表記法を使う\n        yield {name: binding[\'value\'] for name, binding in result.items()}\n        \n        \n# Yahoo!ジオコーダAPIのURL\nYAHOO_GEOCODER_API_URL = \'https://map.yahooapis.jp/geocode/V1/geoCoder\'\n# DBM(ファイルを使ったキーバリュー型のDB)をジオコーディング結果のキャッシュとして使用する\n# この変数はdictと同じように扱える\ngeocoding_cache = dbm.open(\'geocoding.db\', \'c\')\n\n\ndef geocode(address):\n    """\n    引数で指定した住所をジオコーディングして、経度と緯度のペアを返す\n    """\n    \n    if address not in geocoding_cache:\n        # 住所がキャッシュに存在しない場合はYahoo!ジオコーダAPIでジオコーディングする\n        print(\'Geocoding {0}...\'.format(address), file=sys.stderr)\n        url = YAHOO_GEOCODER_API_URL + \'?\' + urlencode({\n            # アプリケーションIDは環境変数から取得する\n            \'appid\': os.environ[\'YAHOOJAPAN_APP_ID\'],\n            \'output\': \'json\',\n            \'query\': address,\n        })\n        \n        response_text = urlopen(url).read()\n        # APIのレスポンスをキャッシュに格納する\n        # キーや値にはbytes型しか使えないが、str型は自動的にbytes型に変換される\n        geocoding_cache[address] = response_text\n        \n    # キャッシュ内のAPIレスポンスをdictに変換\n    # 値はbytes型なので、文字列として扱うにはデコードが必要\n    response = json.loads(geocoding_cache[address].decode(\'utf-8\'))\n    \n    if \'Feature\' not in response:\n        # ジオコーディングで結果が得られなかった場合はNoneのペアを返す\n        return (None, None)\n    \n    # Coordinateというキーの値を , で分割\n    coordinates = response[\'Feature\'][0][\'Geometry\'][\'Coordinates\'].split(\',\')\n    # floatnのペアに変換して返す\n    return (float(coordinates[0]), float(coordinates[1]))\n\n\nif __name__ == \'__main__\':\n    main()')


# In[ ]:


get_ipython().system('forego run python get_museum_with_location.py')


# # Google Maps JavaScript APIを使った地図による可視化
# 地図はちょっともうおなかいっぱいなので写経せず。。
# # BigQueryによる解析

# In[ ]:


# !pip install bigquery-python


# # code 5.29 TwitterのデータをBigQueryにインポートする

# In[ ]:


get_ipython().run_cell_magic('writefile', 'import_from_stream_api_to_bigquery.py', '\n# TwitterのデータをBigQueryにインポートする\n\nimport os\nimport sys\nfrom datetime import timezone\nimport tweepy\nimport bigquery\n\n# 環境変数からTwitterの認証情報を取得する\nCONSUMER_KEY = os.environ[\'CONSUMER_KEY\']\nCONSUMER_SECRET = os.environ[\'CONSUMER_SECRET\']\nACCESS_TOKEN = os.environ[\'ACCESS_TOKEN\']\nACCESS_TOKEN_SECRET = os.environ[\'ACCESS_TOKEN_SECRET\']\n\n# Twitterの認証情報を設定する\nauth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)\nauth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)\n\n# BigQueryの認証情報(credentials.json)を指定してBigQueryのクライアントを作成する\n# 明示的にreadonly=Falseとしないと書き込みができない\nclient = bigquery.get_client(json_key_file=\'credentials.json\', readonly=False)\n\nDATASET_NAME = \'twitter\' # BigQueryのデータセット名\nTABLE_NAME = \'tweets\' # BigQueryのテーブル名\n\n# 書籍ではデータセットが存在しなくてもcreate_table()できるように書かれているが、\n# 先にデータセットを作成しなければcreate_table()できなかった。仕様変更?\n\n# データセットが存在しない場合は作成する\nif not client.check_dataset(DATASET_NAME):\n    print(\'Creating dataset {0}\'.format(DATASET_NAME), file=sys.stderr)\n    client.create_dataset(DATASET_NAME)\n    \n# テーブルが存在しない場合は作成する\nif not client.check_table(DATASET_NAME, TABLE_NAME):\n    print(\'Creating table {0}.{1}\'.format(DATASET_NAME, TABLE_NAME), file=sys.stderr)\n    # create_table()の第3引数にはスキーマを指定する\n    client.create_table(DATASET_NAME, TABLE_NAME, [\n        {\'name\': \'id\',                    \'type\': \'string\',         \'description\': \'ツイートのID\'},\n        {\'name\': \'lang\',                \'type\': \'string\',         \'description\': \'ツイートの言語\'},\n        {\'name\': \'screen_name\', \'type\': \'string\',         \'description\': \'ユーザー名\'},\n        {\'name\': \'text\',                 \'type\': \'string\',         \'description\': \'ツイートの本文\'},\n        {\'name\': \'created_at\',      \'type\': \'timestamp\', \'description\': \'ツイートの日時\'},\n    ])\n\n\nclass MyStreamListener(tweepy.streaming.StreamListener):\n    """\n    Streaming APIで取得したツイートを処理するためのクラス\n    """\n    \n    status_list = []\n    num_imported = 0\n    \n    def on_status(self, status):\n        """\n        ツイートを受信した時に呼び出されるメソッド\n        引数はツイートを表すStatusオブジェクト\n        """\n        self.status_list.append(status) # Statusオブジェクトをstatus_listに追加する\n        \n        if len(self.status_list) >= 500:\n            # status_listに500件溜まったらBigQueryにインポートする\n            if not push_to_bigquery(self.status_list):\n                # インポートに失敗した場合はFalseが帰ってくるのでエラーを出して終了する\n                print(\'Failed to send to bigquery\', file=sys.stderr)\n                return False\n            \n            # num_importedを増やして、status_listを空にする\n            self.num_imported += len(self.status_list)\n            self.status_list = []\n            print(\'Imported {0} rows\'.format(self.num_imported), file=sys.stderr)\n            \n            # 料金が高額にならないように、5000件をインポートしたらFalseを返して終了する\n            # 継続的にインポートしたいときは次の2行をコメントアウトする\n            if self.num_imported >= 5000:\n                return False\n            \n            \ndef push_to_bigquery(status_list):\n    """\n    ツイートのリストをBigQueryにインポートする\n    """\n    \n    # TweepyのStatusオブジェクトからdictのリストに変換する\n    rows = []\n    for status in status_list:\n        rows.append({\n            \'id\': status.id_str,\n            \'lang\': status.lang,\n            \'screen_name\': status.author.screen_name,\n            \'text\': status.text,\n            # datetimeオブジェクトをUTCのPOSIXタイムスタンプに変換する\n            \'created_at\': status.created_at.replace(tzinfo=timezone.utc).timestamp(),\n        })\n        \n    # dictのリストをBigQueryにインポートする\n    # 引数は順に、データセット名、テーブル名、行のリスト、行を一意に識別する列名を表す\n    # insert_id_keyはエラーでリトライしたときに重複しないようにするために使われるが、必須ではない\n    return client.push_rows(DATASET_NAME, TABLE_NAME, rows, insert_id_key=\'id\')\n\n\n# Stream APIの読み込みを開始する\nprint(\'Collecting tweets...\', file=sys.stderr)\nstream = tweepy.Stream(auth, MyStreamListener())\n# 公開されているツイートをサンプリングしたストリームを受信する\n# 言語を指定していないので、あらゆる言語のツイートを取得できる\nstream.sample()\n# キーワード引数languagesで日本語のツイートのみに絞り込む\n# stream.sample(languages=[\'ja\'])')


# In[ ]:


get_ipython().system('forego run python import_from_stream_api_to_bigquery.py')


# # Twitterのデータをクエリする

# In[ ]:


# 言語ごとのツイート数の集計
# BigQuery

SELECT lang, COUNT(*) AS count
FROM twitter.tweets
GROUP BY lang
ORDER BY count DESC
LIMIT 20


# In[ ]:


# 日本語ツイートの文字数の分布
# BigQuery

SELECT INTEGER(ROUND(LENGTH(text), -1)) AS length, COUNT(*) AS count
FROM twitter.tweets
WHERE lang = 'ja'
GROUP BY length
ORDER BY length DESC

