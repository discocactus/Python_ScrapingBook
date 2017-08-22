import requests
from retrying import retry  # pip install retrying

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

# stop_max_attempt_numberは最大リトライ回数を指定する。
# wait_exponential_multiplierは指数関数的なウェイトを取る場合の、初回のウェイトをミリ秒単位で指定する。
@retry(stop_max_attempt_number=3, wait_exponential_multiplier=1000)
def fetch(url):
    """
    指定したURLを取得してResponseオブジェクトを返す。一時的なエラーが起きた場合は最大3回リトライする。
    """
    print('Retrieving {0}...'.format(url))
    response = requests.get(url)
    print('Status: {0}'.format(response.status_code))
    if response.status_code not in TEMPORARY_ERROR_CODES:
        return response  # 一時的なエラーでなければresponseを返す。

    # 一時的なエラーの場合は例外を発生させてリトライする。
    raise Exception('Temporary Error: {0}'.format(response.status_code))

if __name__ == '__main__':
    main()
