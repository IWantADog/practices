from dataclasses import dataclass


def func(a: int, b: str) -> str:
    return f"a={a}, b={b}"

@dataclass
class Item:
    a:int
    b:int
    c:int 


class A:
    def __init__(self, item: Item) -> None:
        self.item = item

    def calculate(self) -> int:
        return self.item.a + self.item.b


if __name__ == "__main__":
    item = Item(a=1, b=2, c=3)
    a = A(item)
    c = a.calculate()
    print(c)