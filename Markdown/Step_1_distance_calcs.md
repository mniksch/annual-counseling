
# Here, we'll calculate a (aerial) distance from the college to the city of Chicago
(Other networks could use the same code and simply replace our lat/long with theirs by changing the home_lat and home_lon variables below)


```python
import pandas as pd
import numpy as np
import os

# Edit these to reflect any changes
os.chdir('inputs')
directory_file = 'hd2017.csv'
output_file = 'distance_calcs.csv'
home_lat = 41.88283 # Change this if using a city other than Chicago
home_lon = -87.6276 # Change this if using a city other than Chicago
```


```python
df = pd.read_csv(directory_file, index_col=['UNITID'], usecols=['UNITID','LONGITUD','LATITUDE'],
                na_values='.')
print('Lat/Long info loaded', flush=True)
df.head()
```

    Lat/Long info loaded
    




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>LONGITUD</th>
      <th>LATITUDE</th>
    </tr>
    <tr>
      <th>UNITID</th>
      <th></th>
      <th></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>100654</th>
      <td>-86.568502</td>
      <td>34.783368</td>
    </tr>
    <tr>
      <th>100663</th>
      <td>-86.799345</td>
      <td>33.505697</td>
    </tr>
    <tr>
      <th>100690</th>
      <td>-86.174010</td>
      <td>32.362609</td>
    </tr>
    <tr>
      <th>100706</th>
      <td>-86.640449</td>
      <td>34.724557</td>
    </tr>
    <tr>
      <th>100724</th>
      <td>-86.295677</td>
      <td>32.364317</td>
    </tr>
  </tbody>
</table>
</div>




```python
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
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>LONGITUD</th>
      <th>LATITUDE</th>
      <th>latrad</th>
      <th>lonrad</th>
      <th>dlat</th>
      <th>dlon</th>
      <th>a</th>
      <th>c</th>
      <th>dist</th>
    </tr>
    <tr>
      <th>UNITID</th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>100654</th>
      <td>-86.568502</td>
      <td>34.783368</td>
      <td>0.607084</td>
      <td>-1.510905</td>
      <td>-0.123909</td>
      <td>0.018485</td>
      <td>0.003886</td>
      <td>0.124751</td>
      <td>494.0</td>
    </tr>
    <tr>
      <th>100663</th>
      <td>-86.799345</td>
      <td>33.505697</td>
      <td>0.584785</td>
      <td>-1.514934</td>
      <td>-0.146209</td>
      <td>0.014456</td>
      <td>0.005367</td>
      <td>0.146653</td>
      <td>580.0</td>
    </tr>
    <tr>
      <th>100690</th>
      <td>-86.174010</td>
      <td>32.362609</td>
      <td>0.564834</td>
      <td>-1.504020</td>
      <td>-0.166159</td>
      <td>0.025370</td>
      <td>0.006988</td>
      <td>0.167378</td>
      <td>662.0</td>
    </tr>
    <tr>
      <th>100706</th>
      <td>-86.640449</td>
      <td>34.724557</td>
      <td>0.606058</td>
      <td>-1.512161</td>
      <td>-0.124935</td>
      <td>0.017229</td>
      <td>0.003943</td>
      <td>0.125662</td>
      <td>497.0</td>
    </tr>
    <tr>
      <th>100724</th>
      <td>-86.295677</td>
      <td>32.364317</td>
      <td>0.564864</td>
      <td>-1.506144</td>
      <td>-0.166129</td>
      <td>0.023246</td>
      <td>0.006969</td>
      <td>0.167154</td>
      <td>661.0</td>
    </tr>
  </tbody>
</table>
</div>




```python
# Finally, we'll save the calculations for inclusion in the final directory

output_file = 'distance_calcs.csv'
df.to_csv(output_file, index=True, columns=['dist'], na_rep='N/A')
```
