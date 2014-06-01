# !/usr/bin/evn python
# -*- coding: utf8 -*-
'''
Name: 黃啟軒
Student nubmer: F84004022

-python version: 2.7.3

-purpose:
	use 'regular_expression' to parse real-price housing information to count 
	the highest sale price and lowest sale price of max_distinct_month road in city

-argurments:
	1. url, such as http://www.datagarage.io/api/5365dee31bc6e9d9463a0057 
'''

import re
import  sys
import json
import urllib2

# class road record the road_name month_list price_list
class road:
	
	def __init__(self, road_name):
		self.road_name = road_name
		self.month_list = []
		self.price_list = []

	def insertItem(self, month, price):
		if month not in self.month_list:
			self.month_list.append( month )
		self.price_list.append( price )

	def getPriceList(self):
		return self.price_list

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

def getRoadData(data):

	# find the road in a city has house trading
	# records spreading in max_sidtinct_month
	
	tw_road_area = unicode("土地區段位置或建物區門牌", "utf-8")
	tw_year_month = unicode("交易年月", "utf-8")
	tw_price = unicode("總價元", "utf-8")

	# regular expression 	
	pattern = re.compile( "(.+路)|(.+大道)|(.+街)" ) # priority first
	pattern2 = re.compile( "(.+巷)" )                # if first is not match

	# match road data
	road_dic = {}
	for datum in data:
		# check data format is correct
		if tw_road_area in datum and tw_year_month in datum and tw_price in datum:
			# pattern match
			match = pattern.search( datum[tw_road_area].encode("utf8") )
			if not match:
				match = pattern2.search( datum[tw_road_area].encode("utf8") )
			if match:	
				if match.group() not in road_dic:
					road_dic[ match.group() ]  = road( match.group() )
				road_dic[ match.group() ].insertItem( datum[tw_year_month], datum[tw_price] )
		else:
			print "Error json format is not match!" 
			sys.exit(0)
	

	return road_dic

def maxDictMonRoad( road_data ):

	# sort the result to find the highest distinct_month road 
	# and print the hightest sale price and lowest sale price

	# if road data is none
	if len(road_data) == 0:
		return -1;

	# sort
	sortedlist = sorted(road_data, key = lambda k: len( road_data[k].month_list ), reverse=True)
	max_len = len( road_data[sortedlist[0]].month_list )
	result_list = []
	for road_name in sortedlist:
		if len(road_data[road_name].month_list) == max_len:
			result_list.append( road_data[road_name] )
	
	for road in result_list:
		print "\"" + road.road_name + ", 最高成交價:"+ str(max(road.price_list))  + ", 最低成交價:"+ str( min(road.price_list) ) +"\""

# run program
if len( sys.argv ) == 2:
	print __doc__
	print "URL:", sys.argv[1]
	data = getData()
	road_data = getRoadData(data)
	maxDictMonRoad( road_data )
else:
	print "ERROR len(argv) should be 2"



