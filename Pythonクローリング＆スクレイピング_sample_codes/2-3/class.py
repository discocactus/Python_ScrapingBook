# Rectという名前のクラスを定義する。
class Rect:
    # インスタンスが作成された直後に呼び出される特殊なメソッドを定義する。
    def __init__(self, width, height):
        self.width = width    # width属性に値を格納する。
        self.height = height  # height属性に値を格納する。

    # 面積を計算するメソッドを定義する。
    def area(self):
        return self.width * self.height

r = Rect(100, 20)
print(r.width, r.height, r.area())   # 100 20 2000と表示される。


# Rectを継承したSquareクラスを定義する。
class Square(Rect):
    def __init__(seif, width):
        super().__init__(width, width)  # 親クラスのメソッドを呼び出す。
