#!/usr/bin/python3

import random
from beverages import HotBeverage, Coffee, Tea, Cappuccino, Chocolate

class CoffeeMachine:
  def __init__(self) -> None:
    self.drinks_served = 0

  class EmptyCup(HotBeverage):
    def __init__(self):
      super().__init__("empty cup", 0.90)
    
    def description(self) -> str:
      return "An empty cup?! Gimme my money back!"
  
  class BrokenMachineException(Exception):
    def __init__(self) -> None:
      super().__init__("This coffee machine has to be repaired.")

  def repair(self):
    self.drinks_served = 0

  def serve(self, drink: HotBeverage):
    if self.drinks_served >= 10:
      raise self.BrokenMachineException

    self.drinks_served += 1
    return random.choice([drink(), self.EmptyCup()])


def test():
  machine = CoffeeMachine()

  for _ in range(22):
    try:
      print(machine.serve(random.choice([Chocolate, Tea, Coffee, Cappuccino])))
    except Exception as e:
      print(e)
      machine.repair()


if __name__ == '__main__':
  test()