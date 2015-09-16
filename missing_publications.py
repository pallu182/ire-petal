#!/usr/bin/python

import sys
sys.path.append("/Users/pallavik/Library/Enthought/Canopy_64bit/User/lib/python2.7/site-packages")
import requests

def getUserInput() :

	# get user input like ios branch name
	branch = raw_input("Enter the ios branch name : ")
	
	# get component names for which user wants to see the version delta
	compNames = raw_input("Enter the component names seperated by , for which you wish to see the version delta : ")
	print compNames.replace(" ", "")

	return branch,compNames

#def getExportDelta(ctsExportUrl) :
	# Get the XML Output from CTS Rest API's

	# Parse the xml

	# Get published version on the ios branch

	# Get latest version on component

	# Get version delta
#	print "In function get Export Delta function"


# main function 
(branch,compNames) = getUserInput()

# print branch
# print compNames

ctsExportUrl = "http://cts.cisco.com/cts/rest/exports?me.target_branch=%s&publish_contents.component=%s" %(branch, compNames)
urlOutput = requests.get(ctsExportUrl, auth=('pallavik', '!ma82Ge$'))

print urlOutput.text
