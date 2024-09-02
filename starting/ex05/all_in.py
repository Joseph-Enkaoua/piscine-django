#!/usr/bin/python3

import sys

def find_capital_or_state(entry):
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

  titled_entry = entry.title()
  state = states.get(titled_entry)
  capital = capital_cities.get(state)
  if capital:
    print(capital, "is the capital of", titled_entry)
    return
  
  reversed_states = {v: k for k,v in states.items()}
  reversed_capitals = {v: k for k, v in capital_cities.items()}
  key = reversed_capitals.get(titled_entry)
  state = reversed_states.get(key)
  if state:
    print(titled_entry, "is the capital of", state)
    return
  
  print(entry, "is neither a capital city nor a state")


def main():  
  if len(sys.argv) == 2:
    entries = sys.argv[1].split(',')
    for entry in entries:
      entry = entry.strip()
      if entry:
        find_capital_or_state(entry)


if __name__ == '__main__':
  main()
