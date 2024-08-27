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
    reversed_states = {v: k for k,v in states.items()}
    reversed_capitals = {v: k for k, v in capital_cities.items()}
    key = reversed_capitals.get(sys.argv[1])
    state = reversed_states.get(key)
    if state:
      print(state)
    else:
      print("Unknown capital city")


if __name__ == '__main__':
  main()