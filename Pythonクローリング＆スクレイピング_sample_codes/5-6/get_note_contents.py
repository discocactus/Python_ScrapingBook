import sys

from selenium import webdriver


def main():
    """
    メインの処理。
    """

    driver = webdriver.PhantomJS()  # PhantomJSのWebDriverオブジェクトを作成する。
    driver.set_window_size(800, 600)  # ウィンドウサイズを設定する。

    navigate(driver)  # noteのトップページに遷移する。
    posts = scrape_posts(driver)  # 文章コンテンツのリストを取得する。

    # コンテンツの情報を表示する。
    for post in posts:
        print(post)


def navigate(driver):
    """
    目的のページに遷移する。
    """

    print('Navigating...', file=sys.stderr)
    driver.get('https://note.mu/')  # noteのトップページを開く。
    assert 'note' in driver.title  # タイトルに'note'が含まれていることを確認する。


def scrape_posts(driver):
    """
    文章コンテンツのURL、タイトル、概要を含むdictのリストを取得する。
    """

    posts = []

    # すべての文章コンテンツを表すa要素について反復する。
    for a in driver.find_elements_by_css_selector('a.p-post--basic'):
        # URL、タイトル、概要を取得して、dictとしてリストに追加する。
        posts.append({
            'url': a.get_attribute('href'),
            'title': a.find_element_by_css_selector('h4').text,
            'description': a.find_element_by_css_selector('.c-post__description').text,
        })

    return posts

if __name__ == '__main__':
    main()
