#!usr/bin/python3
 
import requests, json, dewiki, sys # type: ignore


def get_page_content() -> str:
  S = requests.session()
  URL = "https://en.wikipedia.org/w/api.php"

  PARAMS = {
    "action": "opensearch",
    "namespace": "0",
    "search": sys.argv[1],
    "limit": "1",
    "format": "json"
  }

  # Get the first result with the request string
  R = S.get(url=URL, params=PARAMS)
  DATA = R.json()

  if len(DATA[1]) == 0:
    print("No results found for the search term.")
    sys.exit(1)

  first_result_title = DATA[1][0]

  PARAMS_CONTENT = {
    "action": "parse",
    "format": "json",
    "prop": "wikitext",
    "page": first_result_title,
    "redirects": "true"
  }

  # Request the actual page of the first search result
  R2 = S.get(url=URL, params=PARAMS_CONTENT)
  content_dict = json.loads(R2.text)
  return dewiki.from_string(content_dict["parse"]["wikitext"]["*"])


def main():
  if len(sys.argv) != 2:
    print('Please add your search request in one string.\nExample: python3 request_wikipedia.py "airplane"')
    sys.exit(1)

  try:
    content = get_page_content()
  except Exception as e:
    print(e)
    sys.exit(1)

  file_name = sys.argv[1].replace(' ', '_')
  with open(file_name+'.wiki', 'w+') as f:
    f.write(content)


if __name__ == "__main__":
  main()