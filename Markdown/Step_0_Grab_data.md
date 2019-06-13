
# Step 0: Grab data files from NCES
# This page is just to grab the files we need

## At the core, each "survey" file has the csv data along with a dictionary for deciphering it
### These will be do


```python
import pandas as pd
import numpy as np
from zipfile import ZipFile
import csv
```


```python
# This function is just a utility for grabbing the files
import urllib
import io
import os

def grab_zipfile(baseUrl, fileroot):
    '''uses a known static baseUrl to grab a zipped archive'''
    full_url = baseUrl + fileroot + '.zip'
    print(full_url, flush=True)
    remoteFile = urllib.request.urlopen(full_url)

    bio = io.BytesIO()
    bio.write(remoteFile.read())

    z = ZipFile(bio, 'r')
    print(z.namelist(), flush=True)
    z.extract(z.namelist()[0])
    return z.namelist()[0]
```


```python
os.mkdir('inputs')
os.chdir('inputs')
```


```python
# Here's where the files live:
baseUrl = 'https://nces.ed.gov/ipeds/datacenter/data/'

# Grad rate data; for each file, we typically try 2 more years than the prior year and if that file doesn't exist, try one more
fileroot = 'GR2017'

grab_zipfile(baseUrl, fileroot)
grab_zipfile(baseUrl, fileroot+'_DICT')

```

    https://nces.ed.gov/ipeds/datacenter/data/GR2017.zip
    ['gr2017.csv']
    https://nces.ed.gov/ipeds/datacenter/data/GR2017_DICT.zip
    ['gr2017.xlsx']
    




    'gr2017.xlsx'




```python
# For grad rate only, we grab the 3 most recent years
grab_zipfile(baseUrl, 'GR2016')
grab_zipfile(baseUrl, 'GR2015')
```

    https://nces.ed.gov/ipeds/datacenter/data/GR2016.zip
    ['gr2016.csv', 'gr2016_rv.csv']
    https://nces.ed.gov/ipeds/datacenter/data/GR2015.zip
    ['gr2015.csv', 'gr2015_rv.csv']
    




    'gr2015.csv'




```python
# The master directory:
grab_zipfile(baseUrl, 'HD2017')
```

    https://nces.ed.gov/ipeds/datacenter/data/HD2017.zip
    ['hd2017.csv']
    




    'hd2017.csv'




```python
grab_zipfile(baseUrl, 'HD2017_DICT')
```

    https://nces.ed.gov/ipeds/datacenter/data/HD2017_DICT.zip
    ['hd2017.xlsx']
    




    'hd2017.xlsx'




```python
# Admissions
grab_zipfile(baseUrl, 'ADM2017')
grab_zipfile(baseUrl, 'ADM2017_DICT')
```

    https://nces.ed.gov/ipeds/datacenter/data/ADM2017.zip
    ['adm2017.csv']
    https://nces.ed.gov/ipeds/datacenter/data/ADM2017_DICT.zip
    ['adm2017.xlsx']
    




    'adm2017.xlsx'




```python
# Ethnicity
grab_zipfile(baseUrl, 'EF2017A')
grab_zipfile(baseUrl, 'EF2017A_DICT')
```

    https://nces.ed.gov/ipeds/datacenter/data/EF2017A.zip
    ['ef2017a.csv']
    https://nces.ed.gov/ipeds/datacenter/data/EF2017A_DICT.zip
    ['ef2017a.xlsx']
    




    'ef2017a.xlsx'




```python
# Retention
grab_zipfile(baseUrl, 'EF2017D')
grab_zipfile(baseUrl, 'EF2017D_DICT')
```

    https://nces.ed.gov/ipeds/datacenter/data/EF2017D.zip
    ['ef2017d.csv']
    https://nces.ed.gov/ipeds/datacenter/data/EF2017D_DICT.zip
    ['ef2017d.xlsx']
    




    'ef2017d.xlsx'




```python
# Institutional Characteristics
grab_zipfile(baseUrl, 'IC2017')
grab_zipfile(baseUrl, 'IC2017_DICT')
```

    https://nces.ed.gov/ipeds/datacenter/data/IC2017.zip
    ['ic2017.csv']
    https://nces.ed.gov/ipeds/datacenter/data/IC2017_DICT.zip
    ['ic2017.xlsx']
    




    'ic2017.xlsx'




```python
# Student Financial Aid
grab_zipfile(baseUrl, 'SFA1617')
grab_zipfile(baseUrl, 'SFA1617_DICT')
```

    https://nces.ed.gov/ipeds/datacenter/data/SFA1617.zip
    ['sfa1617.csv']
    https://nces.ed.gov/ipeds/datacenter/data/SFA1617_DICT.zip
    ['sfa1617.xlsx']
    




    'sfa1617.xlsx'


