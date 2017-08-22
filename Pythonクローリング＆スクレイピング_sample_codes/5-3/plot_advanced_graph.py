import matplotlib
matplotlib.use('Agg')  # 描画のバックエンドとしてデスクトップ環境が不要なAggを使う。
# 日本語を描画できるようフォントを指定する。OS XとUbuntu用に2種類のフォントを列挙している。
# デフォルトでは英語用のフォントが使われ、日本語が□（いわゆる豆腐）で表示されてしまう。
matplotlib.rcParams['font.sans-serif'] = 'Hiragino Kaku Gothic Pro, MigMix 1P'
import matplotlib.pyplot as plt

# plot()の第3引数に系列のスタイルを表す文字列を指定できる。
# 'b'は青色、'x'はバツ印のマーカー、'-'はマーカーを実線で繋ぐことを意味する。
# キーワード引数labelで指定した系列の名前は、凡例で使用される。
plt.plot([1, 2, 3, 4, 5], [1, 2, 3, 4, 5], 'bx-', label='1次関数')
# スタイルの'r'は赤色、'o'は丸印のマーカー、'--'は点線を意味する。
plt.plot([1, 2, 3, 4, 5], [1, 4, 9, 16, 25], 'ro--', label='2次関数')
plt.xlabel('Xの値')  # xlabel()関数でX軸のラベルを指定する。
plt.ylabel('Yの値')  # ylabel()関数でY軸のラベルを指定する。
plt.title('matplotlibのサンプル')  # title()関数でグラフのタイトルを指定する。
plt.legend(loc='best')  # legend()関数で凡例を表示する。loc='best'は最適な位置に表示することを意味する。
plt.xlim(0, 6)  # X軸の範囲を0〜6とする。ylim()関数で同様にY軸の範囲を指定できる。
plt.savefig('advanced_graph.png', dpi=300)  # グラフを画像ファイルに保存する。
