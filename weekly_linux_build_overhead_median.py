import sys
import os
import pymongo
from pymongo import Connection
import pdb
import csv
import datetime
from datetime import date
import time


def Main():
    #date   = sys.argv[1]
    #region = sys.argv[1]
    obj = {'date': ["date"], "Fremont": ["Fremont"], "IDC": ["IDC"], "vCommander+Fremont": ["vCommander+Fremont"], "vCommander+IDC": ["vCommander+IDC"]  }
    try:
        connection = Connection()
        db = connection.calculus #define db here...
        collection = db.collection

        weekly_sum = 0
	weekly_num = []

        mongo = collection.find({"region": "Fremont" }).sort("date_str",pymongo.ASCENDING)
        for index in mongo:
	    date_str = index['date_str']
	    year = int(date_str[:4])
	    month = int(date_str[4:6])
	    day = int(date_str[6:])
            foo_date = date(year, month, day)

	    if foo_date.weekday() == 0:
                obj['date'].append(index['date_str'])
	#end for

        weekly_sum = 0
	weekly_num = []

	mongo = collection.find({"region": "Fremont" }).sort("date_str",pymongo.ASCENDING)
        for index in mongo:
	    date_str = index['date_str']
	    year = int(date_str[:4])
	    month = int(date_str[4:6])
	    day = int(date_str[6:])
            foo_date = date(year, month, day)

            weekly_sum += int(index['durations_and_overhead']['linux_build']['overhead_median'])
            weekly_num.append( int(index['durations_and_overhead']['linux_build']['overhead_median']))

	    if foo_date.weekday() == 0:

	        #median
		
		weekly_num.sort()
		length = len(weekly_num)
                half = int(length/2)
                if length == 1:
                    obj['Fremont'].append(weekly_num[length-1]) 
		elif length % 2 == 0: #even
		    obj['Fremont'].append( (weekly_num[half-1] + weekly_num[half])/2 )
                else: #odd
                    obj['Fremont'].append( weekly_num[half] ) 
                

		#mean
		"""
		length = len(weekly_num)
                obj['Fremont'].append(weekly_sum/length)
                """
 
		weekly_num = []
		weekly_sum = 0
        #end for

        weekly_sum = 0
	weekly_num = []

	mongo = collection.find({"region": "IDC" }).sort("date_str",pymongo.ASCENDING)
        for index in mongo:
	    date_str = index['date_str']
	    year = int(date_str[:4])
	    month = int(date_str[4:6])
	    day = int(date_str[6:])
            foo_date = date(year, month, day)

            weekly_sum += int(index['durations_and_overhead']['linux_build']['overhead_median'])
            weekly_num.append( int(index['durations_and_overhead']['linux_build']['overhead_median']))

	    if foo_date.weekday() == 0:

	        #median
		
		weekly_num.sort()
		length = len(weekly_num)
                half = int(length/2)
                if length == 1:
                    obj['IDC'].append(weekly_num[length-1]) 
		elif length % 2 == 0: #even
		    obj['IDC'].append( (weekly_num[half-1] + weekly_num[half])/2 )
                else: #odd
                    obj['IDC'].append( weekly_num[half] ) 
                

		#mean
		"""
		length = len(weekly_num)
                obj['Fremont'].append(weekly_sum/length)
                """
 
		weekly_num = []
		weekly_sum = 0
        #end for

        weekly_sum = 0
	weekly_num = []

	mongo = collection.find({"region": "vCommander+Fremont" }).sort("date_str",pymongo.ASCENDING)
        for index in mongo:
	    date_str = index['date_str']
	    year = int(date_str[:4])
	    month = int(date_str[4:6])
	    day = int(date_str[6:])
            foo_date = date(year, month, day)

            weekly_sum += int(index['durations_and_overhead']['linux_build']['overhead_median'])
            weekly_num.append( int(index['durations_and_overhead']['linux_build']['overhead_median']))

	    if foo_date.weekday() == 0:

	        #median
		
		weekly_num.sort()
		length = len(weekly_num)
                half = int(length/2)
                if length == 1:
                    obj['vCommander+Fremont'].append(weekly_num[length-1]) 
		elif length % 2 == 0: #even
		    obj['vCommander+Fremont'].append( (weekly_num[half-1] + weekly_num[half])/2 )
                else: #odd
                    obj['vCommander+Fremont'].append( weekly_num[half] ) 
                

		#mean
		"""
		length = len(weekly_num)
                obj['Fremont'].append(weekly_sum/length)
                """
 
		weekly_num = []
		weekly_sum = 0
        #end for
 
        weekly_sum = 0
	weekly_num = []

	mongo = collection.find({"region": "vCommander+IDC" }).sort("date_str",pymongo.ASCENDING)
        for index in mongo:
	    date_str = index['date_str']
	    year = int(date_str[:4])
	    month = int(date_str[4:6])
	    day = int(date_str[6:])
            foo_date = date(year, month, day)

            weekly_sum += int(index['durations_and_overhead']['linux_build']['overhead_median'])
            weekly_num.append( int(index['durations_and_overhead']['linux_build']['overhead_median']))

	    if foo_date.weekday() == 0:

	        #median
		
		weekly_num.sort()
		length = len(weekly_num)
                half = int(length/2)
                if length == 1:
                    obj['vCommander+IDC'].append(weekly_num[length-1]) 
		elif length % 2 == 0: #even
		    obj['vCommander+IDC'].append( (weekly_num[half-1] + weekly_num[half])/2 )
                else: #odd
                    obj['vCommander+IDC'].append( weekly_num[half] ) 
                

		#mean
		"""
		length = len(weekly_num)
                obj['Fremont'].append(weekly_sum/length)
                """
 
		weekly_num = []
		weekly_sum = 0
        #end for

        myfile = open( '/var/www/html/fierybuild/csv/weekly_linux_build_overhead_median.csv', 'w')
        wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
        wr.writerow(obj['date'])
        wr.writerow(obj['Fremont'])
        wr.writerow(obj['IDC'])
        wr.writerow(obj['vCommander+Fremont'])
        wr.writerow(obj['vCommander+IDC'])

    except:
        print "ERROR"

#end

#--------------------------------------
# MAIN ENTRY POINT INTO SCRIPT
if __name__ == "__main__":
    Main()




