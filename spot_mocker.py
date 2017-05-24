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

# path to the server of the spotseeker data
server_url = "http://spotseeker-test-app1.cac.washington.edu"

# path of where to store the mock data
mock_path = "/home/kevin/Desktop/scout-vagrant/venv/src/scout/scout/resources/spotseeker/file"

urls = ['/api/v1/spot?item%3Aextended_info%3Ai_is_active=true&limit=0&extended_info%3Acampus=seattle&extended_info%3Aapp_type=tech', 
        '/api/v1/spot?limit=0&extended_info%3Acampus=seattle&extended_info%3Aapp_type=food', 
        '/api/v1/spot?limit=0&extended_info%3Acampus=seattle&open_now=true']

names = ["Kevin", "Mason", "Craig", "John", "Jim"]
foods = ["Coffee", "Cafe", "Bistro", "Restaurant"]
places = ["Library", "Hallway", "Hall", "Center"]

def scrub(item):
	return item

def main():
   	auth = OAuth1(secrets.KEY, secrets.SECRET)
   	print "How many Food/Study/Tech spots would you like?"
   	num = input();
	for url in urls:
		print "Generating spots for... " + url
		mock_file_path = mock_path + url
		mock_file = open(mock_file_path, 'w+')
		resp = requests.get(server_url + url, auth=auth)
		print len(resp.content)
		data = json.loads(resp.content);
		indexes = random.sample(range(0, len(data) - 1), min(num, len(data)))
		items = []
		for index in indexes:
			# study/food/tech space
			item = data[index]
			clean_space = scrub(item);
			items.append(clean_space)

		mock_file.write(json.dumps(items))

if __name__ == '__main__':
    out = main()
    print out
