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
def main(session, username, password, appID, file, arg):
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
		'participation': '',
		'supervisor_experience': '',
		'supervisor_participation': '',
		'artifact_experience': ''
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
		dict['supervisor_experience'] = row['Supervisor Experience']
		dict['supervisor_participation'] = row['Days of Supervisor Participation']
		dict['artifact_experience'] = row['Artifact Experience']
		
		# Work Experience:
		if arg.lower() == '-we':
			# GET Work Experience Situation
			javax_faces_ViewState = experience_situation(session)
			# Upload Exerience Data
			upload_experience(session, dict, javax_faces_ViewState, counter)
		
		elif arg.lower() == '-s':
			# if not float (meaning it contains data and is not NaN) then continue, otherwise is blank so skip
			if isinstance(row['Supervisor Experience'], float) == False:
				# Get Supervisory Experience
				javax_faces_ViewState = supervisor(session)
				# Upload Supervisory Exerience Data
				upload_supervisor(session, dict, javax_faces_ViewState, counter)

		# Artifact Experience:
		elif arg.lower() == '-a':
			# if not float (meaning it contains data and is not NaN) then continue, otherwise is blank so skip
			if isinstance(row['Artifact Experience'], float) == False:
				# Get Artifact Management
				javax_faces_ViewState = artifact(session)
				# Upload Artifact Management Experience
				upload_artifact(session, dict, javax_faces_ViewState, counter)

		counter += 1

username = sys.argv[1]
password = sys.argv[2]
appID = sys.argv[3]
file = sys.argv[4]
arg = sys.argv[5]

urllib3.disable_warnings()
session = requests.Session()

main(session, username, password, appID, file, arg)
print('Upload Complete')