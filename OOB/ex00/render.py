#!/usr/bin/python3

import os
import sys
import settings

def main():
  if len(sys.argv) != 2 or sys.argv[1][-9:] != '.template' or not os.path.isfile(sys.argv[1]):
    print('Please execute the program with 1 argument which must be the path to an existing \'.template\' file')
    return

  with open(sys.argv[1], 'r') as f:
    template = f.read()

  file = template.format(
    title=getattr(settings, 'title', ''),
    name=getattr(settings, 'name', ''),
    surname=getattr(settings, 'surname', ''),
    age=getattr(settings, 'age', ''),
    profession=getattr(settings, 'profession', '')
  )


  with open("".join([sys.argv[1][0:-9], ".html"]), 'w') as f:
    f.write(file)


if __name__ == '__main__':
  main()