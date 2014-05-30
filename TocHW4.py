# !/usr/bin/evn python
# -*- coding: utf8 -*-
'''
Name: 黃啟軒
Student nubmer: F84004022

-python version: 2.7.3

'''

import re
import  sys
import json
import urllib2

# use arg1 URL to get json data
def getData():
	
	# make sure that we can get data from server
	try:
		response = urllib2.urlopen( sys.argv[1] )
	except URLError, e:
		if hasattr(e, 'reason'):
			print 'we failed to connect server'
			print e.reason
			sys.exit(0)
		elif hasattr(e, 'code'):
			print 'The server could not fulfill the request'
			print  e.code
			sys.exit(0)

	# convert to json format
	data = json.load( response, encoding = ('utf-8') )	
	
	return data

def maxDistinctMonth(data):
	# find the road in a city has house trading
	# records spreading in max_sidtinct_month
	
	tw_road_area = unicode("土地區段位置或建物區門牌", "utf-8")
	tw_year = unicode("交易年月", "utf-8")
	tw_price = unicode("總價元", "utf-8")
	
	pattern = re.compile( "(.)*(路|街|巷)" )

	

	for datum in data:
		if tw_road_area in datum and tw_year in datum and tw_price in datum:
			match_item = pattern.search( datum[tw_road_area].encode("utf8") )
			if match_item:
				print match_item.group()
		else:
			print "Error json format is not match!" 
			sys.exit(0)


# run program
if len( sys.argv ) == 2:
	print __doc__
	print "URL:", sys.argv[1]
	data = getData()
	maxDistinctMonth(data)
else:
	print "ERROR len(argv) should be 2"


