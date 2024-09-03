#!/usr/bin/python3

class HotBeverage:
  def __init__(self, name="hot beverage", price=0.30):
    self.name = name
    self.price = price

  def description(self) -> str:
    return "Just some hot water in a cup."
  
  def __str__(self) -> str:
    return "".join("name : " + self.name + "\nprice : " + "{:.2f}".format(self.price) + "\ndescription : " + self.description())


class Coffee(HotBeverage):
  def __init__(self):
    super().__init__("coffee", 0.40)

  def description(self) -> str:
    return "A coffee, to stay awake."


class Tea(HotBeverage):
  def __init__(self):
    super().__init__("tea")


class Chocolate(HotBeverage):
  def __init__(self):
    super().__init__("chocolate", 0.50)

  def description(self) -> str:
    return "Chocolate, sweet chocolate..."


class Cappuccino(HotBeverage):
  def __init__(self):
    super().__init__("cappuccino", 0.45)

  def description(self) -> str:
    return "Un po’ di Italia nella sua tazza!"


def test():
  print(HotBeverage(), "\n---")
  print(Coffee(), "\n---")
  print(Tea(), "\n---")
  print(Chocolate(), "\n---")
  print(Cappuccino())


if __name__ == '__main__':
  test()