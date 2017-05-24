#! /usr/bin/env python

""" ss_req.py - super simple script to make a request to spotseeker_server.
"""
import secrets
import requests
from requests_oauthlib import OAuth1

def main():
    url = secrets.URL
    auth = OAuth1(secrets.KEY, secrets.SECRET)

    resp = requests.get(url, auth=auth)
    return resp.content

if __name__ == '__main__':
    out = main()
    print out
