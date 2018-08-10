
## We're picking up from where we left off in Step 2

## Now we have Barrons ratings for everything from the Barrons site, correctly matched to the directory.
## We still have to do the following:

4. Use the admissions results data file to: _(done in this workbook)_

 a. Infer Barrons ratings for unrated colleges  
 b. Create a "Most Competitive+" rating for Most Competitive schools that admit 25% or less of applicants
 
## As part of this process, we'll exclude Trade institutions from the list (e.g. schools must at least grant associate's degrees)

## We're also going to use this file to cleanup a few initial fields to create the base for the final directory


```python
import pandas as pd
import numpy as np
import os

# Edit these to reflect any changes
os.chdir('../inputs')
directory_file = 'hd2017.csv'
admissions_file = 'adm2016.csv'
gender_file = 'ef2016a.csv'
inst_char_file = 'ic2017.csv'
clean_barrons_file = '../raw_inputs/true_barrons.csv'
sat_to_act_file = '../raw_inputs/sat_to_act.csv'
distance_file = 'distance_calcs.csv'
base_file = 'base_dir.csv'
```


```python
# At the end of this workbook, we'll want to have a "base directory" for adding to the other steps
#final_columns = ['UNITID','INSTNM',*'CollegeName'*,'ADDR','CITY','STABBR',
#                 'ZIP',*'HBCU'*,*'Type'*,'IALIAS','F1SYSNAM','LONGITUD','LATITUDE',
#                 'DistFromChicago'	'BarronsRating'	'SimpleBarrons']

# In order to get to these, we'll start with these direct pulls from the directory:
pull_columns = ['UNITID','INSTNM','ADDR','CITY','STABBR',
                 'ZIP','HBCU','IALIAS','F1SYSNAM','LONGITUD','LATITUDE','SECTOR']
```


```python
# First, we'll start off with a Base directory of all of the colleges in HD that have SECTOR 1-6,
# which are 2yr and 4yr granting schools

dir_df = pd.read_csv(directory_file, index_col=['UNITID'],
                     usecols=pull_columns,
                     dtype={'ZIP':str},
                     na_values='.',
                     encoding='latin-1')
dir_df = dir_df[dir_df.SECTOR.isin([1,2,3,4,5,6])]
dir_df.head()
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
      <th>INSTNM</th>
      <th>IALIAS</th>
      <th>ADDR</th>
      <th>CITY</th>
      <th>STABBR</th>
      <th>ZIP</th>
      <th>SECTOR</th>
      <th>HBCU</th>
      <th>F1SYSNAM</th>
      <th>LONGITUD</th>
      <th>LATITUDE</th>
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
      <th></th>
      <th></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>100654</th>
      <td>Alabama A &amp; M University</td>
      <td>AAMU</td>
      <td>4900 Meridian Street</td>
      <td>Normal</td>
      <td>AL</td>
      <td>35762</td>
      <td>1</td>
      <td>1</td>
      <td></td>
      <td>-86.568502</td>
      <td>34.783368</td>
    </tr>
    <tr>
      <th>100663</th>
      <td>University of Alabama at Birmingham</td>
      <td></td>
      <td>Administration Bldg Suite 1070</td>
      <td>Birmingham</td>
      <td>AL</td>
      <td>35294-0110</td>
      <td>1</td>
      <td>2</td>
      <td>The University of Alabama System</td>
      <td>-86.799345</td>
      <td>33.505697</td>
    </tr>
    <tr>
      <th>100690</th>
      <td>Amridge University</td>
      <td>Southern Christian University |Regions University</td>
      <td>1200 Taylor Rd</td>
      <td>Montgomery</td>
      <td>AL</td>
      <td>36117-3553</td>
      <td>2</td>
      <td>2</td>
      <td></td>
      <td>-86.174010</td>
      <td>32.362609</td>
    </tr>
    <tr>
      <th>100706</th>
      <td>University of Alabama in Huntsville</td>
      <td>UAH |University of Alabama Huntsville</td>
      <td>301 Sparkman Dr</td>
      <td>Huntsville</td>
      <td>AL</td>
      <td>35899</td>
      <td>1</td>
      <td>2</td>
      <td>The University of Alabama System</td>
      <td>-86.640449</td>
      <td>34.724557</td>
    </tr>
    <tr>
      <th>100724</th>
      <td>Alabama State University</td>
      <td></td>
      <td>915 S Jackson Street</td>
      <td>Montgomery</td>
      <td>AL</td>
      <td>36104-0271</td>
      <td>1</td>
      <td>1</td>
      <td></td>
      <td>-86.295677</td>
      <td>32.364317</td>
    </tr>
  </tbody>
</table>
</div>




```python
# We'll create a simple text field indicates two year vs four year college
# We'll also convert the HBCU field to a Yes/No field
dir_df['Type'] = dir_df.SECTOR.apply(lambda x: '4 year' if x<4 else '2 year')
dir_df.drop(columns=['SECTOR'],inplace=True)
dir_df.HBCU = dir_df.HBCU.apply(lambda x: 'Yes' if x==1 else 'No')
```


```python
# Next, we're going to create a "college name" field with parenthetical
# descriptions of each college based on single sex, HBCU, and 2-year status
gender_df = pd.read_csv(gender_file, index_col=['UNITID'],
                     usecols=['UNITID','EFALEVEL','EFTOTLT','EFTOTLM','EFTOTLW'],
                     na_values='.',
                     encoding='latin-1')
gender_df=gender_df[gender_df.EFALEVEL==1]
gender_df['pct_female']=gender_df.EFTOTLW/gender_df.EFTOTLT
gender_df.head()
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
      <th>EFALEVEL</th>
      <th>EFTOTLT</th>
      <th>EFTOTLM</th>
      <th>EFTOTLW</th>
      <th>pct_female</th>
    </tr>
    <tr>
      <th>UNITID</th>
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
      <td>1</td>
      <td>5859</td>
      <td>2413</td>
      <td>3446</td>
      <td>0.588155</td>
    </tr>
    <tr>
      <th>100663</th>
      <td>1</td>
      <td>19535</td>
      <td>7590</td>
      <td>11945</td>
      <td>0.611467</td>
    </tr>
    <tr>
      <th>100690</th>
      <td>1</td>
      <td>597</td>
      <td>233</td>
      <td>364</td>
      <td>0.609715</td>
    </tr>
    <tr>
      <th>100706</th>
      <td>1</td>
      <td>8468</td>
      <td>4833</td>
      <td>3635</td>
      <td>0.429263</td>
    </tr>
    <tr>
      <th>100724</th>
      <td>1</td>
      <td>5318</td>
      <td>1952</td>
      <td>3366</td>
      <td>0.632945</td>
    </tr>
  </tbody>
</table>
</div>




```python
def create_college_name(df, gender_df):
    """This function uses gender stats, HBCU status, and type to add descriptor to name"""
    id = df.ID
    root = df.INSTNM
    root_add = ''
    if id in gender_df.index:
        pct_f = gender_df.loc[id,'pct_female']
        if pct_f >=0.95:
            root_add = 'Female only'
        elif pct_f <=0.05:
            root_add = 'Male only'
    if df.HBCU == 'Yes':
        if root_add:
            root_add = 'HBCU, '+root_add
        else:
            root_add = 'HBCU'
    if df.Type == '2 year':
        if root_add:
            root_add = root_add + ', 2 year'
        else:
            root_add = '2 year'
    if root_add:
        return root+' ('+root_add+')'
    else:
        return root
    
dir_df['ID']=dir_df.index
dir_df['CollegeName']=dir_df.apply(create_college_name,args=(gender_df,),axis=1)
dir_df.drop(columns=['ID'],inplace=True)
```

## Now that we've created a few of the non-Barron's columns, we'll move forward with the Barrons work


```python
# Now, we'll pull in Barrons and try to infer the Barron's status of missing colleges
# First, we'll pull the clean barron's ratings from the prior step
# NOTE: If there are multiple rows with the same UNITID, this step will fail
barrons_df = pd.read_csv(clean_barrons_file,dtype={'UNITID':str},encoding='cp1252')
barrons_df = barrons_df[pd.notnull(barrons_df.UNITID)]
barrons_df.UNITID = barrons_df.UNITID.astype(int)
barrons_df.set_index(keys=['UNITID'],drop=True,inplace=True)
barrons_df.head()
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
      <th>College Name</th>
      <th>Selectivity</th>
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
      <td>Alabama A&amp;M University</td>
      <td>COMPETITIVE</td>
    </tr>
    <tr>
      <th>100663</th>
      <td>University of Alabama at Birmingham</td>
      <td>COMPETITIVE</td>
    </tr>
    <tr>
      <th>100706</th>
      <td>University of Alabama in Huntsville</td>
      <td>VERY COMPETITIVE</td>
    </tr>
    <tr>
      <th>100724</th>
      <td>Alabama State University</td>
      <td>NONCOMPETITIVE</td>
    </tr>
    <tr>
      <th>100751</th>
      <td>University of Alabama</td>
      <td>COMPETITIVE+</td>
    </tr>
  </tbody>
</table>
</div>




```python
# Next, we'll add those to the directory with 'TBD' as the default
dir_df['BarronsRating'] = dir_df.index.map(lambda x: barrons_df.Selectivity.get(x, 'TBD'))
```


```python
# In order to infer selectivity from admissions, we need to add admissions info
adm_fields = ['APPLCN','ADMSSN',
              'SATPCT','ACTPCT',
              'SATVR25','SATVR75','SATMT25','SATMT75',
              'ACTCM25','ACTCM75']

adm_df = pd.read_csv(admissions_file, index_col=['UNITID'],
                     usecols=['UNITID']+adm_fields,
                     na_values='.',
                     encoding='latin-1')
sat_to_act = pd.read_csv(sat_to_act_file, index_col=['SAT'],dtype={'SAT':int,'ACT':int},encoding='cp1252')
adm_df['pct_accepted'] = adm_df.ADMSSN/adm_df.APPLCN

def calculate_adjact50(df):
    """
    Estimates the median 'ACT' based on 25th to 75th percentile range of either ACT
    or converted SAT
    """
    result = np.nan
    if df.ACTPCT >= 20 and np.isfinite(df.ACTCM25) and np.isfinite(df.ACTCM75): #reasonable number of ACT
        result = (df.ACTCM25 + df.ACTCM75)/2
    elif df.SATPCT >= 20 and (np.isfinite(df.SATVR25) and np.isfinite(df.SATMT25) and
                              np.isfinite(df.SATVR75) and np.isfinite(df.SATMT75)): #same threshold for SAT
        sat25 = int(np.round(df.SATVR25+df.SATMT25,decimals=-1))
        sat75 = int(np.round(df.SATVR75+df.SATMT75,decimals=-1))
        result = (sat_to_act.ACT[sat25]+sat_to_act.ACT[sat75])/2
    return result

adm_df['AdjACT50'] = adm_df.apply(calculate_adjact50,axis=1)
dir_df = pd.concat([dir_df, adm_df[adm_df.index.isin(dir_df.index)]], axis=1)
```


```python
# We also need a single field from this table that indicates if the school is open enrollment
inst_char_df = pd.read_csv(inst_char_file, index_col=['UNITID'],
                     usecols=['UNITID','OPENADMP'],
                     na_values='.',
                     encoding='latin-1')
dir_df['OpenAdmissions'] = dir_df.index.map(lambda x: inst_char_df.OPENADMP.get(x, -2))
```

## The code above gives us the data we need to start inferring Barrons
## The code below does that work


```python
# First, we'll modify the actual Barron's for the most selective schools to create a new category
def make_most_comp_plus(df):
    if (df.BarronsRating == 'MOST COMPETITIVE') and (df.pct_accepted <= 0.25):
        return 'MOST COMPETITIVE+'
    else:
        return df.BarronsRating
dir_df.BarronsRating = dir_df.apply(make_most_comp_plus, axis=1)
```


```python
#Now, we'll start the "SimpleBarrons" columns by collapsing the pluses
# You can see in "VERY  COMPETITIVE" that the original Barrons contains
# Some typos. In future years, this code might throw an error if there
# is a Barrons rating not in this map
barrons_map = { 'MOST COMPETITIVE+':'Most Competitive+',
                'MOST COMPETITIVE':'Most Competitive',
                'HIGHLY COMPETITIVE+':'Highly Competitive',
                'HIGHLY COMPETITIVE':'Highly Competitive',
                'VERY  COMPETITIVE':'Very Competitive',
                'VERY COMPETITIVE':'Very Competitive',
                'VERY COMPETITIVE+':'Very Competitive',
                'COMPETITIVE':'Competitive',
                'COMPETITIVE+':'Competitive',
                'LESS COMPETITIVE':'Less Competitive',
                'LESS COMPETITIVE+':'Less Competitive',
                'NON COMPETITIVE':'Noncompetitive',
                'NONCOMPETITIVE':'Noncompetitive',
                'Not Available':'Not Available',
                'SPECIAL':'Not Available',
                'TBD':'TBD'
              }
dir_df['SimpleBarrons'] = dir_df.BarronsRating.map(barrons_map)
```


```python
#Now we're going to get some statistics in order to create cutoffs for the imputed ratings
act_cutoffs = dir_df[['SimpleBarrons','AdjACT50']].groupby(['SimpleBarrons']).describe()['AdjACT50']
adm_cutoffs = dir_df[['SimpleBarrons','pct_accepted']].groupby(['SimpleBarrons']).describe()['pct_accepted']
print(act_cutoffs.columns)
act_cutoffs['25%']
```

    Index(['count', 'mean', 'std', 'min', '25%', '50%', '75%', 'max'], dtype='object')
    




    SimpleBarrons
    Competitive           21.000
    Highly Competitive    27.500
    Less Competitive      17.750
    Most Competitive      29.875
    Most Competitive+     32.000
    Noncompetitive        19.375
    Not Available         21.750
    TBD                   18.500
    Very Competitive      24.000
    Name: 25%, dtype: float64




```python
adm_cutoffs['75%']
```




    SimpleBarrons
    Competitive           0.807033
    Highly Competitive    0.647430
    Less Competitive      0.827461
    Most Competitive      0.452249
    Most Competitive+     0.177290
    Noncompetitive        0.957850
    Not Available         0.769374
    TBD                   0.900704
    Very Competitive      0.771684
    Name: 75%, dtype: float64




```python
def infer_barrons(df, adm, act):
    """
    Apply function to take college data and ACT/Admissions percentile
    cutoffs to infer Barrons categories
    """
    response = df.SimpleBarrons
    if response != 'TBD':
        return response
    
    if df.OpenAdmissions == 1:
        if df.Type == '4 year':
            return 'Noncompetitive'
        else:
            return '2 year (Noncompetitive)'
    
    if df.Type == '2 year':
        if df.pct_accepted < 0.9:
            return '2 year (Competitive)'
        else:
            return '2 year (Noncompetitive)'
    if np.isfinite(df.AdjACT50) and np.isfinite(df.pct_accepted):
        # Generally, the bar should be met for both metrics to be included
        for check in ['Most Competitive+', 'Most Competitive',
                      'Highly Competitive', 'Very Competitive',
                      'Competitive', 'Less Competitive']:
            if (df.AdjACT50 >= act[check]) and (df.pct_accepted <= adm[check]):
                return check
        if df.pct_accepted <= 0.5:
            return 'Less Competitive'
        else:
            return 'Noncompetitive'
    else:
        return 'Not available'
    
    return response

dir_df['SimpleBarrons'] = dir_df.apply(infer_barrons, args=(adm_cutoffs['75%'],act_cutoffs['25%']),axis=1)
```


```python
# Now that we've got everything done, we'll save off the base_directory

#Quick change to Open Admissions to make intelligible
dir_df['OpenAdmissions'] = dir_df.OpenAdmissions.map({1:'Yes',2:'No',-2:'N/A'})

# Bring back in the distance calculation from before
distance_df = pd.read_csv(distance_file, index_col=['UNITID'],encoding='cp1252')
dir_df['DistFromChicago'] = dir_df.index.map(lambda x: distance_df.dist.get(x, np.nan))

# Finally, cull/reorder and save
final_names = ['INSTNM','CollegeName','ADDR','CITY','STABBR',
               'ZIP','HBCU','Type','IALIAS','F1SYSNAM','LONGITUD','LATITUDE',
               'DistFromChicago','BarronsRating','SimpleBarrons','OpenAdmissions']
dir_df[final_names].to_csv(base_file, na_rep='N/A')
```
