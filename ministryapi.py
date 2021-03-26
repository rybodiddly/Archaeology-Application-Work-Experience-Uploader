from bs4 import BeautifulSoup
from datetime import datetime
import re
import time

# GET Cookie / Session ID
def get_sessionID(session):
	url = 'https://www.iaa.gov.on.ca/iaalogin/IAALogin.jsp?REDID=PASTPORT'
	try:
		session.get(url, verify=False)
		print('GET Session ID')
	except:
		print('Error: Unable to GET Session ID and Cookie for Login Sequence')

# POST Login
def login(session, username, password):
	url = 'https://www.iaa.gov.on.ca/iaalogin/servlet/IAALogin'
	headers = {
		'Host': 'www.iaa.gov.on.ca',
		'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:87.0) Gecko/20100101 Firefox/87.0',
		'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
		'Accept-Language': 'en-CA,en-US;q=0.7,en;q=0.3',
		'Accept-Encoding': 'gzip, deflate, br',
		'Content-Type': 'application/x-www-form-urlencoded',
		'Origin': 'https://www.iaa.gov.on.ca',
		'Connection': 'keep-alive',
		'Referer': 'https://www.iaa.gov.on.ca/iaalogin/IAALogin.jsp?REDID=PASTPORT',
		'Upgrade-Insecure-Requests': '1'
	}
	payload = {
		'source_login': 'iaalogin',
		'GAURI': '',
		'login_url': 'https://www.iaa.gov.on.ca/iaalogin/IAALogin.jsp',
		'PAId': 'PASTPORT',
		'language': 'en_US',
		'pageGenTime': str(int(time.time()*1000)),
		'ldap_user': username,
		'ldap_password': password
	}
	try:
		session.post(url, headers=headers, data=payload, verify=False)
		print('POST Login')
	except:
		print('Error: Unable to Access Account')

# GET Applications
def get_application(session):
	url = 'https://www.pastport.mtc.gov.on.ca/APSWeb/application/applicationSearch.xhtml'
	headers = {
		'Host': 'www.pastport.mtc.gov.on.ca',
		'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:87.0) Gecko/20100101 Firefox/87.0',
		'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
		'Accept-Language': 'en-CA,en-US;q=0.7,en;q=0.3',
		'Accept-Encoding': 'gzip, deflate, br',
		'Connection': 'keep-alive',
		'Referer': 'https://www.pastport.mtc.gov.on.ca/APSWeb/application/applicationDetails.xhtml?page=New',
		'Upgrade-Insecure-Requests': '1'
	}
	try:
		get_applications = session.get(url, headers=headers, verify=False)
		print('GET Applications')
		soup = BeautifulSoup(get_applications.text, 'html.parser')
		page_token = soup.find('input', {'name':'applicationSearchForm:pageToken'})['value']
		javax_faces_ViewState = soup.find('input', {'name':'javax.faces.ViewState'})['value']
		return page_token, javax_faces_ViewState
	except:
		print("Error: Unable to Access Application or Unable to Find Page Token / View State")

# POST Application Selection - First Round
def select_app_v1(session, appID, page_token, javax_faces_ViewState):
	url = 'https://www.pastport.mtc.gov.on.ca/APSWeb/application/applicationSearch.xhtml'
	headers = {
		'Host': 'www.pastport.mtc.gov.on.ca',
		'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:87.0) Gecko/20100101 Firefox/87.0',
		'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
		'Accept-Language': 'en-CA,en-US;q=0.7,en;q=0.3',
		'Accept-Encoding': 'gzip, deflate, br',
		'Content-Type': 'application/x-www-form-urlencoded',
		'Origin': 'https://www.pastport.mtc.gov.on.ca',
		'Connection': 'keep-alive',
		'Referer': 'https://www.pastport.mtc.gov.on.ca/APSWeb/application/applicationSearch.xhtml',
		'Upgrade-Insecure-Requests': '1'
	}
	payload = {
		'applicationSearchForm:pageToken': page_token,
		'applicationSearchForm:searchAdvFlag': 'false',
		'applicationSearchForm:searchResFlag': 'true',
		'applicationSearchForm:searchResult': '',
		'applicationSearchForm:extApplicationId': format_appID(appID),
		'autoScroll': '0,0',
		'applicationSearchForm:extLicAppType': '',
		'applicationSearchForm_SUBMIT': '1',
		'javax.faces.ViewState': javax_faces_ViewState,
		'applicationSearchForm:_idcl': 'applicationSearchForm:extsearch'
	}
	try:
		search = session.post(url, headers=headers, data=payload, verify=False)
		print('POST Application Search Function V1:', appID)
		soup = BeautifulSoup(search.text, 'html.parser')
		javax_faces_ViewState = soup.find('input', {'name':'javax.faces.ViewState'})['value']
		idcl = ''
		for item in soup.find_all('a'):
			try:
				if re.search(':select', item['onclick']):
					idcl = item['id']
			except:
				pass

		return javax_faces_ViewState, idcl

	except:
		print('Error: Unable to Access Application #:', appID)

# POST Application Selection - Second Round /w Redirect
def select_app_v2(session, appID, page_token, javax_faces_ViewState, idcl):
	url = 'https://www.pastport.mtc.gov.on.ca/APSWeb/application/applicationSearch.xhtml'
	headers = {
		'Host': 'www.pastport.mtc.gov.on.ca',
		'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:87.0) Gecko/20100101 Firefox/87.0',
		'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
		'Accept-Language': 'en-CA,en-US;q=0.7,en;q=0.3',
		'Accept-Encoding': 'gzip, deflate, br',
		'Content-Type': 'application/x-www-form-urlencoded',
		'Origin': 'https://www.pastport.mtc.gov.on.ca',
		'Connection': 'keep-alive',
		'Referer': 'https://www.pastport.mtc.gov.on.ca/APSWeb/application/applicationSearch.xhtml',
		'Upgrade-Insecure-Requests': '1'
	}
	payload = {
		'applicationSearchForm:pageToken': page_token,
		'applicationSearchForm:searchAdvFlag': 'false',
		'applicationSearchForm:searchResFlag': 'true',
		'applicationSearchForm:searchResult': '',
		'applicationSearchForm:extApplicationId': format_appID(appID),
		'autoScroll': '0,0',
		'applicationSearchForm:extLicAppType': '246',
		'applicationSearchForm:resultSize': '10',
		'applicationSearchForm:currentPageIndex': '1',
		'applicationSearchForm:targetPageIndex': '0',
		'applicationSearchForm:sortBy': 'APPLICATION_NUM',
		'applicationSearchForm_SUBMIT': '1',
		'javax.faces.ViewState': javax_faces_ViewState,
		'applicationSearchForm:_idcl': idcl
	}
	try:
		session.post(url, headers=headers, data=payload, verify=False)
		print('POST Application Search Function V2:', appID)
	except:
		print('Error: Unable to Access Application #:', appID)

# GET URL: https://www.pastport.mtc.gov.on.ca/APSWeb/application/applicationWorkExperience.xhtml
# GET Work Experience
def work_experience(session):
	url = 'https://www.pastport.mtc.gov.on.ca/APSWeb/application/applicationWorkExperience.xhtml'
	headers = {
		'Host': 'www.pastport.mtc.gov.on.ca',
		'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:87.0) Gecko/20100101 Firefox/87.0',
		'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
		'Accept-Language': 'en-CA,en-US;q=0.7,en;q=0.3',
		'Accept-Encoding': 'gzip, deflate, br',
		'Connection': 'keep-alive',
		'Referer': 'https://www.pastport.mtc.gov.on.ca/APSWeb/application/applicationSummary.xhtml',
		'Upgrade-Insecure-Requests': '1'
	}
	try:
		session.get(url, headers=headers, verify=False)
		print('GET Work Experience Section of Application')
	except:
		print('Error: Unable to Access Work Experience')

# GET URL: https://www.pastport.mtc.gov.on.ca/APSWeb/application/applicationWEWorkSituation.xhtml
# GET Work Experience Situation (General Experience, not supervisory)
def experience_situation(session):
	url= 'https://www.pastport.mtc.gov.on.ca/APSWeb/application/applicationWEWorkSituation.xhtml'
	headers = {
		'Host': 'www.pastport.mtc.gov.on.ca',
		'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:87.0) Gecko/20100101 Firefox/87.0',
		'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
		'Accept-Language': 'en-CA,en-US;q=0.7,en;q=0.3',
		'Accept-Encoding': 'gzip, deflate, br',
		'Connection': 'keep-alive',
		'Referer': 'https://www.pastport.mtc.gov.on.ca/APSWeb/application/applicationWorkExperience.xhtml',
		'Upgrade-Insecure-Requests': '1'
	}
	try:
		get_work_experience_situation = session.get(url, headers=headers, verify=False)
		print('GET Work Experience Situation')
		soup = BeautifulSoup(get_work_experience_situation.text, 'html.parser')
		javax_faces_ViewState = soup.find('input', {'name':'javax.faces.ViewState'})['value']
		return javax_faces_ViewState
	except:
		print('Error: Unable to Access Work Experience Situation')

# POST URL: https://www.pastport.mtc.gov.on.ca/APSWeb/application/applicationWEWorkSituation.xhtml
# POST Upload Work Experience
def upload_experience(session, dict, javax_faces_ViewState, counter):
	url ='https://www.pastport.mtc.gov.on.ca/APSWeb/application/applicationWEWorkSituation.xhtml'
	headers = {
		'Host': 'www.pastport.mtc.gov.on.ca',
		'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:87.0) Gecko/20100101 Firefox/87.0',
		'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
		'Accept-Language': 'en-CA,en-US;q=0.7,en;q=0.3',
		'Accept-Encoding': 'gzip, deflate, br',
		'Content-Type': 'application/x-www-form-urlencoded',
		'Origin': 'https://www.pastport.mtc.gov.on.ca',
		'Connection': 'keep-alive',
		'Referer': 'https://www.pastport.mtc.gov.on.ca/APSWeb/application/applicationWEWorkSituation.xhtml',
		'Upgrade-Insecure-Requests': '1'
	}
	payload = {
		'applicationWEWorkSituationForm:pifNum': dict['pif'],
		'applicationWEWorkSituationForm:projectName': dict['project'],
		'applicationWEWorkSituationForm:bordenNumber': borden(dict['borden']),
		'applicationWEWorkSituationForm:stage': stage(dict['stage']),
		'applicationWEWorkSituationForm:projectLocation': dict['location'],
		'applicationWEWorkSituationForm:territory': dict['province'],
		'applicationWEWorkSituationForm:specify': '',
		'applicationWEWorkSituationForm:projLiencedSupName': dict['licensee'],
		'applicationWEWorkSituationForm:projectStartDateInputDate': rearrange_date(dict['start_date']),
		'applicationWEWorkSituationForm:projectStartDateInputCurrentDate': current_sdate(dict['start_date']),
		'applicationWEWorkSituationForm:projectEndDateInputDate': rearrange_date(dict['end_date']),
		'applicationWEWorkSituationForm:projectEndDateInputCurrentDate': datetime.today().strftime("%m/%Y"),
		'applicationWEWorkSituationForm:culturalPeriodId': cultural_period(dict['cultural_period']),
		'applicationWEWorkSituationForm:geogTerrainId': terrain(dict['terrain']),
		'applicationWEWorkSituationForm:numOfPrtcptDays': dict['participation'],
		'autoScroll': '0,1296.5',
		'applicationWEWorkSituationForm_SUBMIT': '1',
		'javax.faces.ViewState': javax_faces_ViewState,
		'applicationWEWorkSituationForm:_idcl': 'applicationWEWorkSituationForm:saveAOWS'
	}
	try:
		#session.post(url, headers=headers, data=payload, verify=False)
		r = session.post(url, headers=headers, data=payload, verify=False)
		print('POST Upload Work Experience')
		# Write html of POST Results to dump folder for debugging
		with open('dumps/' + str(counter) + '_dump.html', 'w') as f:
			f.write(r.text)
			f.close
	except:
		print('Error: Unable to Upload Work Experience')

# GET URL: https://www.pastport.mtc.gov.on.ca/APSWeb/application/applicationWEFieldWork.xhtml
# GET Supervisory Experience
def supervisor(session):
	url= 'https://www.pastport.mtc.gov.on.ca/APSWeb/application/applicationWEFieldWork.xhtml'
	headers = {
		'Host': 'www.pastport.mtc.gov.on.ca',
		'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:87.0) Gecko/20100101 Firefox/87.0',
		'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
		'Accept-Language': 'en-CA,en-US;q=0.7,en;q=0.3',
		'Accept-Encoding': 'gzip, deflate, br',
		'Connection': 'keep-alive',
		'Referer': 'https://www.pastport.mtc.gov.on.ca/APSWeb/application/applicationWorkExperience.xhtml',
		'Upgrade-Insecure-Requests': '1'
	}
	try:
		get_artifact = session.get(url, headers=headers, verify=False)
		print('GET Supervisory Experience')
		soup = BeautifulSoup(get_artifact.text, 'html.parser')
		javax_faces_ViewState = soup.find('input', {'name':'javax.faces.ViewState'})['value']
		return javax_faces_ViewState
	except:
		print('Error: Unable to Access Supervisory Experience')

# POST URL: https://www.pastport.mtc.gov.on.ca/APSWeb/application/applicationWEFieldWork.xhtml
# POST Upload Supervisory Experience
def upload_supervisor(session, dict, javax_faces_ViewState, counter):
	url ='https://www.pastport.mtc.gov.on.ca/APSWeb/application/applicationWEFieldWork.xhtml'
	headers = {
		'Host': 'www.pastport.mtc.gov.on.ca',
		'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:87.0) Gecko/20100101 Firefox/87.0',
		'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
		'Accept-Language': 'en-CA,en-US;q=0.7,en;q=0.3',
		'Accept-Encoding': 'gzip, deflate, br',
		'Content-Type': 'application/x-www-form-urlencoded',
		'Origin': 'https://www.pastport.mtc.gov.on.ca',
		'Connection': 'keep-alive',
		'Referer': 'https://www.pastport.mtc.gov.on.ca/APSWeb/application/applicationWEFieldWork.xhtml',
		'Upgrade-Insecure-Requests': '1'
	}
	payload = {
		'applicationWEFieldWorkForm:pifNum': dict['pif'],
		'applicationWEFieldWorkForm:projectName': dict['project'],
		'applicationWEFieldWorkForm:bordenNumber': borden(dict['borden']),
		'applicationWEFieldWorkForm:projectStageTypeCode': stage(dict['stage']),
		'applicationWEFieldWorkForm:projectLocation': dict['location'],
		'applicationWEFieldWorkForm:provinceCode': dict['province'],
		'applicationWEFieldWorkForm:specify': dict['supervisor_participation'],
		'applicationWEFieldWorkForm:projLiencedSupName': dict['licensee'],
		'applicationWEFieldWorkForm:projectStartDateInputDate': rearrange_date(dict['start_date']),
		'applicationWEFieldWorkForm:projectStartDateInputCurrentDate': current_sdate(dict['start_date']),
		'applicationWEFieldWorkForm:projectEndDateInputDate': rearrange_date(dict['end_date']),
		'applicationWEFieldWorkForm:projectEndDateInputCurrentDate': datetime.today().strftime("%m/%Y"),
		'applicationWEFieldWorkForm:numOfSupDays': '',
		'applicationWEFieldWorkForm:fieldworkRoleId': supervisor_role(dict['supervisor_experience']),
		'applicationWEFieldWorkForm:numOfPrtcptDays': dict['participation'],
		'autoScroll': '0,1018',
		'applicationWEFieldWorkForm_SUBMIT': '1',
		'javax.faces.ViewState': javax_faces_ViewState,
		'applicationWEFieldWorkForm:_idcl': 'applicationWEFieldWorkForm:saveSOFW',
	}
	try:
		#session.post(url, headers=headers, data=payload, verify=False)
		r = session.post(url, headers=headers, data=payload, verify=False)
		print('POST Upload Supervisory Experience')
		# Write html of POST Results to dump folder for debugging
		with open('dumps/' + str(counter) + '_dump.html', 'w') as f:
			f.write(r.text)
			f.close
	except:
		print('Error: Unable to Upload Supervisory Experience')

# GET URL: https://www.pastport.mtc.gov.on.ca/APSWeb/application/applicationWEArtifact.xhtml
# GET Artifact Management Experience
def artifact(session):
	url= 'https://www.pastport.mtc.gov.on.ca/APSWeb/application/applicationWEArtifact.xhtml'
	headers = {
		'Host': 'www.pastport.mtc.gov.on.ca',
		'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:87.0) Gecko/20100101 Firefox/87.0',
		'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
		'Accept-Language': 'en-CA,en-US;q=0.7,en;q=0.3',
		'Accept-Encoding': 'gzip, deflate, br',
		'Connection': 'keep-alive',
		'Referer': 'https://www.pastport.mtc.gov.on.ca/APSWeb/application/applicationWorkExperience.xhtml',
		'Upgrade-Insecure-Requests': '1'
	}
	try:
		get_artifact = session.get(url, headers=headers, verify=False)
		print('GET Artifact Management Experience')
		soup = BeautifulSoup(get_artifact.text, 'html.parser')
		javax_faces_ViewState = soup.find('input', {'name':'javax.faces.ViewState'})['value']
		return javax_faces_ViewState
	except:
		print('Error: Unable to Access Artifact Management Experience')

# POST URL: https://www.pastport.mtc.gov.on.ca/APSWeb/application/applicationWEArtifact.xhtml
# POST Upload Artifact Managment Experience
def upload_artifact(session, dict, javax_faces_ViewState, counter):
	url ='https://www.pastport.mtc.gov.on.ca/APSWeb/application/applicationWEArtifact.xhtml'
	headers = {
		'Host': 'www.pastport.mtc.gov.on.ca',
		'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:87.0) Gecko/20100101 Firefox/87.0',
		'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
		'Accept-Language': 'en-CA,en-US;q=0.7,en;q=0.3',
		'Accept-Encoding': 'gzip, deflate, br',
		'Content-Type': 'application/x-www-form-urlencoded',
		'Origin': 'https://www.pastport.mtc.gov.on.ca',
		'Connection': 'keep-alive',
		'Referer': 'https://www.pastport.mtc.gov.on.ca/APSWeb/application/applicationWEArtifact.xhtml',
		'Upgrade-Insecure-Requests': '1'
	}
	payload = {
		'applicationWEArtifactForm:pifNum': dict['pif'],
		'applicationWEArtifactForm:projectName': dict['project'],
		'applicationWEArtifactForm:directorName': dict['licensee'],
		'applicationWEArtifactForm:description': dict['artifact_experience'],
		'applicationWEArtifactForm:projectStartDateInputDate': rearrange_date(dict['start_date']),
		'applicationWEArtifactForm:projectStartDateInputCurrentDate': current_sdate(dict['start_date']),
		'applicationWEArtifactForm:projectEndDateInputDate': rearrange_date(dict['end_date']),
		'applicationWEArtifactForm:projectEndDateInputCurrentDate': datetime.today().strftime("%m/%Y"),
		'autoScroll': '0,723.5',
		'applicationWEArtifactForm_SUBMIT': '1',
		'javax.faces.ViewState': javax_faces_ViewState,
		'applicationWEArtifactForm:_idcl': 'applicationWEArtifactForm:saveAOFW'
	}
	try:
		#session.post(url, headers=headers, data=payload, verify=False)
		r = session.post(url, headers=headers, data=payload, verify=False)
		print('POST Upload Artifact Management Experience')
		# Write html of POST Results to dump folder for debugging
		with open('dumps/' + str(counter) + '_dump.html', 'w') as f:
			f.write(r.text)
			f.close
	except:
		print('Error: Unable to Upload Artifact Management Experience')

# re-arrange dates from MM/DD/YYY to DD/MM/YYYY
# prefix 0 if day or month not 2 digits
def rearrange_date(data):
	parts = data.split('/')
	if len(parts[0]) < 2:
		parts[0] = '0' + parts[0]
	if len(parts[1]) < 2:
		parts[1] = '0' + parts[1]
	rearranged = parts[1] + '/' + parts[0] + '/' + parts[2]
	return rearranged

def current_sdate(data):
	parts = data.split('/')
	rearranged = parts[0] + '/' + parts[2]
	return rearranged

# borden select one
def borden(data):
	borden = ''
	if isinstance(data, float) == False:
		split = str(data).split(',')
		borden =  split[0]
	return borden

# stage selector
# Todo: use a dictionary with key/value pairs
def stage(data):
	stringed = str(data)
	if stringed == '1':
		return '1'
	elif stringed == '2':
		return '2'
	elif stringed == '1&2':
		return '3'
	elif stringed == '3':
		return '4'
	elif stringed == '4':
		return '6'

# cultural period selector
def cultural_period(data):
	#print(data)
	#print('Float:', isinstance(data, float))
	periods = {
		'Archaic': '4081',
		'Euro-Canadian': '4082',
		'Multi-component': '4083',
		'Paleo-Indian': '4084',
		'Post-Contact Indigenous': '4085',
		'Woodland': '4086',
		'Pre-Contact': '18091',
		'Post-Contact': '18092',
		'Industrial': '18093',
		'Fur Trade': '18094',
		'No Sites': '18095',
		'Other': '18096'
	}
	for key, value in periods.items():
		if isinstance(data, float) == False:
			if str(data).lower() == key.lower():
				return value
		else:
			return ''

# terrain selector
def terrain(data):
	terrains = {
		'Agricultural': '4088',
		'Arctic': '18086',
		'Canadian Shield': '4089',
		'Cemetery/Burial': '4090',
		'Industrial': '4091',
		'Marine': '18087',
		'Open field': '4092',
		'Park': '18088',
		'Urban': '4093',
		'Wooded': '4094',
		'No Sites': '18089',
		'Other': '18090'
	}

	for key, value in terrains.items():
		if isinstance(data, float) == False:
			if str(data).lower() == key.lower():
				return value
		else:
			return ''

def supervisor_role(data):
	roles = {
		'Supervisor': '277',
		'Co-Supervisor': '278',
		'Assistant Supervisor': '279',
		'Crew Chief': '280',
		'Team Lead': '281'
	}
	for key, value in roles.items():
		if isinstance(data, float) == False:
			if str(data).lower() == key.lower():
				return value
		else:
			return ''

def format_appID(appID):
	if appID[:5] != 'APPL-':
		newID = 'APPL-' + appID
		return newID
	else:
		return appID.upper()