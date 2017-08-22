import sys
import os
import json
import dbm
from urllib.request import urlopen
from urllib.parse import urlencode

from SPARQLWrapper import SPARQLWrapper


def main():
    features = []  # 美術館の情報を格納するためのリスト。

    for museum in get_museums():
        # ラベルがある場合はラベルを、ない場合はsの値を取得。
        label = museum.get('label', museum['s'])
        address = museum['address']

        if 'lon_degree' in museum:
            # 位置情報が含まれる場合は、経度と緯度を60進数（度分秒）から10進数に変換する。
            # 10進数の度 = 60進数の度 + 60進数の分 / 60 + 60進数の秒 / 3600
            lon = float(museum['lon_degree']) + float(museum['lon_minute']) / 60 + \
                float(museum['lon_second']) / 3600
            lat = float(museum['lat_degree']) + float(museum['lat_minute']) / 60 + \
                float(museum['lat_second']) / 3600
        else:
            # 位置情報が含まれない場合は、住所をジオコーディングして経度と緯度を取得する。
            lon, lat = geocode(address)

        print(label, address, lon, lat)  # 変数の値を表示。

        # ジオコーディングしても位置情報を取得できなかった場合はfeaturesに含めない。
        if lon is None:
            continue

        # featuresに美術館の情報をGeoJSONのFeatureの形式で追加する。
        features.append({
            'type': 'Feature',
            'geometry': {'type': 'Point', 'coordinates': [lon, lat]},
            'properties': {'label': label, 'address': address},
        })

    # GeoJSONのFeatureCollectionの形式でdictを作成する。
    feature_collection = {
        'type': 'FeatureCollection',
        'features': features,
    }
    # FeatureCollectionを.geojsonという拡張子のファイルに書き出す。
    with open('museums.geojson', 'w') as f:
        json.dump(feature_collection, f)


def get_museums():
    """
    SPARQLを使ってDBpedia Japaneseから美術館の情報を取得する。
    """

    print('Executing SPARQL query...', file=sys.stderr)

    # SPARQLエンドポイントのURLを指定してインスタンスを作成する。
    sparql = SPARQLWrapper('http://ja.dbpedia.org/sparql')
    # 日本の美術館を取得するクエリを設定する。
    # ※正規表現にバックスラッシュを含むので、rで始まるraw文字列を使用している。
    sparql.setQuery(r'''
    SELECT * WHERE {
        ?s rdf:type dbpedia-owl:Museum ;
        prop-ja:所在地 ?address .
        OPTIONAL { ?s rdfs:label ?label . }
        OPTIONAL {
        ?s prop-ja:経度度 ?lon_degree ;
            prop-ja:経度分 ?lon_minute ;
            prop-ja:経度秒 ?lon_second ;
            prop-ja:緯度度 ?lat_degree ;
            prop-ja:緯度分 ?lat_minute ;
            prop-ja:緯度秒 ?lat_second .
        }
        FILTER REGEX(?address, "^\\p{Han}{2,3}[都道府県]")
    } ORDER BY ?s
    ''')
    # 取得するフォーマットとしてJSONを指定する。
    sparql.setReturnFormat('json')
    # query()でクエリを実行し、convert()でレスポンスをパースしてdictを得る。
    response = sparql.query().convert()

    print('Got {0} results'.format(len(response['results']['bindings']), file=sys.stderr))

    # クエリの実行結果を反復処理する。
    for result in response['results']['bindings']:
        # 扱いやすいように {変数名1: 値1, 変数名2: 値2, ...} という形式のdictをyieldする。
        # resultを加工した辞書を得るために、辞書内包表記というリスト内包表記に似た表記法を使う。
        yield {name: binding['value'] for name, binding in result.items()}


# Yahoo!ジオコーダAPIのURL。
YAHOO_GEOCODER_API_URL = 'http://geo.search.olp.yahooapis.jp/OpenLocalPlatform/V1/geoCoder'
# DBM（ファイルを使ったキーバリュー型のDB）をジオコーディング結果のキャッシュとして
# 使用する。この変数はdictと同じように扱える。
geocoding_cache = dbm.open('geocoding.db', 'c')


def geocode(address):
    """
    引数で指定した住所をジオコーディングして、経度と緯度のペアを返す。
    """

    if address not in geocoding_cache:
        # 住所がキャッシュに存在しない場合はYahoo!ジオコーダAPIでジオコーディングする。
        print('Geocoding {0}...'.format(address), file=sys.stderr)
        url = YAHOO_GEOCODER_API_URL + '?' + urlencode({
            # アプリケーションIDは環境変数から取得する。
            'appid': os.environ['YAHOOJAPAN_APP_ID'],
            'output': 'json',
            'query': address,
        })

        response_text = urlopen(url).read()
        # APIのレスポンスをキャッシュに格納する。
        # キーや値にはbytes型しか使えないが、str型は自動的にbytes型に変換される。
        geocoding_cache[address] = response_text

    # キャッシュ内のAPIレスポンスをdictに変換。
    # 値はbytes型なので、文字列として扱うにはデコードが必要。
    response = json.loads(geocoding_cache[address].decode('utf-8'))

    if 'Feature' not in response:
        # ジオコーディングで結果が得られなかった場合はNoneのペアを返す。
        return (None, None)

    # Coordinatesというキーの値を,で分割。
    coordinates = response['Feature'][0]['Geometry']['Coordinates'].split(',')
    # floatのペアに変換して返す。
    return (float(coordinates[0]), float(coordinates[1]))

if __name__ == '__main__':
    main()
