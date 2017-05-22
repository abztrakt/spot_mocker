#! /usr/bin/env python

""" ss_req.py - super simple script to make a request to spotseeker_server.
"""
import settings

def main():
    print settings.URL
    print settings.KEY
    print settings.SECRET

if __name__ == '__main__':
    main()
