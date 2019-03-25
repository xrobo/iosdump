#!/usr/bin/python

import sys
import os
import re
from datetime import datetime

storage = "/srv/iosdump/data/dumps"
archive = "/srv/iosdump/data/archive"


def page(code, body=None):
    html = 'Status: ' + str(code) + '\n' + \
           'Content-Type: text/plain' + '\n\n' + \
           body
    print html
    sys.exit(0)


def backup(hostname):
    arcdir = archive + '/' + hostname
    arcfile = arcdir + '/' + hostname + '_' + \
        datetime.now().strftime("%Y.%m.%d.%H%M%S") + '.conf'
    curfile = storage + '/' + hostname + '.conf'
    if os.path.exists(curfile):
        if not os.path.exists(arcdir):
            os.mkdir(arcdir)
        os.rename(curfile, arcfile)


def catch():
    postdata = sys.stdin.read()
    if len(postdata) > 100000:
        page(500, "Content body too long")
    hostname = get_hostname(postdata)
    backup(hostname)
    fh = open(storage + '/' + hostname + '.conf', "w")
    fh.write(postdata)
    fh.close()
    page(201, 'saved')


def get_hostname(postdata):
    match = re.search('hostname (\w+)', postdata)
    if match:
        return match.group(1)
    else:
        return 'unknown'


def main():
    method = os.environ.get('REQUEST_METHOD')
    if method:
        if method == 'POST':
            catch()
        else:
            page(405, 'This URI should be used with a POST method only')
    else:
        print 'This is a CGI-script that should be run using a web-client'


if __name__ == "__main__":
    main()
