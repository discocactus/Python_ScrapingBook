import sys
import time

import requests
import lxml.html
import boto3

# S3のバケット名。自分で作成したバケットに置き換えてください。
S3_BUCKET_NAME = 'scraping-book'


def main():
    # Wikimedia Commonsのページから画像のURLを抽出する。
    image_urls = get_image_urls('https://commons.wikimedia.org/wiki/Category:Mountain_glaciers')

    # S3のBucketオブジェクトを取得する。
    s3 = boto3.resource('s3')
    bucket = s3.Bucket(S3_BUCKET_NAME)

    for image_url in image_urls:
        time.sleep(2)  # 2秒のウェイトを入れる。

        # 画像ファイルをダウンロードする。
        print('Downloading', image_url, file=sys.stderr)
        response = requests.get(image_url)

        # URLからファイル名を取得する。
        _, filename = image_url.rsplit('/', maxsplit=1)

        # ダウンロードしたファイルをS3に保存する。
        print('Putting', filename, file=sys.stderr)
        bucket.put_object(Key=filename, Body=response.content)


def get_image_urls(page_url):
    """
    引数で与えられたURLのページに表示されているサムネイル画像の元画像のURLのリストを取得する。
    """
    response = requests.get(page_url)
    html = lxml.html.fromstring(response.text)

    image_urls = []
    for img in html.cssselect('.thumb img'):
        thumbnail_url = img.get('src')
        image_urls.append(get_original_url(thumbnail_url))

    return image_urls


def get_original_url(thumbnail_url):
    """
    サムネイルのURLから元画像のURLを取得する。
    """

    # 一番最後の/で区切り、ディレクトリに相当する部分のURLを得る。
    directory_url, _ = thumbnail_url.rsplit('/', maxsplit=1)
    # /thumb/を/に置き換えて元画像のURLを得る。
    original_url = directory_url.replace('/thumb/', '/')

    return original_url

if __name__ == '__main__':
    main()
