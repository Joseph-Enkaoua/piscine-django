#!/usr/bin/python3

def print_numbers():
  with open('numbers.txt', 'r') as file:
    content = file.read()
    nums = content.split(',')
    for num in nums:
      num = num.strip() # avoid printing empty line in the end
      print(num)


if __name__ == '__main__':
  print_numbers()