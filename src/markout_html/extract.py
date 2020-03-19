#!/usr/bin/env python

"""Markout HTML extraction."""

import sys
import re
import logging
import urllib.request
from pyquery import PyQuery as pq

def extract_html(html, tokens, only_on = 'body'):
  """Extract HTML contents from string to any format using tokens

  Keyword arguments:
  html -- the HTML code string
  tokens -- the list of tokens used to extract HTML contents into the formatted result
  only_on -- only extract contents inside this tag (default 'body')
  """
  result = ''

  # Remove useless content
  d = pq(html)
  d('head').remove()
  html = pq(d(only_on)).html()

  if html is not None:
    d = pq(html)
    for key in tokens.keys():
      for e in d(key):
        # Verify <a> and <img> special tags cases
        if key == 'a':
          inline_md = ':extracted:' + tokens[key].format(pq(e).text(), pq(e).attr('href')) + ':extracted:'
          html = html.replace(str(pq(e)), inline_md)
        elif key == 'img':
          inline_md = ':extracted:' + tokens[key].format(pq(e).attr('alt'), pq(e).attr('src')) + ':extracted:'
          html = html.replace(str(pq(e)), inline_md)
        else:
          inline_md = ':extracted:' + tokens[key].format(pq(e).text()) + ':extracted:'
          html = html.replace(str(pq(e)), inline_md)

    # Prepare regex to search for marked content
    r = re.compile(r":extracted:([\s\S]*?):extracted:")

    # Extract marked HTML contents
    for md in r.finditer(html):
      result += md.group(1) + '\n'

  return result.strip()

def extract_url(url, tokens, only_on = 'body'):
  """Extract HTML contents from web page to any format using tokens.

  Keyword arguments:
  url -- the page address
  tokens -- the list of tokens used to extract HTML contents into the formatted result
  only_on -- only extract contents inside this tag (default 'body')
  """
  result = ''

  if url != '' and tokens != {}:
    # Request and decode HTML page
    req = urllib.request.Request(url)
    try:
      with urllib.request.urlopen(req) as response:
        html = response.read().decode('utf8')
    except urllib.error.HTTPError as e:
      logging.debug('Request error, code:', e.code)
      sys.exit()

    result = extract_html(html, tokens, only_on)

  return result
