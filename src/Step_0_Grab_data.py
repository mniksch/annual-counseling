
# coding: utf-8

# # This page is just to grab the files we need
# 
# ## At the core, each "survey" file has the csv data along with a dictionary for deciphering it

# In[1]:


import pandas as pd
import numpy as np
from zipfile import ZipFile
import csv


# In[17]:


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


# In[33]:


os.mkdir('inputs')
os.chdir('inputs')


# In[16]:


# Here's where the files live:
baseUrl = 'https://nces.ed.gov/ipeds/datacenter/data/'

# Grad rate data; for each file, we typically try 2 more years than the prior year and if that file doesn't exist, try one more
fileroot = 'GR2016'

grab_zipfile(baseUrl, fileroot)
grab_zipfile(baseUrl, fileroot+'_DICT')


# In[18]:


# For grad rate only, we grab the 3 most recent years
grab_zipfile(baseUrl, 'GR2015')
grab_zipfile(baseUrl, 'GR2014')


# In[19]:


# The master directory:
grab_zipfile(baseUrl, 'HD2017')


# In[20]:


grab_zipfile(baseUrl, 'HD2017_DICT')


# In[22]:


# Admissions
grab_zipfile(baseUrl, 'ADM2016')
grab_zipfile(baseUrl, 'ADM2016_DICT')


# In[24]:


# Ethnicity
grab_zipfile(baseUrl, 'EF2016A')
grab_zipfile(baseUrl, 'EF2016A_DICT')


# In[26]:


# Retention
grab_zipfile(baseUrl, 'EF2016D')
grab_zipfile(baseUrl, 'EF2016D_DICT')


# In[27]:


# Institutional Characteristics
grab_zipfile(baseUrl, 'IC2016')
grab_zipfile(baseUrl, 'IC2016_DICT')


# In[29]:


# Student Financial Aid
grab_zipfile(baseUrl, 'SFA1516')
grab_zipfile(baseUrl, 'SFA1516_DICT')


# In[34]:


grab_zipfile(baseUrl, 'SFA1516_DICT')

