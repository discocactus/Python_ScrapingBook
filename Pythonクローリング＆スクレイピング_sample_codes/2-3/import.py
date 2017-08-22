import sys  # sysモジュールを現在の名前空間にインポート。
from datetime import date  # datetimeモジュールから、dateクラスだけを現在の名前空間にインポート。

print(sys.argv)  # sysモジュールのargvという変数で、コマンドライン引数のリストを取得して表示する。
print(date.today())  # dateクラスのtoday()メソッドで今日の日付を取得して表示する。
