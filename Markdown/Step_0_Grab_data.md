
# This page is just to grab the files we need

## At the core, each "survey" file has the csv data along with a dictionary for deciphering it


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
    print(full_url)
    remoteFile = urllib.request.urlopen(full_url)

    bio = io.BytesIO()
    bio.write(remoteFile.read())

    z = ZipFile(bio, 'r')
    print(z.namelist())
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
fileroot = 'GR2016'

grab_zipfile(baseUrl, fileroot)
grab_zipfile(baseUrl, fileroot+'_DICT')

```

    https://nces.ed.gov/ipeds/datacenter/data/GR2016.zip
    ['gr2016.csv']
    https://nces.ed.gov/ipeds/datacenter/data/GR2016_DICT.zip
    ['gr2016.xlsx']
    




    'gr2016.xlsx'




```python
# For grad rate only, we grab the 3 most recent years
grab_zipfile(baseUrl, 'GR2015')
grab_zipfile(baseUrl, 'GR2014')
```

    https://nces.ed.gov/ipeds/datacenter/data/GR2015.zip
    ['gr2015.csv', 'gr2015_rv.csv']
    https://nces.ed.gov/ipeds/datacenter/data/GR2014.zip
    ['gr2014.csv', 'gr2014_rv.csv']
    




    'gr2014.csv'




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
grab_zipfile(baseUrl, 'ADM2016')
grab_zipfile(baseUrl, 'ADM2016_DICT')
```

    https://nces.ed.gov/ipeds/datacenter/data/ADM2016.zip
    ['adm2016.csv']
    https://nces.ed.gov/ipeds/datacenter/data/ADM2016_DICT.zip
    ['adm2016.xlsx']
    




    'adm2016.xlsx'




```python
# Ethnicity
grab_zipfile(baseUrl, 'EF2016A')
grab_zipfile(baseUrl, 'EF2016A_DICT')
```

    https://nces.ed.gov/ipeds/datacenter/data/EF2016A.zip
    ['ef2016a.csv']
    https://nces.ed.gov/ipeds/datacenter/data/EF2016A_DICT.zip
    ['ef2016a.xlsx']
    




    'ef2016a.xlsx'




```python
# Retention
grab_zipfile(baseUrl, 'EF2016D')
grab_zipfile(baseUrl, 'EF2016D_DICT')
```

    https://nces.ed.gov/ipeds/datacenter/data/EF2016D.zip
    ['ef2016d.csv']
    https://nces.ed.gov/ipeds/datacenter/data/EF2016D_DICT.zip
    ['ef2016d.xlsx']
    




    'ef2016d.xlsx'




```python
# Institutional Characteristics
grab_zipfile(baseUrl, 'IC2016')
grab_zipfile(baseUrl, 'IC2016_DICT')
```

    https://nces.ed.gov/ipeds/datacenter/data/IC2016.zip
    ['ic2016.csv']
    https://nces.ed.gov/ipeds/datacenter/data/IC2016_DICT.zip
    ['ic2016.xlsx']
    




    'ic2016.xlsx'




```python
# Student Financial Aid
grab_zipfile(baseUrl, 'SFA1516')
grab_zipfile(baseUrl, 'SFA1516_DICT')
```

    https://nces.ed.gov/ipeds/datacenter/data/SFA1516.zip
    ['sfa1516.csv']
    https://nces.ed.gov/ipeds/datacenter/data/SFA1516_DICT.zip
    ['sfa1516.xlsx']
    




    'sfa1516.xlsx'




```python
grab_zipfile(baseUrl, 'SFA1516_DICT')
```

    https://nces.ed.gov/ipeds/datacenter/data/SFA1516_DICT.zip
    ['sfa1516.xlsx']
    




    'sfa1516.xlsx'


