#!usr/bin/python3

from path import Path # type: ignore


def main():
  try:
    Path('new-folder').mkdir_p()
    Path('new-folder/new-file').touch()
  except Exception as e:
    print(e)

  with open('./new-folder/new-file', 'w+') as f:
    f.write('Successfuly done exercise 01')
    f.seek(0)
    print('Printing the content of \'new-folder/new-file\':\n')
    print(f.read())


if __name__ == "__main__":
  main()