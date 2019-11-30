#!/usr/bin/env python3

import re
import json
import sys
import os
import urllib.request
from pyquery import PyQuery as pq

def extract_markdown(url, tokens, only_on = 'html'):
  """Generate Markdown code from a HTML page.

  Keyword arguments:
  url -- the page address
  tokens -- the list of tokens used to convert HTML to Markdown
  only_on -- from which tag should the Markdown be extracted (default 'html')
  """
  markdown = ''

  if url != '' and tokens != {}:
    # Request and decode HTML page
    req = urllib.request.Request(url)
    try:
      with urllib.request.urlopen(req) as response:
        html = response.read().decode('utf8')
    except urllib.error.HTTPError as e:
      print('Error: Request error, code:', e.code)

    # Prepare 'only_on' HTML document
    d = pq(html)
    d('head').remove()
    html = pq(d(only_on)).html()

    if html is not None:
      d = pq(html)
      for key in tokens.keys():
        # Iterate through each element that has a token on 'tokens'
        for e in d(key):
          # Verify <a> and <img> special tags cases
          if key == 'a':
            inline_md = ':markdown:' + tokens[key].format(pq(e).text(), pq(e).attr('href')) + ':markdown:'
            html = html.replace(str(pq(e)), inline_md)
          elif key == 'img':
            inline_md = ':markdown:' + tokens[key].format(pq(e).attr('alt'), pq(e).attr('src')) + ':markdown:'
            html = html.replace(str(pq(e)), inline_md)
          else:
            inline_md = ':markdown:' + tokens[key].format(pq(e).text()) + ':markdown:'
            html = html.replace(str(pq(e)), inline_md)

      # Prepare regex to search for Markdown
      r = re.compile(r":markdown:([\s\S]*?):markdown:")

      # Extract generated Markdown from HTML
      for md in r.finditer(html):
        markdown += md.group(1) + '\n'

  return markdown.strip()

def main():
  argc = len(sys.argv)

  f = sys.argv[1] if argc > 1 else '.markoutrc.json'

  try:
    with open(f, 'r') as opt_file:
      contents = json.loads(opt_file.read())
  except FileNotFoundError:
    print('Error: File not accessible!')

  tokens = contents['tokens'] if contents is not None else {'p': "{}"}
  only_on = contents['only_on'] if contents is not None else 'body'
  links = contents['links'] if contents is not None else {'https://docs.python.org/3/': 'out.md'}

  # Iterate through each link and write out the results
  for link in links.keys():
    f = links[link] or 'out/out.md'

    try:
      os.makedirs(os.path.dirname(f), exist_ok=True)
      with open(f, 'w+') as dest_file:
        dest_file.write(extract_markdown(link, tokens, only_on))
    except IsADirectoryError:
      print('Error: This is not a file!')

if __name__ == '__main__':
  main()
