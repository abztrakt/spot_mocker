#! /usr/bin/env python

""" ss_req.py - super simple script to make a request to spotseeker_server.
"""
import secrets
import requests
import os
import json
import time
import random
from requests_oauthlib import OAuth1

# path of where to store the mock data
mock_path = "/home/kevin/Desktop/scout-vagrant/venv/src/scout/scout/resources/spotseeker/file"

names = []
foods = []
places = []

def scrub(item):
	#name, s_website_url, s_phone, s_support_email, owner, manager, images, location[building_name]
	print item.get('name')
	print item.get('s_website_url')
	return item

def gather():
	dir_path = os.path.dirname(os.path.realpath(__file__))
	names_file = open(dir_path + "/names.txt", 'r')
	names = names_file.read().split('\n')
	foods_file = open(dir_path + "/foods.txt", 'r')
	foods = foods_file.read().split('\n')
	places_file = open(dir_path + "/places.txt", 'r')
	places = places_file.read().split('\n')

def main():
	gather()
   	auth = OAuth1(secrets.KEY, secrets.SECRET)
   	print "How many Food/Study/Tech spots would you like?"
   	num = input();
	for item_type, url in secrets.ITEMS.iteritems():
		print "Generating spots for... " + item_type
		mock_file_path = mock_path + url
		mock_file = open(mock_file_path, 'w+')
		resp = requests.get(secrets.URL + url, auth=auth)
		print len(resp.content)
		data = json.loads(resp.content);
		indexes = random.sample(range(0, len(data) - 1), min(num, len(data)))
		items = []
		for index in indexes:
			# study/food/tech space
			item = data[index]
			clean_space = scrub(item);
			# print clean_space
			print ""
			print ""
			items.append(clean_space)

		mock_file.write(json.dumps(items))

if __name__ == '__main__':
    out = main()
