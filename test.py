import json
import requests
import pandas as pd

#url = 'https://researchworkspace.com/files/45140417/MBNMS_MARINe_Photoplots_Pelvetiopsis%20californica.json'
url = 'https://www.researchworkspace.com/files/44959120/marine_photoplot_sites_mbnms.json'
response = requests.get(url)
data = response.json()
print(data)