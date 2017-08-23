
import sqlite3

conn = sqlite3.connect('top_cities.db')

c = conn.cursor()
c.execute('DROP TABLE IF EXISTS cities')
c.execute('''
    CREATE TABLE cities (
        rank integer,
        city text,
        population integer
    )
''')

# execute()メソッドの第2引数にはSQL文のパラメーターのリストを指定できる
# パラメーターで置き換える場所(プレースホルダー)は ? で指定する
c.execute('INSERT INTO cities VALUES (?, ?, ?)', (1, '上海', 24150000))

# パラメーターが辞書の場合、プレースホルダーは :キー名 で指定する
c.execute('INSERT INTO cities VALUES (:rank, :city, :population)',
         {'rank': 2, 'city': 'カラチ', 'population': 23500000})

# executemany()メソッドでは、複数のパラメーターをリストで指定できる
# パラメーターの数(ここでは3つ)のSQLを順に実行できる
c.executemany('INSERT INTO cities VALUES (:rank, :city, :population)', [
    {'rank': 3, 'city': '北京', 'population': 21516000},
    {'rank': 4, 'city': '天津', 'population': 14722100},
    {'rank': 5, 'city': 'イスタンブル', 'population': 14160467},
])

conn.commit()

c.execute('SELECT * FROM cities')
for row in c.fetchall():
    print(row)
    
conn.close()