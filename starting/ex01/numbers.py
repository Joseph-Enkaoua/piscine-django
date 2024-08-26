#!/usr/bin/python3

def read_number(file):
  content = []
  while True:
    char = file.read(1)
    if char == ',' or char == '':
      break
    content.append(char)
  return ''.join(content)

def print_numbers():
  with open('numbers.txt', 'r') as file:
    while True:
      number = read_number(file)
      number = number.strip()
      if not number:
        break
      print(number)

if __name__ == '__main__':
  print_numbers()