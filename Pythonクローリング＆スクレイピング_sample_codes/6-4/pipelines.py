from scrapy.exceptions import DropItem

from pymongo import MongoClient
import MySQLdb


class ValidationPipeline(object):
    """
    Itemを検証するPipeline。
    """

    def process_item(self, item, spider):
        if not item['title']:
            # titleフィールドが取得できていない場合は破棄する。
            # DropItem()の引数は破棄する理由を表すメッセージ。
            raise DropItem('Missing title')

        return item  # titleフィールドが正しく取得できている場合。


class MongoPipeline(object):
    """
    ItemをMongoDBに保存するPipeline。
    """

    def open_spider(self, spider):
        """
        Spiderの開始時にMongoDBに接続する。
        """

        self.client = MongoClient('localhost', 27017)  # ホストとポートを指定してクライアントを作成。
        self.db = self.client['scraping-book']  # scraping-book データベースを取得。
        self.collection = self.db['items']  # items コレクションを取得。

    def close_spider(self, spider):
        """
        Spiderの終了時にMongoDBへの接続を切断する。
        """

        self.client.close()

    def process_item(self, item, spider):
        """
        Itemをコレクションに追加する。
        """

        # insert_one()の引数は書き換えられるので、コピーしたdictを渡す。
        self.collection.insert_one(dict(item))
        return item


class MySQLPipeline(object):
    """
    ItemをMySQLに保存するPipeline。
    """

    def open_spider(self, spider):
        """
        Spiderの開始時にMySQLサーバーに接続する。
        itemsテーブルが存在しない場合は作成する。
        """

        settings = spider.settings  # settings.pyから設定を読み込む。
        params = {
            'host': settings.get('MYSQL_HOST', 'localhost'),  # ホスト
            'db': settings.get('MYSQL_DATABASE', 'scraping'),  # データベース名
            'user': settings.get('MYSQL_USER', ''),  # ユーザー名
            'passwd': settings.get('MYSQL_PASSWORD', ''),  # パスワード
            'charset': settings.get('MYSQL_CHARSET', 'utf8mb4'),  # 文字コード
        }
        self.conn = MySQLdb.connect(**params)  # MySQLサーバーに接続。
        self.c = self.conn.cursor()  # カーソルを取得。
        # itemsテーブルが存在しない場合は作成。
        self.c.execute('''
            CREATE TABLE IF NOT EXISTS items (
                id INTEGER NOT NULL AUTO_INCREMENT,
                title CHAR(200) NOT NULL,
                PRIMARY KEY (id)
            )
        ''')
        self.conn.commit()  # 変更をコミット。

    def close_spider(self, spider):
        """
        Spiderの終了時にMySQLサーバーへの接続を切断する。
        """

        self.conn.close()

    def process_item(self, item, spider):
        """
        Itemをitemsテーブルに挿入する。
        """

        self.c.execute('INSERT INTO items (title) VALUES (%(title)s)', dict(item))
        self.conn.commit()  # 変更をコミット。
        return item
