
import sys
import os
import getopt
import pdb
import json
import pymongo
from pymongo import Connection

###############################################################################
# Parse_Args()
###############################################################################
def Parse_Args(cfg):

    json = {
            "url": "",
            "date_str": "",
	    "date": {"start": "", "end": ""},
	    "region": "",
	    "windows_concurrent_builds": [],
	    "linux_concurrent_builds": [],
	    "daily_stats": { 
			     "builds": {"submitted": "", "completed": "", "submitted_and_completed_same_day": "", "failed": "", "windows_wait": "", "linux_wait": "" }, 
			     "tests": {"submitted": "", "completed": "", "submitted_and_completed_same_day": "", "failed": "", "windows_wait": "", "linux_wait": "" } 
			   },
	    "durations_and_overhead": {
					  "windows_build": {"duration_mean": "", "duration_median": "", "overhead_mean": "", "overhead_median": ""},
					  "linux_build" : {"duration_mean": "", "duration_median": "", "overhead_mean": "", "overhead_median": ""},
					  "windows_install": {"duration_mean": "", "duration_median": "", "overhead_mean": "", "overhead_median": ""},
					  "linux_install": {"duration_mean": "", "duration_median": "", "overhead_mean": "", "overhead_median": ""},
					  "fiery_test": {"duration_mean": "", "duration_median": "", "overhead_mean": "", "overhead_median": ""}
				      },
	    "builds_completed_submitted":{"builds_completed": [], "builds_submitted": [] },
	    "tests_completed_submitted":{"tests_completed": [], "tests_submitted" : [] },
	    "median_build_durations_minutes": { "windows": [], "linux": [] },
	    "mean_median_processing_lead_time_minutes": {"mean_lead_time": [], "median_lead_time": [] }
    }

    obj = { "err": 0, "msg": "", "html": "", "index" : 0 ,"region" : "", "date" : "", "json": json }
   
    try:
        cfg.pop(0)
	argv = cfg
        if len(argv) <= 0:
            msg = "Error: 14\nNeed command line arguments for test to function."
            Shut_Down( 14, msg, True, True )

        opts, argv = getopt.getopt(argv,"hR:D:", ["help", "region=", "date="])

    except getopt.GetoptError: 
        msg = "*** Unknown argument passed in the command line ***\n"
        msg = msg + " " + str(sys.exc_info()[0])
        Shut_Down( 23, msg, True, True )

    for o, a in opts:
        if o in ("-h", "--help"):
	    msg = ""
            Shut_Down( 0, msg, False, True )
        elif o in ("-R", "--region"):
            obj['region'] = a
	    obj['json']['region'] = a
        elif o in ("-D", "--date"):
            obj['date'] = a
	    obj['json']['date_str'] = a
        else:
            msg = "\nError: 23\nUnknown argument passed in the command line...\n"
            Shut_Down( 23, msg, True, True )
    #end for    

    #----------------------------------
    # CHECK variables: Must have region and date
    if obj['region'] == '':
        msg = "ERROR: 15\nMissing region"
        Shut_Down( 15, msg, True, True ) 
    if obj['date'] == '':
        msg = "ERROR: 16\nMissing date"
        Shut_Down( 16, msg, True, True )
 
    return obj
#end

###############################################################################
# Shut_Down:
###############################################################################
def Shut_Down(err, msg, show_err, show_use):

    if show_err == True:
        ret_str = Error(msg)
        print ret_str

    if show_use == True:
        ret_str = Usage()
        print ret_str

    print str(err)+" "+msg
    sys.exit(err)
#end

###############################################################################
# Error:
###############################################################################
def Error(err):
    msg = """
-------------------------------------------------------------------------------
                              MAD COW ALERT:
-------------------------------------------------------------------------------

					       /;    ;\\
					   __  \\\____//
					  /{_\_/   `'\____
					  \___   (o)  (o  }
	       _____________________________/          :--'   
	   ,-,'`@@@@@@@@       @@@@@@         \_    `__\\
	  ;:(  @@@@@@@@@        @@@             \___(o'o)
	  :: )  @@@@          @@@@@@        ,'@@(  `===='        
	  :: : @@@@@:          @@@@         `@@@:
	  :: \  @@@@@:       @@@@@@@)    (  '@@@'
	  ;; /\      /`,    @@@@@@@@@\   :@@@@@)                   
	  ::/  )    {_----------------:  :~`,~~;
	 ;;'`; :   )                  :  / `; ;
	;;;; : :   ;                  :  ;  ; :                       
	`'`' / :  :                   :  :  : :
	    )_ \__;      ";"          :_ ;  \_\       `,','
	    :__\  \    * `,'*         \  \  :  \   *  8`;'*  *
		`^'     \ :/           `^'  `-^-'   \\v/ :  \/   

-------------------------------------------------------------------------------               
"""+str(err)+"""
-------------------------------------------------------------------------------
"""
    return msg
#end Error()

###############################################################################
# Usage:
###############################################################################
def Usage():
    msg = """
-------------------------------------------------------------------------------
Calculus_Scrapper: Usage() 
-------------------------------------------------------------------------------

OPTIONS:

-------------------------------------------------------------------------------
EXIT CODES:
-------------------------------------------------------------------------------
0             No Errors Were Detected.
14            Missing command line args.
15            Missing 'region'
16            Missing 'date'
-------------------------------------------------------------------------------
"""
    return msg
#end Usage()

###############################################################################
# Get_HTML:
###############################################################################
def Get_HTML(obj):
    try:
        url = "http://calculus.efi.com/charts/loads?region="+obj['region']+"&start="+obj['date']
	obj['json']['url'] = url
        cmd = "curl 'http://calculus.efi.com/charts/loads?region="+obj['region']+"&start="+obj['date']+"'"
        result = os.popen(cmd).read()
        obj['html'] = result
    except:
        obj['err'] = 17
	obj['msg'] = "ERROR: 17\nCan't read URL"
    return obj
#end

def Set_Dates(obj):
    try:
        next_line = 0
        arr = obj['html'].split('\n')
        for line in arr:
	    if next_line == 1:
	        #    <h2>loads for Fremont between Sun 06/12/2016 and Mon 06/13/2016</h2>
	        text = "between "
		location = line.find(text)
                date = line[location + 8:-5].split(" and ")
		obj['json']['date']['start'] = date[0]
		obj['json']['date']['end'] = date[1]
                break            
	    else:
	        if "matroshka" in line:
	            next_line = 1 
    except:
        obj['err'] = 18
	obj['msg'] = "ERROR: 18\nCan't read dates"
    return obj
#end

def Set_Windows_Concurrent_Builds(obj):
    try:
        next_line = 0
	arr = obj['html'].split('\n')
	for line in arr:
	    if next_line == 1:
		text = "chd=t:"
                location = line.find(text)
		line = line[location + 6:]
		text = "&amp"
		location = line.find(text)
		line = line[:location]
                obj['json']['windows_concurrent_builds'] = line.split(',')
		break
            else:
	        if "windows concurrent builds" in line:
		    next_line = 1
    except:
        obj['err'] = 19
	obj['msg'] = "ERROR: 19\nCan't read Windows Concurrent Builds"
    return obj
#end

def Set_Linux_Concurrent_Builds(obj):
    try:
        next_line = 0
	arr = obj['html'].split('\n')
	for line in arr:
	    if next_line == 1:
		text = "chd=t:"
                location = line.find(text)
		line = line[location + 6:]
		text = "&amp"
		location = line.find(text)
		line = line[:location]
                obj['json']['linux_concurrent_builds'] = line.split(',')
		break
            else:
	        if "linux concurrent builds" in line:
		    next_line = 1
    except:
        obj['err'] = 20
	obj['msg'] = "ERROR: 20\nCan't read Linux Concurrent Builds"
    return obj
#end

def Set_Daily_Stats_Builds(obj):
    try:
        #<td class="td-left">builds:</td> #32 length
	arr = obj['html'].split('\n')
	for line in arr:
            if '<td class="td-left">builds:</td><td>' in line:
		text = '<td class="td-left">builds:</td><td>'
		location = line.find(text)
		line = line[location + 36:-5]
		line = line.replace('</td>', '')
		arr = line.split('<td>')
		obj['json']['daily_stats']['builds']['submitted'] = arr[0]
		obj['json']['daily_stats']['builds']['completed'] = arr[1]
		obj['json']['daily_stats']['builds']['submitted_and_completed_same_day'] = arr[2]
		obj['json']['daily_stats']['builds']['failed'] = arr[3]
		obj['json']['daily_stats']['builds']['windows_wait'] = arr[4]
		obj['json']['daily_stats']['builds']['linux_wait'] = arr[5]
		break
    except:
        obj['err'] = 21
	obj['msg'] = "ERROR: 21\nCan't read Daily Stats: Builds"

    return obj
#end

def Set_Daily_Stats_Tests(obj):
    try:
        #<td class="td-left">tests:</td><td>
	arr = obj['html'].split('\n')
	for line in arr:
            if '<td class="td-left">tests:</td><td>' in line:
		text = '<td class="td-left">tests:</td><td>'
		location = line.find(text)
		line = line[location + 35:-5]
		line = line.replace('</td>', '')
		arr = line.split('<td>')
		obj['json']['daily_stats']['tests']['submitted'] = arr[0]
		obj['json']['daily_stats']['tests']['completed'] = arr[1]
		obj['json']['daily_stats']['tests']['submitted_and_completed_same_day'] = arr[2]
		obj['json']['daily_stats']['tests']['failed'] = arr[3]
		obj['json']['daily_stats']['tests']['windows_wait'] = arr[4]
		obj['json']['daily_stats']['tests']['linux_wait'] = arr[5]
		break
    except:
        obj['err'] = 22
	obj['msg'] = "ERROR: 22\nCan't read Daily Stats: Tests"

    return obj
#end

def Set_Durations_And_Overhead_Windows_Build(obj):
    try:
        #<td class="td-left">windows build:</td><td>
        arr = obj['html'].split('\n')
	for line in arr:
            if '<td class="td-left">windows build:</td><td>' in line:
		text = '<td class="td-left">windows build:</td><td>'
		location = line.find(text)
		line = line[location + len(text):-5]
		line = line.replace('</td>', '').replace(' minutes', '')
		arr = line.split('<td>')
		obj['json']['durations_and_overhead']['windows_build']['duration_mean'] = int(arr[0])
		obj['json']['durations_and_overhead']['windows_build']['duration_median'] = int(arr[1])
		obj['json']['durations_and_overhead']['windows_build']['overhead_mean'] = int(arr[2])
		obj['json']['durations_and_overhead']['windows_build']['overhead_median'] = int(arr[3])
		break
    except:
        obj['err'] = 23
	obj['msg'] = "ERROR: 23\nCan't read Durations And Overhead: Windows Build"

    return obj	
#end

def Set_Durations_And_Overhead_Linux_Build(obj):
    try:
        #<td class="td-left">windows build:</td><td>
        arr = obj['html'].split('\n')
	for line in arr:
            if '<td class="td-left">linux build:</td><td>' in line:
		text = '<td class="td-left">linux build:</td><td>'
		location = line.find(text)
		line = line[location + len(text):-5]
		line = line.replace('</td>', '').replace(' minutes', '')
		arr = line.split('<td>')
		obj['json']['durations_and_overhead']['linux_build']['duration_mean'] = int(arr[0])
		obj['json']['durations_and_overhead']['linux_build']['duration_median'] = int(arr[1])
		obj['json']['durations_and_overhead']['linux_build']['overhead_mean'] = int(arr[2])
		obj['json']['durations_and_overhead']['linux_build']['overhead_median'] = int(arr[3])
		break
    except:
        obj['err'] = 24
	obj['msg'] = "ERROR: 24\nCan't read Durations And Overhead: Linux Build"

    return obj	
#end

def Set_Durations_And_Overhead_Windows_Install(obj):
    try:
        arr = obj['html'].split('\n')
	for line in arr:
            if '<td class="td-left">windows install:</td><td>' in line:
		text = '<td class="td-left">windows install:</td><td>'
		location = line.find(text)
		line = line[location + len(text):-5]
		line = line.replace('</td>', '').replace(' minutes', '')
		arr = line.split('<td>')
		obj['json']['durations_and_overhead']['windows_install']['duration_mean'] = int(arr[0])
		obj['json']['durations_and_overhead']['windows_install']['duration_median'] = int(arr[1])
		obj['json']['durations_and_overhead']['windows_install']['overhead_mean'] = int(arr[2])
		obj['json']['durations_and_overhead']['windows_install']['overhead_median'] = int(arr[3])
		break
    except:
        obj['err'] = 25
	obj['msg'] = "ERROR: 25\nCan't read Durations And Overhead: Windows Install"

    return obj	

#end

def Set_Durations_And_Overhead_Linux_Install(obj):
    try:
        arr = obj['html'].split('\n')
	for line in arr:
            if '<td class="td-left">linux install:</td><td>' in line:
		text = '<td class="td-left">linux install:</td><td>'
		location = line.find(text)
		line = line[location + len(text):-5]
		line = line.replace('</td>', '').replace(' minutes', '')
		arr = line.split('<td>')
		obj['json']['durations_and_overhead']['linux_install']['duration_mean'] = int(arr[0])
		obj['json']['durations_and_overhead']['linux_install']['duration_median'] = int(arr[1])
		obj['json']['durations_and_overhead']['linux_install']['overhead_mean'] = int(arr[2])
		obj['json']['durations_and_overhead']['linux_install']['overhead_median'] = int(arr[3])
		break
    except:
        obj['err'] = 26
	obj['msg'] = "ERROR: 26\nCan't read Durations And Overhead: Linux Install"

    return obj	
#end

def Set_Durations_And_Overhead_Fiery_Test(obj):
    try:
        arr = obj['html'].split('\n')
	for line in arr:
            if '<td class="td-left">fiery test:</td><td>' in line:
		text = '<td class="td-left">fiery test:</td><td>'
		location = line.find(text)
		line = line[location + len(text):-5]
		line = line.replace('</td>', '').replace(' minutes', '')
		arr = line.split('<td>')
		obj['json']['durations_and_overhead']['fiery_test']['duration_mean'] = arr[0]
		obj['json']['durations_and_overhead']['fiery_test']['duration_median'] = arr[1]
		obj['json']['durations_and_overhead']['fiery_test']['overhead_mean'] = arr[2]
		obj['json']['durations_and_overhead']['fiery_test']['overhead_median'] = arr[3]
		break
    except:
        obj['err'] = 27
	obj['msg'] = "ERROR: 27\nCan't read Durations And Overhead: Fiery Test"

    return obj	
#end

def Set_Builds_Completed_Submitted_Builds_Completed_Builds_Submitted(obj):
    #<h3>builds completed/submitted</h3>
    try:
        next_line = 0
	arr = obj['html'].split('\n')
	for line in arr:
	    if next_line == 1:
		text = "chd=t:"
                location = line.find(text)
		line = line[location + 6:]
		text = "&amp"
		location = line.find(text)
		line = line[:location]
                arr = line.split('|')
		obj['json']['builds_completed_submitted']['builds_completed'] = arr[0].split(',')
		obj['json']['builds_completed_submitted']['builds_submitted'] = arr[1].split(',')
		break
            else:
	        if "builds completed/submitted" in line:
		    next_line = 1
    except:
        obj['err'] = 28 
	obj['msg'] = "ERROR: 28\nCan't read "
    return obj

#end

def Set_Tests_Completed_Submitted_Tests_Completed_Tests_Submitted(obj):
    #<h3>tests completed/submitted</h3>
    try:
        next_line = 0
	arr = obj['html'].split('\n')
	for line in arr:
	    if next_line == 1:
		text = "chd=t:"
                location = line.find(text)
		line = line[location + 6:]
		text = "&amp"
		location = line.find(text)
		line = line[:location]
                arr = line.split('|')
		obj['json']['tests_completed_submitted']['tests_completed'] = arr[0].split(',')
		obj['json']['tests_completed_submitted']['tests_submitted'] = arr[1].split(',')
		break
            else:
	        if "tests completed/submitted" in line:
		    next_line = 1
    except:
        obj['err'] = 28 
	obj['msg'] = "ERROR: 28\nCan't read "
    return obj

#end

def Set_Median_Build_Durations_Minutes_Windows_Linux(obj):
    try:
        next_line = 0
	arr = obj['html'].split('\n')
	for line in arr:
	    if next_line == 1:
		text = "chd=t:"
                location = line.find(text)
		line = line[location + 6:]
		text = "&amp"
		location = line.find(text)
		line = line[:location]
                arr = line.split('|')
		obj['json']['median_build_durations_minutes']['windows'] = arr[0].split(',')
		obj['json']['median_build_durations_minutes']['linux'] = arr[1].split(',')
		break
            else:
	        if "median build durations (minutes)" in line:
		    next_line = 1
    except:
        obj['err'] = 28 
	obj['msg'] = "ERROR: 28\nCan't read "
    return obj
#end

def Set_Mean_Median_Processing_Lead_Time_Minutes_Mean_Lead_Time_Median_Lead_Time(obj):
    try:
        next_line = 0
	arr = obj['html'].split('\n')
	for line in arr:
	    if next_line == 1:
		text = "chd=t:"
                location = line.find(text)
		line = line[location + 6:]
		text = "&amp"
		location = line.find(text)
		line = line[:location]
                arr = line.split('|')
		obj['json']['mean_median_processing_lead_time_minutes']['mean_lead_time'] = arr[0].split(',')
		obj['json']['mean_median_processing_lead_time_minutes']['median_lead_time'] = arr[1].split(',')
		break
            else:
	        if "mean/median processing lead time (minutes)" in line:
		    next_line = 1
    except:
        obj['err'] = 28 
	obj['msg'] = "ERROR: 28\nCan't read "
    return obj

#end

def Write_To_MongoDB(obj):
    try:
        json_dump = json.dumps(obj['json'], indent=4, sort_keys=True )
	connection = Connection()
        db = connection.calculus #define db here...
        collection = db.collection
	collection.insert(obj['json'])
        print "Inserted data into DB"
        #mongo = collection.find({"region": "Fremont" })
	#mongo = collection.find({'date.start': 'Wed 06/01/2016'})
        #for index in mongo:
	#    print index
    except:
        obj['err'] = 33
	obj['msg'] = "ERROR: 33\nCan't write to database "+ str(sys.exc_info()[0])
    return obj
#end


###############################################################################
# Main method
###############################################################################
def Main():
    #----------------------------------
    # Setup and parse command line args
    cfg = sys.argv
    obj = Parse_Args(cfg)

    #----------------------------------
    # Build URL
    obj = Get_HTML(obj)
    if obj['err'] != 0:
        Shut_Down(obj['err'], obj['msg'], True, True )

    obj = Set_Dates(obj)
    if obj['err'] != 0:
        Shut_Down(obj['err'], obj['msg'], True, True )

    obj = Set_Windows_Concurrent_Builds(obj)
    if obj['err'] != 0:
        Shut_Down(obj['err'], obj['msg'], True, True )

    obj = Set_Linux_Concurrent_Builds(obj)
    if obj['err'] != 0:
        Shut_Down(obj['err'], obj['msg'], True, True )

    obj = Set_Daily_Stats_Builds(obj)
    if obj['err'] != 0:
        Shut_Down(obj['err'], obj['msg'], True, True )

    obj = Set_Daily_Stats_Tests(obj)
    if obj['err'] != 0:
        Shut_Down(obj['err'], obj['msg'], True, True )

    obj = Set_Durations_And_Overhead_Windows_Build(obj)
    if obj['err'] != 0:
        Shut_Down(obj['err'], obj['msg'], True, True )

    obj = Set_Durations_And_Overhead_Linux_Build(obj)
    if obj['err'] != 0:
        Shut_Down(obj['err'], obj['msg'], True, True )

    obj = Set_Durations_And_Overhead_Windows_Install(obj)
    if obj['err'] != 0:
        Shut_Down(obj['err'], obj['msg'], True, True )
  
    obj = Set_Durations_And_Overhead_Linux_Install(obj)
    if obj['err'] != 0:
        Shut_Down(obj['err'], obj['msg'], True, True )
   
    obj = Set_Durations_And_Overhead_Fiery_Test(obj)
    if obj['err'] != 0:
        Shut_Down(obj['err'], obj['msg'], True, True )
   
    obj = Set_Builds_Completed_Submitted_Builds_Completed_Builds_Submitted(obj)  
    if obj['err'] != 0:
        Shut_Down(obj['err'], obj['msg'], True, True )

    obj = Set_Tests_Completed_Submitted_Tests_Completed_Tests_Submitted(obj)
    if obj['err'] != 0:
        Shut_Down(obj['err'], obj['msg'], True, True )
 
    obj = Set_Median_Build_Durations_Minutes_Windows_Linux(obj)
    if obj['err'] != 0:
        Shut_Down(obj['err'], obj['msg'], True, True )    
 
    obj = Set_Mean_Median_Processing_Lead_Time_Minutes_Mean_Lead_Time_Median_Lead_Time(obj)
    if obj['err'] != 0:
        Shut_Down(obj['err'], obj['msg'], True, True )

    obj = Write_To_MongoDB(obj)
    if obj['err'] != 0:
        Shut_Down(obj['err'], obj['msg'], True, True )

    #json_dump = json.dumps(obj['json'], indent=4, sort_keys=True )
    #print json_dump 
#end

#--------------------------------------
# MAIN ENTRY POINT INTO SCRIPT
if __name__ == "__main__":
    Main()
