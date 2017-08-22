import re

value = '3,000'
if not re.search(r'^[0-9,]+$', value):  # 数字とカンマのみを含む正規表現にマッチするかチェックする。
    raise ValueError('Invalid price')  # 正しい値でない場合は例外を発生させる。
