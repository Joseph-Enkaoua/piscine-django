#!/usr/bin/python3

import sys

def main():
  states = {
    "Oregon" : "OR",
    "Alabama" : "AL",
    "New Jersey": "NJ",
    "Colorado" : "CO"
  }
  capital_cities = {
    "OR": "Salem",
    "AL": "Montgomery",
    "NJ": "Trenton",
    "CO": "Denver"
  }

  if len(sys.argv) == 2:
    state = states.get(sys.argv[1])
    capital = capital_cities.get(state)
    if capital:
      print(capital)
    else:
      print("Unknown state")


if __name__ == '__main__':
  main()