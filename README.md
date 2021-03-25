# Archaeology-Application-Work-Experience-Uploader
Python script to upload work experience for the Ontario Archaeology License Application

__Usage:__
```
uploader.py <user_name> <password> <application_id> <csv_file>

Example:
python uploader.py myusername mypassword 1234 WorkExperience.csv
```

__How To:__
Use the included csv file. Make sure there are no spaces after pif / borden #'s. Also make sure all stages, cultural periods and terrain types correctly match ministry requirements.

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
