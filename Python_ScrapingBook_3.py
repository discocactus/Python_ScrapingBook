
# coding: utf-8

# In[ ]:


# chapter 3-2 webページを簡単に取得する


# In[ ]:


import requests


# In[ ]:


r = requests.get('https://gihyo.jp/dp')
# webページを取得


# In[ ]:


type(r)
# get関数の戻り値はレスポンス型


# In[ ]:


r.status_code
# HTTPステータスコードを取得


# In[ ]:


r.headers['content-type']
# HTTPヘッダーの辞書を取得


# In[ ]:


r.encoding
# HTTPヘッダーから得られたエンコーディングを取得


# In[ ]:


r.text
# str型にデコードしたレスポンスボディを取得


# In[ ]:


r.content
# bytes型のレスポンスボディを取得


# In[ ]:


r = requests.get('http://weather.livedoor.com/forecast/webservice/json/v1?city=130010')
# 東京の天気をjson形式で取得


# In[ ]:


r.json()


# In[ ]:


r = requests.post('http://httpbin.org/post', data={'key1': 'value1'})
# POSTメソッドで送信


# In[ ]:


r = requests.get('http://httpbin.org/get',
                headers={'user-agent': 'my-crawler/1.0 (+foo@example.com)'})
# キーワード引数headersにdictで指定してリクエストにHTTPヘッダーを追加


# In[ ]:


r = requests.get('https://api.github.com/user',
                auth=('discocactus', '<password>'))
# Basic認証のユーザー名とパスワードの組をキーワード引数authで指定


# In[ ]:


r = requests.get('http://httpbin.org/get', params={'key1': 'value1'})
# URLのパラメーターは引数paramsで指定することも可能


# In[ ]:


# 複数のページを連続してクロールする場合は、Sessionオブジェクトを使うのが効果的


# In[ ]:


s = requests.Session()


# In[ ]:


s.headers.update({'user-agent': 'my-crawler/1.0 (+foo@example.com)'})
# HTTPヘッダーを複数のリクエストで使い回す


# In[ ]:


r = s.get('https://gihyo.jp/')
# Sessionオブジェクトでもrequestsの様にget(), post()などのメソッドが使える


# In[ ]:


r = s.get('https://gihyo.jp/dp')


# In[ ]:


# chapter 3-3 HTMLのスクレイピング


# In[ ]:


# lxmlによるスクレイピング


# In[ ]:


import lxml.html


# In[ ]:


tree = lxml.html.parse('index.html')
# parse()関数でファイルパスを指定してパース
# URLを指定することも可能だが細かい指定ができない


# In[ ]:


from urllib.request import urlopen


# In[ ]:


tree = lxml.html.parse(urlopen('http://example.com/'))
# ファイルオブジェクトを指定してパースすることも可能


# In[ ]:


type(tree)


# In[ ]:


html = tree.getroot()


# In[ ]:


type(html)


# In[ ]:


# fromstring()関数で文字列(strまたはbytes)をパースできる
# ただし、encodingが指定されたXML宣言を含むstrをパースすると、ValueErrorが発生するので注意


# In[ ]:


html = lxml.html.fromstring('''
    <html>
    <head><title>八百屋オンライン</title></head>
    <body>
    <h1 id="main">今日のくだもの</h1>
    <ul>
        <li>りんご</li>
        <li class="featured">みかん</li>
        <li>ぶどう</li>
    </ul>
    </body>
    </html>''')


# In[ ]:


type(html)


# In[ ]:


html.xpath('//li')
# XPathにマッチする要素のリストを取得


# In[ ]:


html.cssselect('li')
# CSSセレクターにマッチする要素のリストを取得


# In[ ]:


h1 = html.xpath('//h1')[0]


# In[ ]:


h1.tag
# タグの名前


# In[ ]:


h1.text
# 要素のテキスト


# In[ ]:


h1.get('id')
# 属性の値


# In[ ]:


h1.attrib
# 全属性を表すdict-likeなオブジェクト


# In[ ]:


h1.getparent()
# 親要素


# In[ ]:


get_ipython().run_cell_magic('writefile', 'scrape_by_lxml.py', "\nimport lxml.html\n\n# HTMLファイルを読み込みgetroot()メソッドでHtmlElementオブジェクトを得る\ntree = lxml.html.parse('index.html')\nhtml = tree.getroot()\n\n# cssselect()メソッドでa要素のリストを取得して、個々のa要素に対して処理を行う\nfor a in html.cssselect('a'):\n    # href属性とリンクのテキストを取得して表示する\n    print(a.get('href'), a.text)")


# In[ ]:


get_ipython().system('python scrape_by_lxml.py')


# In[ ]:


# Beautiful Soupによるスクレイピング


# In[ ]:


from bs4 import BeautifulSoup


# In[ ]:


with open('index.html') as f:
    soup = BeautifulSoup(f, 'html.parser')
# 第1引数にファイルオブジェクトを指定してBeautifulSoupオブジェクトを生成
# BeautifulSoupにはファイル名やURLを指定することはできない
# 第2引数にパーサーを指定する


# In[ ]:


# BeautifulSoupのコンストラクターにはHTMLの文字列を渡すことも可能
soup = BeautifulSoup('''
    <html>
    <head><title>八百屋オンライン</title></head>
    <body>
    <h1 id="main">今日のくだもの</h1>
    <ul>
        <li>りんご</li>
        <li class="featured">みかん</li>
        <li>ぶどう</li>
    </ul>
    </body>
    </html>''', 'html.parser')


# In[ ]:


soup.h1


# In[ ]:


type(soup.h1)


# In[ ]:


soup.h1.name


# In[ ]:


soup.h1.string


# In[ ]:


type(soup.h1.string)


# In[ ]:


soup.ul.text


# In[ ]:


type(soup.h1.text)


# In[ ]:


soup.h1['id']


# In[ ]:


soup.h1.get('id')


# In[ ]:


soup.h1.attrs


# In[ ]:


soup.h1.parent


# In[ ]:


soup.li
# 複数の要素がある場合は先頭の要素が取得される


# In[ ]:


soup.find('li')


# In[ ]:


soup.find_all('li')
# find_all()メソッドで指定した名前の要素のリストを取得


# In[ ]:


soup.find_all('li', class_='featured')
# キーワード引数でclassなどの属性を指定できる
# classは予約語なのでclass_を使うことに注意


# In[ ]:


soup.find_all(id='main')


# In[ ]:


soup.find_all('li', class_='featured')


# In[ ]:


soup.find_all(id='main')
# タグ名を省略して属性のみで探すことも可能


# In[ ]:


soup.select('li')
# select()メソッドでCSSセレクターにマッチする要素を取得


# In[ ]:


soup.select('li.featured')


# In[ ]:


soup.select('#main')


# In[ ]:


get_ipython().run_cell_magic('writefile', 'scrape_by_bs4.py', "\nfrom bs4 import BeautifulSoup\n\nwith open('index.html') as f:\n    soup = BeautifulSoup(f, 'html.parser')\n\nfor a in soup.find_all('a'):\n    print(a.get('href'), a.text)")


# In[ ]:


get_ipython().system('python scrape_by_bs4.py')


# In[ ]:


# pyqueryによるスクレイピング


# In[ ]:


from pyquery import PyQuery as pq


# In[ ]:


d = pq(filename='index.html')


# In[ ]:


d = pq(url='http://example.com/')


# In[ ]:


d = pq('''
    <html>
    <head><title>八百屋オンライン</title></head>
    <body>
    <h1 id="main">今日のくだもの</h1>
    <ul>
        <li>りんご</li>
        <li class="featured">みかん</li>
        <li>ぶどう</li>
    </ul>
    </body>
    </html>''')


# In[ ]:


d('h1')


# In[ ]:


type(d('h1'))


# In[ ]:


d('h1')[0]


# In[ ]:


d('h1').text()


# In[ ]:


d('h1').attr('id')


# In[ ]:


d('h1').attr.id


# In[ ]:


d('h1').attr['id']


# In[ ]:


d('h1').parent()


# In[ ]:


d('li')


# In[ ]:


d('li.featured')


# In[ ]:


d('#main')


# In[ ]:


d('body').find('li')


# In[ ]:


d('li').filter('.featured')


# In[ ]:


d('li').eq(1)


# In[ ]:


# RSSのスクレイピング


# In[ ]:


import feedparser


# In[ ]:


d = feedparser.parse('http://b.hatena.ne.jp/hotentry/it.rss')
# parse()関数にURLを指定してパースできる


# In[ ]:


# d = feedparser.parse('it.rss')
# parse()関数にはファイルパス、ファイルオブジェクト、XMLの文字列も指定できる


# In[ ]:


type(d)


# In[ ]:


d.version


# In[ ]:


d.feed.title


# In[ ]:


d['feed']['title']
# dictの形式でもアクセスできる


# In[ ]:


d.feed.link


# In[ ]:


d.feed.description
# フィードの説明を取得する


# In[ ]:


len(d.entries)


# In[ ]:


d.entries[0].title


# In[ ]:


d.entries[0].link


# In[ ]:


d.entries[0].description


# In[ ]:


d.entries[0].updated


# In[ ]:


d.entries[0].updated_parsed
# 要素の更新日時をパースしてtime.struct_timeを取得する


# In[ ]:


get_ipython().run_cell_magic('writefile', 'scrape_by_feedparser.py', "\nimport feedparser\n\nd = feedparser.parse('http://b.hatena.ne.jp/hotentry/it.rss')\n\nfor entry in d.entries:\n    print(entry.link, entry.title)")


# In[ ]:


get_ipython().system('python scrape_by_feedparser.py')


# In[ ]:


# chapter 3-5 データベースに保存する


# In[ ]:


# MySQLへのデータの保存


# In[ ]:


# データベースとユーザーの作成 > ターミナル操作はEvernoteに


# In[ ]:


get_ipython().run_cell_magic('writefile', 'save_mysql.py', "\nimport MySQLdb\n\nconn = MySQLdb.connect(db='scraping', user='scraper', passwd='password', charset='utf8mb4')\n\nc = conn.cursor()\nc.execute('DROP TABLE IF EXISTS cities')\nc.execute('''\n    CREATE TABLE cities (\n        rank integer,\n        city text,\n        population integer\n    )\n''')\n\nc.execute('INSERT INTO cities VALUES (%s, %s, %s)', (1, '上海', 24150000))\n\nc.execute('INSERT INTO cities VALUES (%(rank)s, %(city)s, %(population)s)',\n         {'rank': 2, 'city': 'カラチ', 'population': 23500000})\n\nc.executemany('INSERT INTO cities VALUES (%(rank)s, %(city)s, %(population)s)', [\n    {'rank': 3, 'city': '北京', 'population': 21516000},\n    {'rank': 4, 'city': '天津', 'population': 14722100},\n    {'rank': 5, 'city': 'イスタンブル', 'population': 14160467},\n])\n\nconn.commit()\n\nc.execute('SELECT * FROM cities')\nfor row in c.fetchall():\n    print(row)\n    \nconn.close()")


# In[ ]:


get_ipython().system('python save_mysql.py')


# In[ ]:


# MongoDBへのデータの保存


# In[ ]:


# 本ではデフォルトのデータベースディレクトリは /data/db 、起動は mongod コマンドのみだが、それではなぜかうまく動かない
# ターミナルで mongod --config /usr/local/etc/mongod.conf で起動
# 終了は ctrl + c


# In[ ]:


get_ipython().run_cell_magic('writefile', 'save_mongo.py', "\nimport lxml.html\nfrom pymongo import MongoClient\n\n# HTMLファイルを読み込み、getroot()メソッドでHtmlElementオブジェクトを得る\ntree = lxml.html.parse('index.html')\nhtml = tree.getroot()\n\nclient = MongoClient('localhost', 27017)\ndb = client.scraping # scrapingデータベースを取得（作成）する\ncollection = db.links # linksコレクションを取得（作成）する\n\n# このスクリプトを何回実行しても同じ結果になるよう、コレクションのドキュメントをすべて削除する\ncollection.delete_many({})\n\n# cssselect()メソッドでa要素のリストを取得して、個々のa要素に対して処理を行う\nfor a in html.cssselect('a'):\n    # href属性とリンクのテキストを取得して保存する\n    collection.insert_one({\n        'url': a.get('href'),\n        'title': a.text,\n    })\n\n# コレクションのすべてのドキュメントを_idの順にソートして取得する\nfor link in collection.find().sort('_id'):\n    print(link['_id'], link['url'], link['title'])")


# In[ ]:


get_ipython().system('python save_mongo.py')


# In[ ]:


# chapter 3-6 クローラーとURL


# In[ ]:


# 相対URLから絶対URLへの変換例


# In[ ]:


from urllib.parse import urljoin


# In[ ]:


base_url = 'http://example.com/books/top.html'


# In[ ]:


# // で始まる相対URL
urljoin(base_url, '//cdn.example.com/logo.png')


# In[ ]:


# / で始まる相対URL
urljoin(base_url, '/articles/')


# In[ ]:


# ./ 形式の表記
urljoin(base_url, './')


# In[ ]:


# chapter 3-7 Pythonによるクローラーの作成


# In[ ]:


get_ipython().run_cell_magic('writefile', 'python_crawler_1.py', '\n# 一覧ページからURLの一覧を抜き出す(1)\n\nimport requests\nimport lxml.html\n\nresponse = requests.get(\'https://gihyo.jp/dp\')\nroot = lxml.html.fromstring(response.content)\nfor a in root.cssselect(\'a[itemprop="url"]\'):\n    url = a.get(\'href\')\n    print(url)')


# In[ ]:


get_ipython().system('python python_crawler_1.py')


# In[ ]:


get_ipython().run_cell_magic('writefile', 'python_crawler_2.py', '\n# 一覧ページからURLの一覧を抜き出す(2)\n# 不要なリンクを除外し、相対URLを絶対URLに変換する\n\nimport requests\nimport lxml.html\n\nresponse = requests.get(\'https://gihyo.jp/dp\')\nroot = lxml.html.fromstring(response.content)\nroot.make_links_absolute(response.url) # すべてのリンクを絶対URLに変換する\n\n# id="listBook"である要素の子孫のa要素のみを取得する\nfor a in root.cssselect(\'#listBook a[itemprop="url"]\'):\n    url = a.get(\'href\')\n    print(url)')


# In[ ]:


get_ipython().system('python python_crawler_2.py')


# In[ ]:


get_ipython().run_cell_magic('writefile', 'python_crawler_3.py', '\n# 一覧ページからURLの一覧を抜き出す(3)\n# あとで利用しやすいよう関数をつかってリファクタリングしておく\n\nimport requests\nimport lxml.html\n\ndef main():\n    """\n    クローラーのメインの処理\n    """\n    response = requests.get(\'https://gihyo.jp/dp\')\n    # scrape_list_page()関数を呼び出し、ジェネレーターイテレーターを取得\n    urls = scrape_list_page(response)\n    for url in urls: # ジェネレーターイテレーターはlistなどと同様に繰り返し可能\n        print(url)\n\ndef scrape_list_page(response):\n    """\n    一覧ページのResponseから詳細ページのURLを抜き出すジェネレーター関数\n    """\n    root = lxml.html.fromstring(response.content)\n    root.make_links_absolute(response.url) # すべてのリンクを絶対URLに変換する\n\n    # id="listBook"である要素の子孫のa要素のみを取得する\n    for a in root.cssselect(\'#listBook a[itemprop="url"]\'):\n        url = a.get(\'href\')\n        yield url # yield文でジェネレーターイテレーターの要素を返す\n        \nif __name__ == \'__main__\':\n    main()')


# In[ ]:


get_ipython().system('python python_crawler_3.py')


# In[ ]:


# 詳細ページからスクレイピングする(クロール前のテスト)


# In[ ]:


get_ipython().run_cell_magic('writefile', 'python_crawler_4.py', '\n# 詳細ページからスクレイピングする(1)\n\nimport requests\nimport lxml.html\n\n\ndef main():\n    session = requests.Session() # 複数のページをクロールするのでSessionを使う\n    response = session.get(\'https://gihyo.jp/dp\')\n    urls = scrape_list_page(response)\n    for url in urls:\n        response = session.get(url) # Sessionを使って詳細ページを取得\n        ebook = scrape_detail_page(response) # 詳細ページからスクレイピングして電子書籍の情報を得る\n        print(ebook) # 電子書籍の情報を表示\n        break # まず1ページだけで試すためbreak文でループを抜ける\n        \n        \ndef scrape_list_page(response):\n    root = lxml.html.fromstring(response.content)\n    root.make_links_absolute(response.url)\n    \n    for a in root.cssselect(\'#listBook a[itemprop="url"]\'):\n        url = a.get(\'href\')\n        yield url\n        \n        \ndef scrape_detail_page(response):\n    """\n    詳細ページのResponseから電子書籍の情報をdictで取得する\n    """\n    root = lxml.html.fromstring(response.content)\n    ebook = {\n        \'url\': response.url, # URL\n        \'title\': root.cssselect(\'#bookTitle\')[0].text_content(), # タイトル\n        \'price\': root.cssselect(\'.buy\')[0].text, # 価格(.textで直接の子である文字列のみを取得)\n        \'content\': [h3.text_content() for h3 in root.cssselect(\'#content > h3\')], # 目次\n    }\n    return ebook # dictを返す\n\n\nif __name__ == \'__main__\':\n    main()')


# In[ ]:


get_ipython().system('python python_crawler_4.py')


# In[ ]:


get_ipython().run_cell_magic('writefile', 'python_crawler_5.py', '\n# 詳細ページからスクレイピングする(2)\n#  不要な空白や改行は削除したい\n\nimport re\nimport requests\nimport lxml.html\n\n\ndef main():\n    session = requests.Session() # 複数のページをクロールするのでSessionを使う\n    response = session.get(\'https://gihyo.jp/dp\')\n    urls = scrape_list_page(response)\n    for url in urls:\n        response = session.get(url) # Sessionを使って詳細ページを取得\n        ebook = scrape_detail_page(response) # 詳細ページからスクレイピングして電子書籍の情報を得る\n        print(ebook) # 電子書籍の情報を表示\n        break # まず1ページだけで試すためbreak文でループを抜ける\n        \n        \ndef scrape_list_page(response):\n    root = lxml.html.fromstring(response.content)\n    root.make_links_absolute(response.url)\n    \n    for a in root.cssselect(\'#listBook a[itemprop="url"]\'):\n        url = a.get(\'href\')\n        yield url\n        \n        \ndef scrape_detail_page(response):\n    """\n    詳細ページのResponseから電子書籍の情報をdictで取得する\n    """\n    root = lxml.html.fromstring(response.content)\n    ebook = {\n        \'url\': response.url, # URL\n        \'title\': root.cssselect(\'#bookTitle\')[0].text_content(), # タイトル\n        \'price\': root.cssselect(\'.buy\')[0].text.strip(), # 価格(.textで直接の子である文字列のみを取得、strip()で前後の空白を削除)\n        \'content\': [normalize_spaces(h3.text_content()) for h3 in root.cssselect(\'#content > h3\')], # 目次\n    }\n    return ebook # dictを返す\n\n\ndef normalize_spaces(s):\n    """\n    連続する空白を1つのスペースに置き換え、前後の空白は削除した新しい文字列を取得する\n    """\n    return re.sub(r\'\\s+\', \' \', s).strip()\n\n\nif __name__ == \'__main__\':\n    main()')


# In[ ]:


get_ipython().system('python python_crawler_5.py')


# In[ ]:


# 詳細ページをクロールする


# In[ ]:


get_ipython().run_cell_magic('writefile', 'python_crawler_6.py', '\n# 詳細ページをクロールする\n#  不要な空白や改行は削除したい\n# 1秒ごとに電子書籍の情報を取得して表示する\n\nimport time\nimport re\nimport requests\nimport lxml.html\n\n\ndef main():\n    session = requests.Session() # 複数のページをクロールするのでSessionを使う\n    response = session.get(\'https://gihyo.jp/dp\')\n    urls = scrape_list_page(response)\n    for url in urls:\n        time.sleep(1) # 1秒のウェイトを入れる\n        response = session.get(url) # Sessionを使って詳細ページを取得\n        ebook = scrape_detail_page(response) # 詳細ページからスクレイピングして電子書籍の情報を得る\n        print(ebook) # 電子書籍の情報を表示\n        \n        \ndef scrape_list_page(response):\n    root = lxml.html.fromstring(response.content)\n    root.make_links_absolute(response.url)\n    \n    for a in root.cssselect(\'#listBook a[itemprop="url"]\'):\n        url = a.get(\'href\')\n        yield url\n        \n        \ndef scrape_detail_page(response):\n    """\n    詳細ページのResponseから電子書籍の情報をdictで取得する\n    """\n    root = lxml.html.fromstring(response.content)\n    ebook = {\n        \'url\': response.url, # URL\n        \'title\': root.cssselect(\'#bookTitle\')[0].text_content(), # タイトル\n        \'price\': root.cssselect(\'.buy\')[0].text.strip(), # 価格(.textで直接の子である文字列のみを取得、strip()で前後の空白を削除)\n        \'content\': [normalize_spaces(h3.text_content()) for h3 in root.cssselect(\'#content > h3\')], # 目次\n    }\n    return ebook # dictを返す\n\n\ndef normalize_spaces(s):\n    """\n    連続する空白を1つのスペースに置き換え、前後の空白は削除した新しい文字列を取得する\n    """\n    return re.sub(r\'\\s+\', \' \', s).strip()\n\n\nif __name__ == \'__main__\':\n    main()')


# In[ ]:


get_ipython().system('python python_crawler_6.py')


# In[ ]:


# スクレイピングしたデータを保存する


# In[ ]:


get_ipython().run_cell_magic('writefile', 'python_crawler_final.py', '\n# 詳細ページをクロールする\n#  不要な空白や改行は削除したい\n# 1秒ごとに電子書籍の情報を取得して表示する\n# 取得したデータをMongoDBに保存する(あらかじめMongoDBを起動しておく)\n# mongod --config /usr/local/etc/mongod.conf\n# 2回目以降はクロール済みのURLはクロールしないようにする\n\nimport time\nimport re\nimport requests\nimport lxml.html\nfrom pymongo import MongoClient\n\n\ndef main():\n    """\n    クローラーのメインの処理\n    """\n    \n    client = MongoClient(\'localhost\', 27017) # ローカルホストのMongoDBに接続する\n    collection = client.scraping.ebooks # scrapingデータベースのebooksコレクションを得る\n    # データを一意に識別するキーを格納するkeyフィールドにユニークなインデックスを作成する\n    collection.create_index(\'key\', unique=True)\n    \n    response = requests.get(\'https://gihyo.jp/dp\') # 一覧ページを取得する\n    urls = scrape_list_page(response) # 詳細ページのURL一覧を得る\n    for url in urls:\n        key = extract_key(url) # URLからキーを取得する\n        \n        ebook = collection.find_one({\'key\': key}) # MongoDBからkeyに該当するデータを探す\n        if not ebook: # MongoDBに存在しない場合だけ、詳細ページをクロールする\n            time.sleep(1) # 1秒のウェイトを入れる\n            response = requests.get(url) # 詳細ページを取得\n            ebook = scrape_detail_page(response) # 詳細ページからスクレイピングして電子書籍の情報を得る\n            collection.insert_one(ebook) # 電子書籍の情報をMongoDBに保存する\n            \n        print(ebook) # 電子書籍の情報を表示\n        \n        \ndef scrape_list_page(response):\n    """\n    一覧ページのResponseから詳細ページのURLを抜き出す\n    """\n    root = lxml.html.fromstring(response.content)\n    root.make_links_absolute(response.url)\n    \n    for a in root.cssselect(\'#listBook a[itemprop="url"]\'):\n        url = a.get(\'href\')\n        yield url\n        \n        \ndef scrape_detail_page(response):\n    """\n    詳細ページのResponseから電子書籍の情報をdictで得る\n    """\n    root = lxml.html.fromstring(response.content)\n    ebook = {\n        \'url\': response.url, # URL\n        \'key\': extract_key(response.url), # URLから抜き出したキー\n        \'title\': root.cssselect(\'#bookTitle\')[0].text_content(), # タイトル\n        \'price\': root.cssselect(\'.buy\')[0].text.strip(), # 価格(.textで直接の子である文字列のみを取得、strip()で前後の空白を削除)\n        \'content\': [normalize_spaces(h3.text_content()) for h3 in root.cssselect(\'#content > h3\')], # 目次\n    }\n    return ebook # dictを返す\n\n\ndef extract_key(url):\n    """\n    URLからキー(URLの末尾のISBN)を抜き出す\n    """\n    m = re.search(r\'/([^/]+)$\', url)\n    return m.group(1)\n\n\ndef normalize_spaces(s):\n    """\n    連続する空白を1つのスペースに置き換え、前後の空白は削除した新しい文字列を取得する\n    """\n    return re.sub(r\'\\s+\', \' \', s).strip()\n\n\nif __name__ == \'__main__\':\n    main()')


# In[ ]:


get_ipython().system('python python_crawler_final.py')

