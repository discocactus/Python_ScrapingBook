import re
import sys
from urllib.request import urlopen

f = urlopen('https://gihyo.jp/dp')
bytes_content = f.read()  # bytes型のレスポンスボディを一旦変数に格納する。

# charsetはHTMLの最初の方に書かれていると期待できるので、
# レスポンスボディの先頭1024バイトをASCII文字列としてデコードする。
# ASCII範囲外の文字はU+FFFD（REPLACEMENT CHARACTER）に置き換え、例外を発生させない。
scanned_text = bytes_content[:1024].decode('ascii', errors='replace')

# デコードした文字列から正規表現でcharsetの値を抜き出す。
match = re.search(r'charset=["\']?([\w-]+)', scanned_text)
if match:
    encoding = match.group(1)
else:
    encoding = 'utf-8'  # charsetが明示されていない場合はUTF-8とする。

print('encoding:', encoding, file=sys.stderr)  # 得られたエンコーディングを標準エラー出力に出力する。

text = bytes_content.decode(encoding)  # 得られたエンコーディングで再度デコードする。
print(text)  # レスポンスボディを標準出力に出力する。
