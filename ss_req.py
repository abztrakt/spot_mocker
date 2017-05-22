#! /usr/bin/env python

""" ss_req.py - super simple script to make a request to spotseeker_server.
"""
import settings
import requests
from requests_oauthlib import OAuth1

def main():
    url = settings.URL
    auth = OAuth1(settings.KEY, settings.SECRET)

    resp = requests.get(url, auth=auth)
    return resp.content

if __name__ == '__main__':
    out = main()
    print out
