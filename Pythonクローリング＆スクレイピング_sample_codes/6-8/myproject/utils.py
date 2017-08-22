import logging

import lxml.html
import readability

# ReadabilityのDEBUG/INFOレベルのログを表示しないようにする。
# Spider実行時にReadabilityのログが大量に表示されて、
# ログが見づらくなってしまうのを防ぐため。
logging.getLogger('readability.readability').setLevel(logging.WARNING)


def get_content(html):
    """
    HTMLの文字列から (タイトル, 本文) のタプルを取得する。
    """

    document = readability.Document(html)
    content_html = document.summary()
    # HTMLタグを除去して本文のテキストのみを取得する。
    content_text = lxml.html.fromstring(content_html).text_content().strip()
    short_title = document.short_title()

    return short_title, content_text
