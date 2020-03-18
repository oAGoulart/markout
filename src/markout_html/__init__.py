#!/usr/bin/env python3

import json
import sys
from pathlib import Path
from .markout_html import extract_url

def main():
  """Entry point for the application script"""
  argc = len(sys.argv)

  f = sys.argv[1] if argc > 1 else '.markoutrc.json'

  try:
    with open(f, 'r') as opt_file:
      contents = json.loads(opt_file.read())

    tokens = contents['tokens']
    only_on = contents['only_on']
    links = contents['links']
  except FileNotFoundError:
    tokens = {'p': "{}"}
    only_on = 'body'
    links = {'https://docs.python.org/3/': 'out.md'}

    print('Warning: Config file not accessible! Using default values.')

  # Iterate through each link and write out the results
  for link in links.keys():
    f = Path(links[link] or 'out/out.md')

    try:
      if f.parent != f:
        f.parent.mkdir(parents=True, exist_ok=True)

      with f.open('w+') as dest_file:
        dest_file.write(extract_url(link, tokens, only_on))
    except IOError:
      print('Error: Input/output error')
