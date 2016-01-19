#!/usr/bin/python

import sys
sys.path.append("/Users/pallavik/Library/Enthought/Canopy_64bit/User/lib/python2.7/site-packages")
import requests
import xmltodict
import string

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
		# for some reason for single component xmltodict processing fails, hence we are doing seperate stuff
		l1 = compNames.split(",")

		if len(l1) > 1:
			for idx in xmlObj.get('ExportsReport').get('Component') :
				parseCompDetails(idx)	
				(comp, pubVersion, latestVersion, versionDelta, publishDate) = parseCompDetails(idx)
				print comp , "\t\t", pubVersion,"\t", latestVersion,"\t", versionDelta, "\t", publishDate
				
		else :
			id = xmlObj.get('ExportsReport').get('Component')
			(comp, pubVersion, latestVersion, versionDelta, publishDate) = parseCompDetails(id)
			print comp , "\t\t", pubVersion,"\t", latestVersion,"\t", versionDelta, "\t", publishDate
	except :
		print "Oopsie daisies !! Something went wrong in parsing the cts xml output. Please check !"

	# Get published version on the ios branch

	# Get latest version on component

	# Get version delta
#	print "In function get Export Delta function"


def parseCompDetails(id) :
	comp          = id['@name']
	pubVersion    = id['TargetBranch']['Version']['@name']
	latestVersion = id['TargetBranch']['Version']['LatestVersion']
	versionDelta  = id['TargetBranch']['Version']['VersionDelta']
	publishDate   = id['TargetBranch']['Version']['PublishDate']

	return (comp, pubVersion, latestVersion, versionDelta, publishDate)

# main function 
(branch,compNames) = getUserInput()

getExportDelta(branch, compNames)


