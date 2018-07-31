
# coding: utf-8

# # Here, we'll calculate a (aerial) distance from the college to the city of Chicago
# (Other networks could use the same code and simply replace our lat/long with theirs by changing the home_lat and home_lon variables below)

# In[ ]:


import pandas as pd
import numpy as np
import os

# Edit these to reflect any changes
os.chdir('./inputs')
directory_file = 'hd2017.csv'
output_file = 'distance_calcs.csv'
home_lat = 41.88283 # Change this if using a city other than Chicago
home_lon = -87.6276 # Change this if using a city other than Chicago


# In[ ]:


df = pd.read_csv(directory_file, index_col=['UNITID'], usecols=['UNITID','LONGITUD','LATITUDE'],
                na_values='.')
print('Lat/Long info loaded', flush=True)
df.head()


# In[ ]:


# These calculations are based on geometry incorporating approximations of the earth's curvature
# Calculations are based on the Haversine formula: https://en.wikipedia.org/wiki/Haversine_formula

df['latrad'] = np.deg2rad(df.LATITUDE)
df['lonrad'] = np.deg2rad(df.LONGITUD)
home_latrad = np.deg2rad(home_lat)
home_lonrad = np.deg2rad(home_lon)
df['dlat'] = df['latrad']-home_latrad
df['dlon'] = df['lonrad']-home_lonrad
df['a'] = np.sin(df.dlat/2)**2+np.cos(home_latrad)*np.cos(df.latrad)*np.sin(df.dlon/2)**2
df['c'] = 2*np.arcsin(np.sqrt(df['a']))
df['dist'] = np.round(df['c']*3956)
df.head()


# In[ ]:


# Finally, we'll save the calculations for inclusion in the final directory

output_file = 'distance_calcs.csv'
df.to_csv(output_file, index=True, columns=['dist'], na_rep='N/A')

