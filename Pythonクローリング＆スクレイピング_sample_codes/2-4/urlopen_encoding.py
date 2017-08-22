import sys
from urllib.request import urlopen

f = urlopen('https://gihyo.jp/dp')
# HTTPヘッダーからエンコーディングを取得する（明示されていない場合はutf-8とする）。
encoding = f.info().get_content_charset(failobj="utf-8")
print('encoding:', encoding, file=sys.stderr)  # エンコーディングを標準エラー出力に出力する。

text = f.read().decode(encoding)  # 得られたエンコーディングを指定して文字列にデコードする。
print(text)  # デコードしたレスポンスボディを標準出力に出力する。
