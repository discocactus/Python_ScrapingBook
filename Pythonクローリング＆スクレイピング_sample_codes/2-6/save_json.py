import json

cities = [
    {'rank': 1, 'city': '上海', 'population': 24150000},
    {'rank': 2, 'city': 'カラチ', 'population': 23500000},
    {'rank': 3, 'city': '北京', 'population': 21516000},
    {'rank': 4, 'city': '天津', 'population': 14722100},
    {'rank': 5, 'city': 'イスタンブル', 'population': 14160467},
]

print(json.dumps(cities))
