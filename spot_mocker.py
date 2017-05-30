#! /usr/bin/env python

""" ss_req.py - super simple script to make a request to spotseeker_server.
"""
import secrets
import description
import requests
import os
import errno
import json
import time
import random
from requests_oauthlib import OAuth1

# path of where to store the mock data
mock_path = secrets.MOCK_PATH

# storing data to generate field names
names = []
foods = []
places = []
items = []


# returns a random owner name
def get_name():
	owner = ""
	owner = random.choice(names)
	return owner

# returns a random spot of the passed space_type
def get_item(space_type):
	spot = ""
	if space_type == "Study":
		spot = random.choice(places)
	elif space_type == "Tech":
		spot = random.choice(items)
	else:
		spot = random.choice(foods)
	return spot

# replaces name with new custom one, and replaces other sensitive info
def scrub(item, item_type=""):
	#images, location[building_name]
	owner = get_name()
	item_type = get_item(item_type)
	print owner
	item['name'] = owner + "\'s " + item_type 
	print item['name']
	item['extended_info']['s_website_url'] = 'https://www.google.com'
	item['extended_info']['s_phone'] = '5555555555'
	item['extended_info']['s_support_email'] = 'helloworld@uw.edu'
	item['extended_info']['owner'] = owner
	item['extended_info']['manager'] = owner
	item['extended_info']['s_description'] = 'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.'
	return item

# Builds up info for mock data from the txt files
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

def make_sure_path_exists(path):
    try:
        os.makedirs(path)
    except OSError as exception:
        if exception.errno != errno.EEXIST:
            raise


def create(item, item_type, items=[]):
	if item_type != "Tech":
		clean_space = scrub(item, item_type);
		spot_id = item['id']
		 # writing the detail of that item/file
		make_sure_path_exists(mock_path + "/api/v1/spot/")
		mock_spot_file = open(mock_path + "/api/v1/spot/" + str(spot_id), 'w+')
		mock_spot_file.write(json.dumps(item))
		# print clean_space
		print ""
		items.append(clean_space)
	else:
		tech_items = item["items"]
		ids = []
		scrubbed_items = []
		for i in xrange(0, len(tech_items) -1):
			tech_item = tech_items[i]
			clean_space = scrub(tech_item, item_type);
			spot_id = tech_item['id']
			ids.append(spot_id)
			scrubbed_items.append(clean_space)
		for i in ids:
			test = mock_path + "/api/v1/spot?item%3Aid=" + str(i) + "&extended_info%3Aapp_type=tech"
			# print tech_item
			mock_spot_file = open(test, 'w+')
			mock_spot_file.write(json.dumps([item]))
		item["items"] = scrubbed_items
		items.append(item)

def main():
	gather()
	auth = OAuth1(secrets.KEY, secrets.SECRET)
	if not os.path.exists(mock_path):
		print "Make sure you put in a valid path to put the mock data within your secrets.py!"
		return False
	print "Enter 1: generate mock data from a URL (discover cards/filter results)"
	print "Enter 2: to generate a set of mock data (list of food/study/tech along with their individual detail pages)"
	ch = input()
	if ch == 1:
		item_type = raw_input("First things first: What kind of spots are we viewing here (Food, Tech, Study)? ")
		url = raw_input("What's the URL? ")
		data = []
		try:
			print "Gathering data..."
			resp = requests.get(secrets.URL + url, auth=auth)
			data = json.loads(resp.content)
		except:
			print "Invalid URL"
			return
		print "Scrubbing..."
		for d in data:
			create(d, item_type)
		print "Saving..."
		make_sure_path_exists(mock_path + url)
		mock_spot_file = open(mock_path + url, 'w+')
		mock_spot_file.write(json.dumps(data))
		print "Successfully wrote file?"


	else:
		print "How many Food/Study/Tech locations would you like?"
		num = input()
		make_sure_path_exists(mock_path + "/api/v1/spot/")
		for item_type, url in secrets.ITEMS.iteritems():
			print "Generating spots for... " + item_type
			mock_file_path = mock_path + url
			mock_file = open(mock_file_path, 'w+')
			resp = requests.get(secrets.URL + url, auth=auth)
			data = json.loads(resp.content);
			indexes = random.sample(range(0, len(data) - 1), min(num, len(data) - 1))
			items = []
			for index in indexes:
				# study/food/tech space
				item = data[index]
				create(item, item_type, items)
			mock_file.write(json.dumps(items))

if __name__ == '__main__':
    out = main()
    print 
