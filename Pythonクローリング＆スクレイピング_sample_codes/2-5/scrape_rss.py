from xml.etree import ElementTree  # ElementTreeモジュールをインポートする。

# parse()関数でファイルを読み込んでElementTreeオブジェクトを得る。
tree = ElementTree.parse('rss2.xml')
# getroot()メソッドでXMLのルート要素（この例ではrss要素）に対応するElementオブジェクトを得る。
root = tree.getroot()

# findall()メソッドでXPathにマッチする要素のリストを取得する。
# channel/item はchannel要素の子要素であるitem要素を表す。
for item in root.findall('channel/item'):
    # find()メソッドでXPathにマッチする要素を取得し、text属性で要素の文字列を取得する。
    title = item.find('title').text  # title要素の文字列を取得する。
    url = item.find('link').text     # link要素の文字列を取得する。
    print(url, title)  # URLとタイトルを表示する。
