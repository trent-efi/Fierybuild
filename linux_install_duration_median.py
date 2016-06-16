import sys
import os
import pymongo
from pymongo import Connection
import pdb
import csv

def Main():
    #date   = sys.argv[1]
    #region = sys.argv[1]
    obj = {'date': ["date"], "Fremont": ["Fremont"], "IDC": ["IDC"], "vCommander+Fremont": ["vCommander+Fremont"], "vCommander+IDC": ["vCommander+IDC"]  }
    try:
        connection = Connection()
        db = connection.calculus #define db here...
        collection = db.collection

        #db.collection.find({ "region": "vCommander+Fremont", "date_str": "20160612" } )
        #mongo = collection.find({"region": region, "date_str": date } )
        #mongo = collection.find({"region": "Fremont" })
        #mongo = collection.find({"region": "Fremont" }).sort({"date_str": -1})
	mongo = collection.find({"region": "Fremont" }).sort("date_str",pymongo.ASCENDING)
        #mongo = collection.find({'date.start': 'Wed 06/01/2016'})

        for index in mongo:
            obj['date'].append(index['date_str'])
	    obj['Fremont'].append(index['durations_and_overhead']['linux_install']['duration_median'])          

	mongo = collection.find({"region": "IDC" }).sort("date_str",pymongo.ASCENDING)
        for index in mongo:
	    obj['IDC'].append(index['durations_and_overhead']['linux_install']['duration_median'])    

	mongo = collection.find({"region": "vCommander+Fremont" }).sort("date_str",pymongo.ASCENDING)
        for index in mongo:
	    obj['vCommander+Fremont'].append(index['durations_and_overhead']['linux_install']['duration_median'])  

	mongo = collection.find({"region": "vCommander+IDC" }).sort("date_str",pymongo.ASCENDING)
        for index in mongo:
	    obj['vCommander+IDC'].append(index['durations_and_overhead']['linux_install']['duration_median']) 

        myfile = open( 'csv/linux_install_duration_median.csv', 'w')
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


