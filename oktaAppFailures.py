#!/usr/bin/python3

import requests as r
import json, csv
import logging as l
import settings as s
payload = ''

def buildHeader():
	return{
		'Accept': "application/json",
    	'Content-Type': "application/json",
    	'Authorization': 'SSWS ' + s.APITOKEN,
    	'Host': s.HOST
		}

def getAssignments(appId):
	url = f"https://{s.HOST}/api/v1/apps/{appId}/users"
	l.debug(url)
	headers = buildHeader()
	result = r.request("GET", url, headers=headers)
	if result.status_code != 200:
		l.error(f"Unable to retrieve users")
		return False
	response = json.loads(result.text)
	with open('oktaAppAssignmentFailures.csv','w',newline='') as file:
		writer = csv.writer(file)
		writer.writerow(['UserName','FirstName','LastName','UserId','AppID','SyncState'])
		for user in response:
			if 'ERROR' in user['syncState']:
				writer.writerow([user['credentials']['userName'],user['profile']['firstName'],user['profile']['lastName'],user['id'],s.APPID,user['syncState']])

def main():
	l.info('-- Start')
	getAssignments(s.APPID)

if __name__ == '__main__':
	main()