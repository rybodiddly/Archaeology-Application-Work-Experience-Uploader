# Archaeology-Application-Work-Experience-Uploader
Python script to upload work experience for the Ontario Archaeology License Application

__Requirements:__
```
bs4 (BeautifulSoup)
pandas
requests
urllib3
```

__Usage:__
```
uploader.py <user_name> <password> <application_id> <csv_file>

Example:
python uploader.py myusername mypassword 1234 WorkExperience.csv
```

__How To:__

Create a new R License application online. To Get application number /ID, log in to your account, click `Applications` from the left hand menu so it drops down, then from the drop down select `Search for an Application`. Then select `New License` from the `Licence Application Type` drop down. The following page will show you your application id number. You can enter just the 4 digits or include the `APPL-` prefix.

Use the included csv file. Make sure there are no spaces after pif / borden #'s. Also make sure all stages, cultural periods and terrain types correctly match ministry requirements. Once the work experience csv is complete, use the commands detailed above to upload your work experience.

__Stage Options:__
```
1
2
1&2
3
4

NOTE: Stage 4 will default to 4 EX on application. If you wish to switch to A&P, you will must currently manually edit online.
```

__Cultural Period Options:__
```
Archaic
Euro-Canadian
Multi-component
Paleo-Indian
Post-Contact Indigenous
Woodland
Pre-Contact
Post-Contact
Industrial
Fur Trade
No Sites
Other
```
__Terrain Options:__
```
Agricultural
Arctic
Canadian Shield
Cemetery/Burial
Industrial
Marine
Open field
Park
Urban
Wooded
No Sites
Other
```
__Notes:__
- currently this script is intented for new R license applications. It has not been tested with any other license or license renewal type.
