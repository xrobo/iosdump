#!/usr/bin/python

import sys

srorage="/opt/cisco/dumps"
archive="/opt/cisco/archive"

def page(code, body=None):
  html = 'Status: ' + str(code) + '\n' + \
         'Content-Type: text/plain' + '\n\n' + \
         body
  print html
  sys.exit(0)


def dump():
  input = sys.stdin.read()
  if len(input) > 100000:
    page(500, "Content body too long")
  page(200, input)


def main():
  method = os.environ.get('REQUEST_METHOD')
  if method:
    if method == 'POST':
      dump()
    else:
      page(405, 'This URI should be used with a POST method only')
  else:
    print 'This is a CGI-script that should be run using a web-client'


if __name__=="__main__":
  main()
