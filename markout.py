#!/usr/bin/env python3

from pyquery import PyQuery as pq
import urllib.request
import re
import json
import sys
import os

def extract_markdown(url, tokens, only_on = "html"):
  markdown = ""

  if url != "" and tokens != {}:
    # request and decode html page
    req = urllib.request.Request(url)
    try:
      with urllib.request.urlopen(req) as response:
        html = response.read().decode("utf8")
    except urllib.error.HTTPError as e:
      print("Error: Request error, code:", e.code)

    # prepare html document
    d = pq(html)
    d("head").remove()
    html = pq(d(only_on)).html()

    if html is not None:
      d = pq(html)
      for key in tokens.keys():
        # iterate through each element that was set on tokens
        for e in d(key):
          # verify <a> and <img> cases
          if key == "a":
            inline_md = ":markdown:" + tokens[key].format(pq(e).text(), pq(e).attr("href")) + ":markdown:"
            html = html.replace(str(pq(e)), inline_md)
          elif key == "img":
            inline_md = ":markdown:" + tokens[key].format(pq(e).attr("alt"), pq(e).attr("src")) + ":markdown:"
            html = html.replace(str(pq(e)), inline_md)
          else:
            inline_md = ":markdown:" + tokens[key].format(pq(e).text()) + ":markdown:"
            html = html.replace(str(pq(e)), inline_md)

      # prepare regex to search for
      r = re.compile(r":markdown:([\s\S]*?):markdown:")

      # extract markdown from html
      for md in r.finditer(html):
        markdown += md.group(1) + "\n"

  return markdown.strip()

def main():
  argc = len(sys.argv)

  f = sys.argv[1] if argc > 1 else ".markoutrc.json"

  try:
    with open(f, "r") as opt_file:
      contents = json.loads(opt_file.read())
  except FileNotFoundError:
    print("Error: File not accessible!")

  tokens = contents["tokens"] if contents is not None else {"p": "{}"}
  only_on = contents["only_on"] if contents is not None else "body"
  links = contents["links"] if contents is not None else {"https://docs.python.org/3/": "out.md"}

  # iterate through each link and write out the results
  for link in links.keys():
    f = links[link] or "out/out.md"

    try:
      os.makedirs(os.path.dirname(f), exist_ok=True)
      with open(f, "w+") as dest_file:
        dest_file.write(extract_markdown(link, tokens, only_on))
    except IsADirectoryError:
      print("Error: This is not a file!")

if __name__ == "__main__":
  main()
