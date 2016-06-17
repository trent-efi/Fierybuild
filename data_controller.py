import pdb
import os
import time
import datetime
import sys
import getopt

###############################################################################
# Parse_Args()
###############################################################################
def Parse_Args(cfg):
    obj = {'err': 0, 'msg': '', 'region': '', 'start_date': '', 'end_date': ''}

    try:
        cfg.pop(0)
	argv = cfg
        if len(argv) < 2:
            msg = "Error: 14\nNeed command line arguments for test to function."
            Shut_Down( 14, msg, True, True )

        opts, argv = getopt.getopt(argv,"hR:S:E:", ["help", "region=", "start=", "end="])

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
        elif o in ("-S", "--start"):
            obj['start_date'] = a
	elif o in ("-E", "--end"):
	    obj['end_date'] = a
        else:
            msg = "\nError: 23\nUnknown argument passed in the command line...\n"
            Shut_Down( 23, msg, True, True )
    #end for    

    #----------------------------------
    # CHECK variables: Must have region and date
    if obj['region'] == '':
        msg = "ERROR: 15\nMissing region"
        Shut_Down( 15, msg, True, True ) 
    if obj['start_date'] == '':
        msg = "ERROR: 16\nMissing start date"
        Shut_Down( 16, msg, True, True )
    if obj['end_date'] == '':
        msg = "ERROR: 17\nMissing end date"
        Shut_Down( 17, msg, True, True )
        
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
                           SPONGE-BOB!
-------------------------------------------------------------------------------

				   .--'''''''''--.
				.'      .---.      '.
			       /    .-----------.    \\
			      /        .-----.        \\
			      |       .-.   .-.       |
			      |      /   \ /   \      |
			       \    | .-. | .-. |    /
				'-._| | | | | | |_.-'
				    | '-' | '-' |
				     \___/ \___/
				  _.-'  /   \  `-._
				.' _.--|     |--._ '.
				' _...-|     |-..._ '
				       |     |
				       '.___.'
					 | |
					_| |_
				       /\( )/\\
				      /  ` '  \\
				     | |     | |
				     '-'     '-'
				     | |     | |
				     | |     | |
				     | |-----| |
				  .`/  |     | |/`.
				  |    |     |    |
				  '._.'| .-. |'._.'
					\ | /
					| | |
					| | |
					| | |
				       /| | |\\
				     .'_| | |_`.
				     `. | | | .'
				  .    /  |  \    .
				 /o`.-'  / \  `-.`o\\
				/o  o\ .'   `. /o  o\\
				`.___.'       `.___.'



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
Usage() 
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

def Collect_Data(obj):
    try:
        cmd = 'python /var/www/html/fierybuild/calculus_scraper.py --region '+obj['region']+' --date '+obj['start_date']
        result = os.popen(cmd).read()
        if "ERROR" in result:
	    raise Exception("ERROR")
    except:
        obj['err'] = 18
	obj['msg'] = "ERROR: 18\nCouldn't collect data from: " + obj['region'] + " " + obj['start_date']

    return obj
#end

def Parse_To_Date(date):
    year = date[:4]
    mnth = date[4:6]
    days = date[6:8]

    date_obj = datetime.date(int(year), int(mnth), int(days))

    return date_obj
#end

def Parse_To_Str(date):
    year = date.year
    mnth = date.month
    days = date.day

    year_str = str(year)
    mnth_str = ''
    days_str = ''

    #Months
    if mnth < 10:
        mnth_str = "0"+str(mnth)
    else:
        mnth_str = str(mnth)

    #Days
    if days < 10:
        days_str = "0"+str(days)
    else:
        days_str = str(days)

    date_str = year_str + mnth_str + days_str

    return date_str
#end

def Increment_Date_Str(obj):
    #convert to date
    date = Parse_To_Date(obj['start_date'])
    one_day = datetime.timedelta(days=1)
    date = date + one_day

    obj['start_date'] = Parse_To_Str(date)

    return obj
#end

###############################################################################
# Main method
###############################################################################
def Main():
    obj = Parse_Args(sys.argv)
    
    initial_start = obj['start_date']

    start = Parse_To_Date(obj['start_date'])
    end   = Parse_To_Date(obj['end_date'])

    while start <= end:

        obj = Collect_Data(obj)
	if obj['err'] != 0:
            Shut_Down( obj['err'], obj['msg'], True, True )

        #Increment start date as string object.
        obj = Increment_Date_Str(obj)
	if obj['err'] != 0:
            Shut_Down( obj['err'], obj['msg'], True, True )

        #increment date as date object
        start = start + datetime.timedelta(days=1)

    #end while

    """
    ###########################################################################
    #Fill Weekly Data:

    #reset start dates
    start = Parse_To_Date( initial_start )
    obj['start'] = initial_start

    #find first monday from start date...
    week = start + datetime.timedelta(days=7)

    while start < week:
        if start.weekday() == 0:
	    break
	else
	    start = start + datetime.timedelta(days=1)
    #end

    while start <= end:    

        #Increment start date as string object.
        obj = Increment_Date_Str(obj)
	if obj['err'] != 0:
            Shut_Down( obj['err'], obj['msg'], True, True )

        #increment date as date object
        start = start + datetime.timedelta(days=1)

    #end
    """

    Shut_Down( 0, 'Program Done, No Errors', False, False )

#end

#--------------------------------------
# MAIN ENTRY POINT INTO SCRIPT
if __name__ == "__main__":
    Main()

