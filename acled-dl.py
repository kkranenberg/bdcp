import requests
import pandas as pd
import io
import json
import urllib
print("Import successful!")

print('Starting ACLED import.')
#acledDF = pd.read_csv(io.StringIO(requests.get('https://api.acleddata.com/acled/read.csv?terms=accept&limit=0').content.decode('utf-8')))
acledDF = pd.read_csv('https://api.acleddata.com/acled/read.csv?terms=accept&limit=0')
print('Imported ACLED successful!')

acledDF.to_csv('acled_api.csv', index=False)
print('Wrote ACLED to disk.')