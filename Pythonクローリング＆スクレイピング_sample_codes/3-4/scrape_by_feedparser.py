import feedparser

# はてなブックマークの人気エントリー（「テクノロジー」カテゴリ）のRSSを読み込む。
d = feedparser.parse('http://b.hatena.ne.jp/hotentry/it.rss')

# すべての要素について処理を繰り返す。
for entry in d.entries:
    print(entry.link, entry.title)
