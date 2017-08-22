import re
import sqlite3
from urllib.request import urlopen
from html import unescape


def main():
    """
    メインの処理。fetch(), scrape(), save()の3つの関数を呼び出す。
    """

    html = fetch('https://gihyo.jp/dp')
    books = scrape(html)
    save('books.db', books)


def fetch(url):
    """
    引数urlで与えられたURLのWebページを取得する。
    WebページのエンコーディングはContent-Typeヘッダーから取得する。
    戻り値：str型のHTML
    """

    f = urlopen(url)
    # HTTPヘッダーからエンコーディングを取得する（明示されていない場合はutf-8とする）。
    encoding = f.info().get_content_charset(failobj="utf-8")
    html = f.read().decode(encoding)  # 得られたエンコーディングを指定して文字列にデコードする。

    return html


def scrape(html):
    """
    引数htmlで与えられたHTMLから正規表現で書籍の情報を抜き出す。
    戻り値：書籍 (dict) のリスト
    """

    books = []
    for partial_html in re.findall(r'<a itemprop="url".*?</ul>\s*</a></li>', html, re.DOTALL):
        # 書籍のURLは itemprop="url" という属性を持つa要素のhref属性から取得する。
        url = re.search(r'<a itemprop="url" href="(.*?)">', partial_html).group(1)
        url = 'https://gihyo.jp' + url  # / で始まっているのでドメイン名などを追加する。

        # 書籍のタイトルは itemprop="name" という属性を持つp要素から取得する。
        title = re.search(r'<p itemprop="name".*?</p>', partial_html).group(0)
        title = re.sub(r'<.*?>', '', title)  # タグを取り除く。
        title = unescape(title)  # 文字参照を元に戻す。

        books.append({'url': url, 'title': title})

    return books


def save(db_path, books):
    """
    引数booksで与えられた書籍のリストをSQLiteデータベースに保存する。
    データベースのパスは引数db_pathで与えられる。
    戻り値：なし
    """

    conn = sqlite3.connect(db_path)  # データベースを開き、コネクションを取得する。

    c = conn.cursor()  # カーソルを取得する。
    # execute()メソッドでSQL文を実行する。
    # このスクリプトを何回実行しても同じ結果になるようにするため、booksテーブルが存在する場合は削除する。
    c.execute('DROP TABLE IF EXISTS books')
    # booksテーブルを作成する。
    c.execute('''
        CREATE TABLE books (
            title text,
            url text
        )
    ''')

    # executemany()メソッドでは、複数のパラメーターをリストで指定できる。
    c.executemany('INSERT INTO books VALUES (:title, :url)', books)

    conn.commit()  # 変更をコミット（保存）する。
    conn.close()  # コネクションを閉じる。

# pythonコマンドで実行された場合にmain()関数を呼び出す。これはモジュールとして他のファイルから
# インポートされたときに、main()関数が実行されないようにするための、Pythonにおける一般的なイディオム。
if __name__ == '__main__':
    main()
