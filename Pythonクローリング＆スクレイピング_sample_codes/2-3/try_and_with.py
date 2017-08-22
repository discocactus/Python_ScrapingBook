d = {'a': 1, 'b': 2}
try:
    print(d['x'])  # 例外が発生する可能性がある処理。
except KeyError:
    # try節内でexcept節に書いた例外（ここではKeyError）が発生した場合、except節が実行される。
    print('x is not found')  # キーが存在しない場合の処理。

# open()関数の戻り値を変数fに代入し、with節のブロック内で使う。このブロックを抜ける際に、f.close()が自動的に呼び出される。
with open('index.html') as f:
    print(f.read())
