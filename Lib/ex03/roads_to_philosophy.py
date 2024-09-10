#!usr/bin/python3

import sys, requests # type: ignore
from bs4 import BeautifulSoup # type: ignore


class RoadsToPhilosophy:
  def __init__(self) -> None:
    self.visited = []

  def search_next_link(self, title: str):
    URL = "https://en.wikipedia.org/wiki/" + title.replace(' ', '_')

    try:
      res = requests.get(URL)
      res.raise_for_status()
    except requests.HTTPError as e:
      if res.status_code == 404:
        print("It's a dead end !")
      else:
        print(e)
      sys.exit(1)

    soup = BeautifulSoup(res.text, 'html.parser')

    page_title = soup.title.string[:-12]
    if page_title in self.visited:
      print('It leads to an infinite loop !')
      sys.exit(1)

    self.visited.append(page_title)

    if page_title == 'Philosophy':
      for t in self.visited:
        print(t)
      if len(self.visited) == 1:
        print('You took the highway to Philosophy!')
      else:
        print('{num} roads from {request} to Philosophy'.format(num=len(self.visited),request=self.visited[0]))
      sys.exit(0)

    # Find the first link that's inside <p> and is a link to another wiki article through filtering all others
    for link in soup.find_all('a', href=True):
      if link.parent.name == 'p' and link.get('href') and link['href'].startswith('/wiki/') \
        and not any(link['href'].startswith(prefix) for prefix in ['/wiki/Help:', '/wiki/Special:', '/wiki/Talk:', \
        '/wiki/Portal:', '/wiki/User:', '/wiki/Template:', '/wiki/File:', '/wiki/Category:', '/wiki/Wikipedia:']):
        self.search_next_link(link['href'][6:])

    print('It leads to a dead end !')


def main():
  if len(sys.argv) != 2:
    print('Please insert your search request in one string.\nExample: python3 request_wikipedia.py "top gun"')
    sys.exit(1)

  road = RoadsToPhilosophy()
  road.search_next_link(sys.argv[1])


if __name__ == "__main__":
  main()