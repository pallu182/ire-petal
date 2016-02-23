#!/auto/sw/packages/python/2.7.9/bin/python

import sys
sys.path.append("/auto/sw/packages/python/2.7.9/lib/python2.7/site-packages")
import requests
sys.path.append("/ws/pallavik-sjc/pip-install-dir/xmltodict")
import xmltodict
import string
import re
sys.path.append("/ws/pallavik-sjc/pip-install-dir/tabulate")
import tabulate
import getpass

def getUserInput() :

	# get user input like ios branch name
	branch = raw_input("Enter the ios branch name : ")
	
	# get component names for which user wants to see the version delta
	compNames = raw_input("Enter the component names seperated by , for which you wish to see the version delta : ")
	compNames = compNames.replace(" ", "")

	return branch,compNames

def getExportDelta(branch, compNames, userid, paswd) :

	# Get the XML Output from CTS Rest API's
	ctsExportUrl = "http://cts.cisco.com/cts/rest/exports?me.target_branch=%s&publish_contents.component=%s" %(branch, compNames)
	urlOutput = requests.get(ctsExportUrl, auth=(userid, paswd))
	
	# try block to open cts xml output
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
	# for some reason for single component xmltodict processing fails, hence we are doing seperate stuff
	l1 = compNames.split(",")

	if len(l1) > 1:
		for idx in xmlObj.get('ExportsReport').get('Component') :
			(comp, pubVersion, latestVersion, versionDelta, publishDate) = parseCompDetails(idx)
			print comp , "\t\t", pubVersion,"\t", latestVersion,"\t", versionDelta, "\t", publishDate
			if int(versionDelta) > 0 :
				getVersionDelta(comp, pubVersion, publishDate, branch)
				
	else :
		id = xmlObj.get('ExportsReport').get('Component')
		(comp, pubVersion, latestVersion, versionDelta, publishDate) = parseCompDetails(id)
		print comp , "\t\t", pubVersion,"\t", latestVersion,"\t", versionDelta, "\t", publishDate
		if int(versionDelta) > 0 :
			getVersionDelta(comp, pubVersion, publishDate, branch)

	# Get version delta


def parseCompDetails(id) :
	comp          = id['@name']
	pubVersion    = id['TargetBranch']['Version']['@name']
	latestVersion = id['TargetBranch']['Version']['LatestVersion']
	versionDelta  = id['TargetBranch']['Version']['VersionDelta']
	publishDate   = id['TargetBranch']['Version']['PublishDate']

	return (comp, pubVersion, latestVersion, versionDelta, publishDate)
def getVersionDelta(comp, pubVersion, publishDate, branch) :

	compBranch = getCompBranchName(comp,pubVersion)
	
	pubDate = publishDate.split(" ")

	ctsUrl = "http://cts.cisco.com/cts/rest/version?component=%s&comp_branch=%s&date_start=%s" %(comp, compBranch, pubDate[0])
	urlOutput = requests.get(ctsUrl, auth=(userid, paswd))
	
	# try block to open cts xml output
	try :
		FH = open("compurlout.txt", "w+")
		FH.write(urlOutput.text)
		FH.close()
	except :
		print "Could not fetch from cts rest api, please check"
		exit(0)

    # open the xml output file and parse it
	try :
		FH = open("compurlout.txt", "r")
	# Parse the xml
		xmlObj = xmltodict.parse(FH)
		FH.close()
	except :
		print "Could not parse the XML output produced by CTS, please check"
		exit(0)

	# Print the XML details in tabular format 
	try :
		for idx in xmlObj.get('VersionReport').get('Component').get('Branch').get('Version') :
			(bugId, committedBy, commitDate, bugExportInfo, version) = parseExportDetails(idx)        
			print bugId, committedBy, commitDate, bugExportInfo, version
	except : 
		id = xmlObj.get('VersionReport').get('Component').get('Branch').get('Version')
		(bugId, committedBy, commitDate, bugExportInfo, version) = parseExportDetails(id)
		print bugId, committedBy, commitDate, bugExportInfo, version


def parseExportDetails(id) :
	version = id['@name']
	bugId  = id['Bugid']
	committedBy = id['Committed_by']
	bugExportInfo = id['Bugid_export_info']
	commitDate = id['Commit_Date']
	print bugId, committedBy, commitDate, bugExportInfo, version
	return(bugId, committedBy, commitDate, bugExportInfo, version)

def getCompBranchName(comp,pubVersion) :

	#print pubVersion
	p = re.compile("\((\w+)\)")
	ver = p.findall(pubVersion)

	#print comp, ver[0]
	compBranch = "comp_%s_%s" %(comp,ver[0])
	#print compBranch
	return compBranch
	
# main function 
(branch,compNames) = getUserInput()

userid 	  = raw_input("Please enter your cec user id : ")
paswd     = getpass.getpass()

getExportDelta(branch, compNames, userid, paswd)

