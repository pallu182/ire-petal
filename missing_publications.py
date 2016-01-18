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
	compNames = compNames.replace(" ", "")

	return branch,compNames

def getExportDelta(branch, compNames) :
	# Get the XML Output from CTS Rest API's

	ctsExportUrl = "http://cts.cisco.com/cts/rest/exports?me.target_branch=%s&publish_contents.component=%s" %(branch, compNames)
	urlOutput = requests.get(ctsExportUrl, auth=('pallavik', '!ma82Ge$'))
	
	# put a try block
	try :
		FH = open("urlout.txt", "w+")
		FH.write(urlOutput.text)
		FH.close()
	except :
		print "Could not fetch from cts rest api, please check"
		exit(0)

	# open the xml output file and parse it
	try :
		FH = open("urlout.txt", "r")
		# Parse the xml
		xmlObj = xmltodict.parse(FH)
		FH.close()
	except :
		print "Could not parse the XML output produced by CTS, please check"
		exit(0)

	print "Component	Published-Version	Latest-Version	VersionDelta"
	try :
		for idx in xmlObj.get('ExportsReport').get('Component') :
			comp = idx['@name']
			pubVersion = idx['TargetBranch']['Version']['@name']
			latestVersion = idx['TargetBranch']['Version']['LatestVersion']
			versionDelta  = idx['TargetBranch']['Version']['VersionDelta']
			print comp , "\t", pubVersion,"\t", latestVersion,"\t", versionDelta
	except :
		print "Oopsie daisies :D"
		print "Missing publication script has a bug, it cannot work for single component !"
		print "Please give more components to work with :)"
	# Get published version on the ios branch

	# Get latest version on component

	# Get version delta
#	print "In function get Export Delta function"


# main function 
(branch,compNames) = getUserInput()

getExportDelta(branch, compNames)


