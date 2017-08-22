import time

import requests

TEMPORARY_ERROR_CODES = (408, 500, 502, 503, 504)  # 一時的なエラーを表すステータスコード。


def main():
    """
    メインとなる処理。
    """
    response = fetch('http://httpbin.org/status/200,404,503')
    if 200 <= response.status_code < 300:
        print('Success!')
    else:
        print('Error!')


def fetch(url):
    """
    指定したURLを取得してResponseオブジェクトを返す。一時的なエラーが起きた場合は最大3回リトライする。
    """
    max_retries = 3  # 最大で3回リトライする。
    retries = 0  # 現在のリトライ回数を示す変数。
    while True:
        try:
            print('Retrieving {0}...'.format(url))
            response = requests.get(url)
            print('Status: {0}'.format(response.status_code))
            if response.status_code not in TEMPORARY_ERROR_CODES:
                return response  # 一時的なエラーでなければresponseを返す。

        except requests.exceptions.RequestException as ex:
            # ネットワークレベルのエラー（RequestException）の場合はリトライする。
            print('Exception occured: {0}'.format(ex))

        retries += 1
        if retries >= max_retries:
            raise Exception('Too many retries.')  # リトライ回数の上限を超えた場合は例外を発生させる。

        wait = 2**(retries - 1)  # 指数関数的なリトライ間隔を求める（**はべき乗を表す演算子）。
        print('Waiting {0} seconds...'.format(wait))
        time.sleep(wait)  # ウェイトを取る。

if __name__ == '__main__':
    main()
