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

# replaces name with new custom one
def scrub(item, item_type):
	#name, s_website_url, s_phone, s_support_email, owner, manager, images, location[building_name]
	owner = get_name()
	item_type = get_item(item_type)

	item['name'] = owner + "\'s " + item_type 
	print item['name']
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

def main():
	gather()
	print "How many Food/Study/Tech locations would you like?"
	num = input()
	print "How many Tech items do you want at each location?"
	tech_num = input()
	for item_type, url in secrets.ITEMS.iteritems():
		print "Generating spots for... " + item_type
		mock_file_path = mock_path + url
		mock_file = open(mock_file_path, 'w+')
		resp = requests.get(secrets.URL + url, auth=auth)
		data = json.loads(resp.content);
		indexes = []
		for i in xrange(0, num):
			indexes.append(random.randint(0, len(data) - 1))
		items = []
		for index in indexes:
			# study/food/tech space
			item = data[index]
			if item_type != "Tech":
				clean_space = scrub(item, item_type);
				spot_id = item['id']
				 # writing the detail of that item/file
				mock_spot_file = open(mock_path + "/api/v1/spot/" + str(spot_id), 'w+')
				mock_spot_file.write(json.dumps(item))
				# print clean_space
				print ""
				items.append(clean_space)
			else:
				tech_items = item["items"]
				tech_indexes = []
				ids = []
				for i in xrange(0, tech_num):
					tech_indexes.append(random.randint(0, len(tech_items) - 1))
				scrubbed_items = []
				for i in tech_indexes:
					tech_item = tech_items[i]
					clean_space = scrub(tech_item, item_type);
					spot_id = tech_item['id']
					ids.append(spot_id)
					scrubbed_items.append(clean_space)
				for i in ids:
					test = mock_path + "/api/v1/spot?item%3Aid=" + str(i) + "&extended_info%3Aapp_type=tech"
					# print tech_item
					mock_spot_file = open(test, 'w+')
					print json.dumps([item])
					print " "
					mock_spot_file.write(json.dumps([item]))

				item["items"] = scrubbed_items
				items.append(item)
		print len(items)
		mock_file.write(json.dumps(items))

if __name__ == '__main__':
    out = main()
    print 
