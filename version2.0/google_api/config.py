# separator used by search.py, categories.py, ...
SEPARATOR = "\t"

LANG            = "en_US" # can be en_US, fr_FR, ko_KR ...
ANDROID_ID      = "365F78B107076EFC"
GOOGLE_LOGIN    = "rio.app.test@gmail.com"
GOOGLE_PASSWORD = "abc13579" 
AUTH_TOKEN      = None #"yyyyyyyyy"
# force the user to edit this file
if any([each == None for each in [ANDROID_ID, GOOGLE_LOGIN, GOOGLE_PASSWORD]]):
    raise Exception("config.py not filled")




PIP             = "72.84.236.204:8080"

NB_RES = 20;
MAX_RESULTS = 500;



