
# CacheControlを使ってキャッシュを処理する

import requests
from cachecontrol import CacheControl

session = requests.session()
cached_session = CacheControl(session) # sessionをラップしたcached_sessionを作る

# 1回目はキャッシュがないのでサーバーから取得しキャッシュする
response = cached_session.get('http://docs.python.org/3/')
print(response.from_cache) # False

# 2回目以降はETagとLast-Modifiedの値を使って更新されているかを確認する
# 更新されていない場合のコンテンツはキャッシュから取得するので高速に処理できる
response = cached_session.get('http://docs.python.org/3/')
print(response.from_cache) # True