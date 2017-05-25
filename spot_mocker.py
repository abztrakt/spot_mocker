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
mock_path = secrets.MOCK_PATH

names = []
foods = []
places = []
items = []

def get_name():
	owner = ""
	owner = random.choice(names)
	return owner


def get_item(space_type):
	m = ""
	if space_type == "Study":
		m = random.choice(places)
	elif space_type == "Tech":
		m = random.choice(items)
	else:
		m = random.choice(foods)
	return m

def scrub(item, item_type):
	#name, s_website_url, s_phone, s_support_email, owner, manager, images, location[building_name]
	owner = get_name()
	item_type = get_item(item_type)
	item['name'] = owner + "\'s " + item_type 
	print item['name']
	return item

def gather():
	dir_path = os.path.dirname(os.path.realpath(__file__))
	names_file = open(dir_path + "/names.txt", 'r')
	global names
	names = (filter(None, names + names_file.read().split('\n')))
	foods_file = open(dir_path + "/foods.txt", 'r')
	global foods
	foods = (filter(None, foods + foods_file.read().split('\n')))
	places_file = open(dir_path + "/places.txt", 'r')
	global places
	places = (filter(None, places + places_file.read().split('\n')))
	items_file = open(dir_path + "/items.txt", 'r')
	global items
	items = (filter(None, items + items_file.read().split('\n')))

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
		data = json.loads(resp.content);
		indexes = random.sample(range(0, len(data) - 1), min(num, len(data)))
		items = []
		for index in indexes:
			# study/food/tech space
			item = data[index]
			clean_space = scrub(item, item_type);
			# print clean_space
			print ""
			print ""
			items.append(clean_space)

		mock_file.write(json.dumps(items))

if __name__ == '__main__':
    out = main()
