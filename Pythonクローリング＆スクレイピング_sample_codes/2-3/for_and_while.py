# 変数xにinの右側のリストの要素が順に代入されて、ブロック内の処理が計3回実行される。
for x in [1, 2, 3]:
    print(x)  # 1, 2, 3が順に表示される。

# 回数を指定した繰り返しには組み込み関数range()を使う。
for i in range(10):
    print(i)  # 0〜9が順に表示される。

# for文にdictを指定するとキーに対して繰り返す。
d = {'a': 1, 'b': 2}
for key in d:
    value = d[key]
    print(key, value)

# dictのitems()メソッドで、dictのキーと値に対して繰り返す。
for key, value in d.items():
    print(key, value)

# while文で式が真の間、繰り返し処理する。
s = 1
while s < 1000:
    print(s)  # 1, 2, 4, 8, 16, 32, 64, 128, 256, 512が順に表示される。
    s = s * 2
