from bs4 import BeautifulSoup
import pandas as pd
import requests
from datetime import datetime
import re
import time
import sys
import urllib3
from ministryapi import *

# main program
def main(username, password, appID, file):
	get_sessionID(session)
	login(session, username, password)
	page_token, javax_faces_ViewState = get_application(session)
	javax_faces_ViewState2, idcl = select_app_v1(session, appID, page_token, javax_faces_ViewState)
	select_app_v2(session, appID, page_token, javax_faces_ViewState2, idcl)
	work_experience(session)
	
	# open csv
	df = pd.read_csv(file)

	dict = {
		'pif': '',
		'project': '',
		'borden': '',
		'stage': '',
		'location': '',
		'province': '',
		'licensee': '',
		'start_date': '',
		'end_date': '',
		'cultural_period': '',
		'terrain': '',
		'participation': ''
	}
	counter = 0
	# Begin Loop:
	# Get CSV Rows:
	for index, row in df.iterrows():
		dict['pif'] = row['Pif']
		dict['project'] = row['Project']
		dict['borden'] = row['Borden']
		dict['stage'] = row['Stage']
		dict['location'] = row['Location']
		dict['province'] = row['Province']
		dict['licensee'] = row['Licensee']
		dict['start_date'] = row['Start Date MM/DD/YYYY']
		dict['end_date'] = row['End Date MM/DD/YYYY']
		dict['cultural_period'] = row['Cultural Period']
		dict['terrain'] = row['Terrain']
		dict['participation'] = row['Days of Participation']
		
		# GET Work Experience Situation
		javax_faces_ViewState = experience_situation(session)
		#time.sleep(1)
		# Upload Exerience Data
		upload(session, dict, javax_faces_ViewState, counter)
		counter += 1
		#time.sleep(1)

username = sys.argv[1]
password = sys.argv[2]
appID = sys.argv[3]
file = sys.argv[4]

urllib3.disable_warnings()
session = requests.Session()

main(username, password, appID, file)
print('Upload Complete')