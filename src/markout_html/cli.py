#!/usr/bin/env python

"""Command-line interface."""

import json
import sys
import argparse
import logging
from pathlib import Path
from .extract import *

def main():
  """Entry point for the application script"""
  parser = argparse.ArgumentParser()
  parser.add_argument('-e', '--extract', help='use to extract a HTML string')
  parser.add_argument('-t', '--tokens', help='JSON string with all tokens')
  parser.add_argument('-o', '--only_on', help='only extract from this tag')
  parser.add_argument('-l', '--links', help='JSON string with all links')
  parser.add_argument('-c', '--config', help='file with all configurations')
  args = parser.parse_args()

  f = args.config if args.config is not None else '.markoutrc.json'
  try:
    with open(f, 'r') as opt_file:
      contents = json.loads(opt_file.read())

    tokens = contents['tokens']
    only_on = contents['only_on']
    links = contents['links']
  except FileNotFoundError:
    tokens = {'p': "\n{}"}
    only_on = 'body'
    links = {'https://docs.python.org/3/': 'out.md'}

    logging.debug('Config file not accessible! Using default values.')
  
  # Terminal arguments have priority
  if args.tokens is not None:
    tokens = json.loads(args.tokens)
  if args.only_on is not None:
    only_on = args.only_on
  if args.links is not None:
    links = json.loads(args.links)

  if args.extract is not None:
    print(extract_html(args.extract, tokens, only_on), end="")
  else:
    # Iterate through each link and write out the results
    for link in links.keys():
      f = Path(links[link] or 'out/out.md')

      try:
        if f.parent != f:
          f.parent.mkdir(parents=True, exist_ok=True)

        with f.open('w+') as dest_file:
          dest_file.write(extract_url(link, tokens, only_on))
      except IOError:
        logging.debug('Input/output error')

if __name__ == '__main__':
  main()
