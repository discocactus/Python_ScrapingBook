from voluptuous import Schema, Match  # pip install voluptuous

# 次の4つのルールを持つスキーマを定義する。
schema = Schema({  # ルール1：オブジェクトはdictである。
    'name': str,   # ルール2：nameの値は文字列である。
    'price': Match(r'^[0-9,]+$'),  # ルール3：priceの値は正規表現にマッチする。
}, required=True)  # ルール4：dictのキーは必須である。

# Schemaオブジェクトを関数として呼び出すと、引数のオブジェクトを対象にバリデーションを行う。
schema({
    'name': 'ぶどう',
    'price': '3,000',
})  # スキーマに適合するので例外は発生しない。

schema({
    'name': None,
    'price': '3,000',
})  # スキーマに適合しないので、例外MultipleInvalidが発生する。
