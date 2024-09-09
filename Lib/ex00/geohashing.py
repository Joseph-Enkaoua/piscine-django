#!/usr/bin/python3

import sys, antigravity


def main():
  if len(sys.argv) != 4:
    print('Usage: python3 geohashing.py <latitude> <longitude> <datedow>\n\
Example: python3 geohashing.py 37.42154234455 -122.085589 05-12-2024')
    sys.exit(1)

  try:
    lat = float(sys.argv[1])
    lon = float(sys.argv[2])

    datedow = sys.argv[3].encode()
    antigravity.geohash(lat, lon, datedow)
    
  except Exception as e:
    print('Error: ' + str(e) + '.\nPlease provide valid number for latitude and longitude.')
    sys.exit(1)

if __name__ == "__main__":
  main()