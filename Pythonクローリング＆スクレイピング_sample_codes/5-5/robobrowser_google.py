from robobrowser import RoboBrowser

# RoboBrowserオブジェクトを作成する。キーワード引数parserはBeautifulSoup()の第2引数として使われる。
browser = RoboBrowser(parser='html.parser')

browser.open('https://www.google.co.jp/')  # open()メソッドでGoogleのトップページを開く。

# 検索語を入力して送信する。
form = browser.get_form(action='/search')  # フォームを取得。
form['q'] = 'Python'  # フォームのqという名前のフィールドに検索語を入力。
browser.submit_form(form, list(form.submit_fields.values())[0])  # 一つ目のボタン（Google 検索）を押す。

# 検索結果のタイトルとURLを抽出して表示する。
# select()メソッドはBeautiful Soupのselect()メソッドと同じものであり、
# 引数のCSSセレクターにマッチする要素に対応するTagオブジェクトのリストを取得できる。
for a in browser.select('h3 > a'):
    print(a.text)
    print(a.get('href'))
