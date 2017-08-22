import sys
import hashlib
import json

from elasticsearch import Elasticsearch

# Elasticsearchのクライアントを作成する。第1引数でノードのリストを指定できる。
# デフォルトではlocalhostの9200ポートに接続するため省略可能。
es = Elasticsearch(['localhost:9200'])

# キーワード引数bodyでJSONに相当するdictを指定して、pagesインデックスを作成する。
# ignore=400はインデックスが存在する場合でもエラーにしないという意味。
result = es.indices.create(index='pages', ignore=400, body={
    # settingsという項目で、kuromoji_analyzerというアナライザーを定義する。
    # アナライザーは転置インデックスの作成方法を指定するもの。
    "settings": {
        "analysis": {
            "analyzer": {
                "kuromoji_analyzer": {
                    # 日本語形態素解析を使って文字列を分割するkuromoji_tokenizerを使用。
                    "tokenizer": "kuromoji_tokenizer"
                }
            }
        }
    },
    # mappingsという項目で、pageタイプを定義する。
    "mappings": {
        "page": {
            # _allはすべてのフィールドを結合して一つの文字列とした特殊なフィールド。
            # アナライザーとして上で定義したkuromoji_analyzerを使用。
            "_all": {"analyzer": "kuromoji_analyzer"},
            # url、title、contentの3つのフィールドを定義。
            # titleとcontentではアナライザーとして上で定義したkuromoji_analyzerを使用。
            "properties": {
                "url": {"type": "string"},
                "title": {"type": "string", "analyzer": "kuromoji_analyzer"},
                "content": {"type": "string", "analyzer": "kuromoji_analyzer"}
            }
        }
    }
})
print(result)  # Elasticsearchからのレスポンスを表示。

# コマンドライン引数の第1引数で指定したパスのファイルを読み込む。
with open(sys.argv[1]) as f:
    for line in f:  # JSON Lines形式のファイルを1行ずつ読み込む。
        page = json.loads(line)  # 行をJSONとしてパースする。
        # URLのSHA-1ハッシュの値をドキュメントのIDとする。
        # IDは必須ではないが、設定しておくと同じIDがあったときに別のドキュメントが
        # 作成されるのではなく、同じドキュメントの新しいバージョンとなり、重複を防げる。
        doc_id = hashlib.sha1(page['url'].encode('utf-8')).hexdigest()
        # Elasticsearchにインデックス化（保存）する。
        result = es.index(index='pages', doc_type='page', id=doc_id, body=page)
        print(result)  # Elasticsearchからのレスポンスを表示。
