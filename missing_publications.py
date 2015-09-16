#!/usr/bin/python

import sys
sys.path.append("/Users/pallavik/Library/Enthought/Canopy_64bit/User/lib/python2.7/site-packages")
import requests
import xmltodict

def getUserInput() :

	# get user input like ios branch name
	branch = raw_input("Enter the ios branch name : ")
	
	# get component names for which user wants to see the version delta
	compNames = raw_input("Enter the component names seperated by , for which you wish to see the version delta : ")
	print compNames.replace(" ", "")

	return branch,compNames

def getExportDelta(branch, compNames) :
	# Get the XML Output from CTS Rest API's

	ctsExportUrl = "http://cts.cisco.com/cts/rest/exports?me.target_branch=%s&publish_contents.component=%s" %(branch, compNames)
	urlOutput = requests.get(ctsExportUrl, auth=('pallavik', '!ma82Ge$'))
	
	# put a try block
	FH = open("urlout.txt", "w+")
	FH.write(urlOutput.text)
	FH.close()
	
	# open the xml output file and parse it
	FH = open("urlout.txt", "r")
	# Parse the xml
	xmlObj = xmltodict.parse(FH)
	FH.close()

	# Get published version on the ios branch

	# Get latest version on component

	# Get version delta
#	print "In function get Export Delta function"


# main function 
(branch,compNames) = getUserInput()

# print branch
# print compNames
getExportDelta(branch, compNames)


