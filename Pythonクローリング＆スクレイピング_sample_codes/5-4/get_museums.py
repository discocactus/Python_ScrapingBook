from SPARQLWrapper import SPARQLWrapper  # pip install SPARQLWrapper

# SPARQLエンドポイントのURLを指定してインスタンスを作成する。
sparql = SPARQLWrapper('http://ja.dbpedia.org/sparql')
# 日本の美術館を取得するクエリを設定する。バックスラッシュを含むので、rで始まるraw文字列を使用している。
sparql.setQuery(r'''
SELECT * WHERE {
    ?s rdf:type dbpedia-owl:Museum ;
       prop-ja:所在地 ?address .
    FILTER REGEX(?address, "^\\p{Han}{2,3}[都道府県]")
} ORDER BY ?s
''')
sparql.setReturnFormat('json')  # 取得するフォーマットとしてJSONを指定する。
# query()でクエリを実行し、convert()でレスポンスをパースしてdictを得る。
response = sparql.query().convert()

for result in response['results']['bindings']:
    print(result['s']['value'], result['address']['value'])  # 抽出した変数の値を表示する。
