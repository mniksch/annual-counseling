
# In this step, we'll process graduation data from the federal files
## In most cases, this is a straight "pull" from the data, but there are a few possible modifications:

- If the sample is too small from the most recent year, use 3 years of data
- For HBCUs, boost by 15%
- For a handful of schools, adjust down to reflect the true Noble rate of success
- Add in a handful of estimates


```python
import pandas as pd
import numpy as np
import os

# Edit these to reflect any changes
work_location = '../inputs'
directory_file = 'hd2017.csv'
base_dir = 'base_dir.csv'
noble_attending = '../raw_inputs/noble_attending.csv'
gr_output = 'grad_rates.csv'
gr_files = {'latest':'gr2016.csv',
            'one_removed':'gr2015.csv',
            'two_removed':'gr2014.csv'}
```


```python
os.chdir(work_location)
```


```python
# We'll use a dict to keep track of each grad rate file, reading in each one
years=['latest','one_removed','two_removed']
gr_dfs = {}
for year in years:
    gr_dfs[year] = pd.read_csv(gr_files[year], index_col=['UNITID'],
                     usecols=['UNITID', 'GRTYPE', 'GRTOTLT','GRBKAAT','GRHISPT'],
                     na_values='.',
                     dtype={'GRTOTLT':float,'GRBKAAT':float,'GRHISPT':float},
                     encoding='latin-1')
    gr_dfs[year].rename(columns={'GRTOTLT':'Total','GRBKAAT':'Black','GRHISPT':'Hisp'}, inplace=True)
    gr_dfs[year]['AA_H']=gr_dfs[year].Black+gr_dfs[year].Hisp
gr_dfs['latest'].head()
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
      <th>GRTYPE</th>
      <th>Total</th>
      <th>Black</th>
      <th>Hisp</th>
      <th>AA_H</th>
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
      <td>2</td>
      <td>1073.0</td>
      <td>1034.0</td>
      <td>4.0</td>
      <td>1038.0</td>
    </tr>
    <tr>
      <th>100654</th>
      <td>3</td>
      <td>295.0</td>
      <td>289.0</td>
      <td>0.0</td>
      <td>289.0</td>
    </tr>
    <tr>
      <th>100654</th>
      <td>4</td>
      <td>404.0</td>
      <td>383.0</td>
      <td>3.0</td>
      <td>386.0</td>
    </tr>
    <tr>
      <th>100654</th>
      <td>6</td>
      <td>1073.0</td>
      <td>1034.0</td>
      <td>4.0</td>
      <td>1038.0</td>
    </tr>
    <tr>
      <th>100654</th>
      <td>8</td>
      <td>1073.0</td>
      <td>1034.0</td>
      <td>4.0</td>
      <td>1038.0</td>
    </tr>
  </tbody>
</table>
</div>




```python
# We now have to sort through these GRTYPES:
# 8 is the adjusted cohort for bachelor's seeking students (completions: 12=6yr, 13=4yr, 14=5yr; transfers=16)
# 29 for associate's seeking (completions: 30=3yr 35=2yr; transfers=33)
# We'll build a list of unitids that have both starting cohorts and completions for either one
valid_unitids = {}
for year in years:
    df = gr_dfs[year]
    valid_unitids[year] = list( (set(df[df['GRTYPE']==8].index) & set(df[df['GRTYPE']==12].index)) |
                                (set(df[df['GRTYPE']==29].index) & set(df[df['GRTYPE']==30].index)) )
print('%d, %d' % (len(gr_dfs['latest']), len(valid_unitids['latest'])))
```

    55742, 4008
    


```python
# We'll use the basic "hd" directory to form the base of the final year output
def create_year_df(df, source_df1, source_df2):
    """Apply function to pull the appropriate data into a single row per college"""
    ix = df.name
    if ix in source_df1.index:
        return source_df1.loc[ix][['Total','Black','Hisp','AA_H']]
    elif ix in source_df2.index:
        return source_df2.loc[ix][['Total','Black','Hisp','AA_H']]
    else:
        return [np.nan,np.nan,np.nan,np.nan]

year_dfs = {}
for year in years:
    dir_df = pd.read_csv(directory_file, index_col=['UNITID'],
                     usecols=['UNITID','INSTNM'],encoding='latin-1')
    dir_df = dir_df[dir_df.index.isin(valid_unitids[year])]
    
    # First do the starts
    start1 = gr_dfs[year][gr_dfs[year].GRTYPE == 12]
    start2 = gr_dfs[year][gr_dfs[year].GRTYPE == 30]
    dir_df[['Cl_Total','Cl_Black','Cl_Hisp','Cl_AA_H']]=dir_df.apply(create_year_df,axis=1,result_type="expand",
                                                                    args=(start1,start2))
    # Then do the completions
    start1 = gr_dfs[year][gr_dfs[year].GRTYPE == 8]
    start2 = gr_dfs[year][gr_dfs[year].GRTYPE == 29]
    dir_df[['St_Total','St_Black','St_Hisp','St_AA_H']]=dir_df.apply(create_year_df,axis=1,result_type="expand",
                                                                    args=(start1,start2))
    # Next the transfers
    start1 = gr_dfs[year][gr_dfs[year].GRTYPE == 16]
    start2 = gr_dfs[year][gr_dfs[year].GRTYPE == 33]
    dir_df[['Xf_Total','Xf_Black','Xf_Hisp','Xf_AA_H']]=dir_df.apply(create_year_df,axis=1,result_type="expand",
                                                                    args=(start1,start2))
    
    # Finally, calculated within year stats
    for type in ['Total','Black','Hisp','AA_H']:
        dir_df['GR_'+type]=dir_df['Cl_'+type]/dir_df['St_'+type]
        dir_df['Xfr_'+type]=dir_df['Xf_'+type]/dir_df['St_'+type]
        dir_df['CI_'+type]=np.sqrt(dir_df['GR_'+type]*(1-dir_df['GR_'+type])/dir_df['St_'+type])
        dir_df.replace(np.inf,np.nan)
    
    year_dfs[year]=dir_df.copy()
year_dfs['latest'].head()
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
      <th>Cl_Total</th>
      <th>Cl_Black</th>
      <th>Cl_Hisp</th>
      <th>Cl_AA_H</th>
      <th>St_Total</th>
      <th>St_Black</th>
      <th>St_Hisp</th>
      <th>St_AA_H</th>
      <th>Xf_Total</th>
      <th>...</th>
      <th>CI_Total</th>
      <th>GR_Black</th>
      <th>Xfr_Black</th>
      <th>CI_Black</th>
      <th>GR_Hisp</th>
      <th>Xfr_Hisp</th>
      <th>CI_Hisp</th>
      <th>GR_AA_H</th>
      <th>Xfr_AA_H</th>
      <th>CI_AA_H</th>
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
      <td>295.0</td>
      <td>289.0</td>
      <td>0.0</td>
      <td>289.0</td>
      <td>1073.0</td>
      <td>1034.0</td>
      <td>4.0</td>
      <td>1038.0</td>
      <td>404.0</td>
      <td>...</td>
      <td>0.013630</td>
      <td>0.279497</td>
      <td>0.370406</td>
      <td>0.013956</td>
      <td>0.000000</td>
      <td>0.750000</td>
      <td>0.000000</td>
      <td>0.278420</td>
      <td>0.371869</td>
      <td>0.013912</td>
    </tr>
    <tr>
      <th>100663</th>
      <td>University of Alabama at Birmingham</td>
      <td>813.0</td>
      <td>197.0</td>
      <td>12.0</td>
      <td>209.0</td>
      <td>1534.0</td>
      <td>402.0</td>
      <td>28.0</td>
      <td>430.0</td>
      <td>374.0</td>
      <td>...</td>
      <td>0.012743</td>
      <td>0.490050</td>
      <td>0.261194</td>
      <td>0.024933</td>
      <td>0.428571</td>
      <td>0.357143</td>
      <td>0.093522</td>
      <td>0.486047</td>
      <td>0.267442</td>
      <td>0.024103</td>
    </tr>
    <tr>
      <th>100690</th>
      <td>Amridge University</td>
      <td>2.0</td>
      <td>1.0</td>
      <td>0.0</td>
      <td>1.0</td>
      <td>7.0</td>
      <td>3.0</td>
      <td>0.0</td>
      <td>3.0</td>
      <td>5.0</td>
      <td>...</td>
      <td>0.170747</td>
      <td>0.333333</td>
      <td>0.666667</td>
      <td>0.272166</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>0.333333</td>
      <td>0.666667</td>
      <td>0.272166</td>
    </tr>
    <tr>
      <th>100706</th>
      <td>University of Alabama in Huntsville</td>
      <td>292.0</td>
      <td>32.0</td>
      <td>8.0</td>
      <td>40.0</td>
      <td>600.0</td>
      <td>92.0</td>
      <td>23.0</td>
      <td>115.0</td>
      <td>179.0</td>
      <td>...</td>
      <td>0.020405</td>
      <td>0.347826</td>
      <td>0.347826</td>
      <td>0.049656</td>
      <td>0.347826</td>
      <td>0.434783</td>
      <td>0.099311</td>
      <td>0.347826</td>
      <td>0.365217</td>
      <td>0.044413</td>
    </tr>
    <tr>
      <th>100724</th>
      <td>Alabama State University</td>
      <td>236.0</td>
      <td>214.0</td>
      <td>2.0</td>
      <td>216.0</td>
      <td>1090.0</td>
      <td>987.0</td>
      <td>6.0</td>
      <td>993.0</td>
      <td>NaN</td>
      <td>...</td>
      <td>0.012475</td>
      <td>0.216819</td>
      <td>NaN</td>
      <td>0.013117</td>
      <td>0.333333</td>
      <td>NaN</td>
      <td>0.192450</td>
      <td>0.217523</td>
      <td>NaN</td>
      <td>0.013092</td>
    </tr>
  </tbody>
</table>
<p>5 rows × 25 columns</p>
</div>




```python
year_dfs['latest'].to_csv('grad2016.csv', na_rep="N/A")
year_dfs['one_removed'].to_csv('grad2015.csv', na_rep="N/A")
year_dfs['two_removed'].to_csv('grad2014.csv', na_rep="N/A")
```

## The above code created three DFs for the most recent three years
## Each DF has the in year counting stats and rates for graduation
### Now we need create a final set of statistics based on these:
- Adj6yrGrad (overall number after adjustments)
- Adj6yrAAH (African American/Hispanic number after adjustments)
- 6yrGrad (overall number, no adjustments)
- 6yrAAH (AA/H no adjustments)
- 6yrAA
- 6yrH
- Xfer
- XferAAH
- XferAA
- XferH



```python
# We'll start with reading some of the rows from the 'base_dir' created in the last step
dir_df = pd.read_csv(base_dir, index_col=['UNITID'],
                     usecols=['UNITID','INSTNM','Type','HBCU'],encoding='latin-1')
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
      <th>HBCU</th>
      <th>Type</th>
    </tr>
    <tr>
      <th>UNITID</th>
      <th></th>
      <th></th>
      <th></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>100654</th>
      <td>Alabama A &amp; M University</td>
      <td>Yes</td>
      <td>4 year</td>
    </tr>
    <tr>
      <th>100663</th>
      <td>University of Alabama at Birmingham</td>
      <td>No</td>
      <td>4 year</td>
    </tr>
    <tr>
      <th>100690</th>
      <td>Amridge University</td>
      <td>No</td>
      <td>4 year</td>
    </tr>
    <tr>
      <th>100706</th>
      <td>University of Alabama in Huntsville</td>
      <td>No</td>
      <td>4 year</td>
    </tr>
    <tr>
      <th>100724</th>
      <td>Alabama State University</td>
      <td>Yes</td>
      <td>4 year</td>
    </tr>
  </tbody>
</table>
</div>




```python
def bump15(x):
    """Helper function to increase by 15% or half the distance to 100"""
    if x > .7:
        return x + (1-x)*.5
    else:
        return x + .15
    
def set_gradrates(df, year_dfs):
    """Apply function to decide how to set the specific values specified above"""
    ix = df.name
    
    # First we see if there is actual data for the latest year
    if ix in year_dfs['latest'].index:
        ty = year_dfs['latest'].loc[ix]
        gr_source = '2016'
        gr_6yr,gr_6yr_aah,gr_6yr_aa,gr_6yr_h,xf,xf_aah,xf_aa,xf_h = ty.reindex(
            ['GR_Total','GR_AA_H','GR_Black','GR_Hisp','Xfr_Total','Xfr_AA_H','Xfr_Black','Xfr_Hisp'])
        
        # If there's data in the latest year, we'll check how robust and add in prior years if necessary
        ci, ci_aah = ty.reindex(['CI_Total','CI_AA_H'])
        # For HBCUs, we bump by the lesser of 15% or half the distance to 100%
        if (df.HBCU == 'Yes') and (ci_aah <= 0.04):
            adj_6yr = gr_6yr
            adj_6yr_aah = bump15(gr_6yr_aah)
        # Otherwise, add more years if the confidence intervals are too low
        elif (ci >0.015) or (ci_aah >0.05):
            calc_fields = ['Cl_Total','Cl_Black','Cl_Hisp','Cl_AA_H',
                           'St_Total','St_Black','St_Hisp','St_AA_H',
                           'Xf_Total','Xf_Black','Xf_Hisp','Xf_AA_H']
            calc_data = ty.reindex(calc_fields)
            
            if ix in year_dfs['one_removed'].index:
                gr_source = '2015-2016'
                ty=year_dfs['one_removed'].loc[ix]
                calc_data = calc_data+ty.reindex(calc_fields)
                
                if ix in year_dfs['two_removed'].index:
                    gr_source = '2014-2016'
                    ty=year_dfs['two_removed'].loc[ix]
                    calc_data = calc_data+ty.reindex(calc_fields)
                    
                    
            gr_6yr = calc_data['Cl_Total']/calc_data['St_Total'] if calc_data['St_Total']>0 else np.nan
            gr_6yr_aah = calc_data['Cl_AA_H']/calc_data['St_AA_H'] if calc_data['St_AA_H']>0 else np.nan
            gr_6yr_aa = calc_data['Cl_Black']/calc_data['St_Black'] if calc_data['St_Black']>0 else np.nan
            gr_6yr_h = calc_data['Cl_Hisp']/calc_data['St_Hisp'] if calc_data['St_Hisp']>0 else np.nan
            xf = calc_data['Xf_Total']/calc_data['St_Total'] if calc_data['St_Total']>0 else np.nan
            xf_aah = calc_data['Xf_AA_H']/calc_data['St_AA_H'] if calc_data['St_AA_H']>0 else np.nan
            xf_aa = calc_data['Xf_Black']/calc_data['St_Black'] if calc_data['St_Black']>0 else np.nan
            xf_h = calc_data['Xf_Hisp']/calc_data['St_Hisp'] if calc_data['St_Hisp']>0 else np.nan
            adj_6yr = gr_6yr
            adj_6yr_aah = gr_6yr_aah
    
        else:
            adj_6yr = gr_6yr
            adj_6yr_aah = gr_6yr_aah
            
    # If there was no data in the most recent year, we got the prior (and stick--no need to add prior prior)
    elif ix in year_dfs['one_removed'].index:
        ty = year_dfs['one_removed'].loc[ix]
        gr_source = '2015'
        gr_6yr,gr_6yr_aah,gr_6yr_aa,gr_6yr_h,xf,xf_aah,xf_aa,xf_h = ty.reindex(
            ['GR_Total','GR_AA_H','GR_Black','GR_Hisp','Xfr_Total','Xfr_AA_H','Xfr_Black','Xfr_Hisp'])
        adj_6yr = gr_6yr
        adj_6yr_aah = gr_6yr_aah
    
    # If no data in the last two years, we'll go to prior prior (and stick--no need to check CI)
    elif ix in year_dfs['two_removed'].index:
        ty = year_dfs['two_removed'].loc[ix]
        gr_source = '2014'
        gr_6yr,gr_6yr_aah,gr_6yr_aa,gr_6yr_h,xf,xf_aah,xf_aa,xf_h = ty.reindex(
            ['GR_Total','GR_AA_H','GR_Black','GR_Hisp','Xfr_Total','Xfr_AA_H','Xfr_Black','Xfr_Hisp'])
        adj_6yr = gr_6yr
        adj_6yr_aah = gr_6yr_aah
    
    # No data in any of the last 3 years
    else:
        gr_source,adj_6yr,adj_6yr_aah,gr_6yr,gr_6yr_aah,gr_6yr_aa,gr_6yr_h,xf,xf_aah,xf_aa,xf_h=['N/A']+[np.nan]*10
        
    # 2 year schools are given 
    if df['Type'] == '2 year':
        adj_6yr = adj_6yr+0.5*xf
        adj_6yr_aah = adj_6yr_aah+0.5*xf_aah
        
    return [gr_source,
            np.round(adj_6yr,decimals=2),np.round(adj_6yr_aah,decimals=2),
            np.round(gr_6yr,decimals=2),np.round(gr_6yr_aah,decimals=2),
            np.round(gr_6yr_aa,decimals=2),np.round(gr_6yr_h,decimals=2),
            np.round(xf,decimals=2),np.round(xf_aah,decimals=2),
            np.round(xf_aa,decimals=2),np.round(xf_h,decimals=2)]

new_columns = ['GR_Source','Adj6yrGrad','Adj6yrAAH','6yrGrad',
               '6yrAAH','6yrAA','6yrH','Xfer','XferAAH','XferAA','XferH']
dir_df[new_columns] = dir_df.apply(set_gradrates,axis=1,args=(year_dfs,),result_type="expand")
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
      <th>HBCU</th>
      <th>Type</th>
      <th>GR_Source</th>
      <th>Adj6yrGrad</th>
      <th>Adj6yrAAH</th>
      <th>6yrGrad</th>
      <th>6yrAAH</th>
      <th>6yrAA</th>
      <th>6yrH</th>
      <th>Xfer</th>
      <th>XferAAH</th>
      <th>XferAA</th>
      <th>XferH</th>
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
      <th></th>
      <th></th>
      <th></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>100654</th>
      <td>Alabama A &amp; M University</td>
      <td>Yes</td>
      <td>4 year</td>
      <td>2016</td>
      <td>0.27</td>
      <td>0.43</td>
      <td>0.27</td>
      <td>0.28</td>
      <td>0.28</td>
      <td>0.00</td>
      <td>0.38</td>
      <td>0.37</td>
      <td>0.37</td>
      <td>0.75</td>
    </tr>
    <tr>
      <th>100663</th>
      <td>University of Alabama at Birmingham</td>
      <td>No</td>
      <td>4 year</td>
      <td>2016</td>
      <td>0.53</td>
      <td>0.49</td>
      <td>0.53</td>
      <td>0.49</td>
      <td>0.49</td>
      <td>0.43</td>
      <td>0.24</td>
      <td>0.27</td>
      <td>0.26</td>
      <td>0.36</td>
    </tr>
    <tr>
      <th>100690</th>
      <td>Amridge University</td>
      <td>No</td>
      <td>4 year</td>
      <td>2016</td>
      <td>0.29</td>
      <td>0.33</td>
      <td>0.29</td>
      <td>0.33</td>
      <td>0.33</td>
      <td>NaN</td>
      <td>0.71</td>
      <td>0.67</td>
      <td>0.67</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>100706</th>
      <td>University of Alabama in Huntsville</td>
      <td>No</td>
      <td>4 year</td>
      <td>2014-2016</td>
      <td>0.48</td>
      <td>0.34</td>
      <td>0.48</td>
      <td>0.34</td>
      <td>0.33</td>
      <td>0.36</td>
      <td>0.32</td>
      <td>0.43</td>
      <td>0.44</td>
      <td>0.39</td>
    </tr>
    <tr>
      <th>100724</th>
      <td>Alabama State University</td>
      <td>Yes</td>
      <td>4 year</td>
      <td>2016</td>
      <td>0.22</td>
      <td>0.37</td>
      <td>0.22</td>
      <td>0.22</td>
      <td>0.22</td>
      <td>0.33</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
  </tbody>
</table>
</div>




```python
dir_df.to_csv(gr_output,na_rep='N/A')
```

# A few more manual steps
## These should eventually be moved to code, but here are a few more checks:
1. Add a correction for schools where we have a lot of is historic results. Historically, this has meant reducing grad rates for schools by 1/3 of the difference between Noble retention and university retention
2. Increase grad rates for partner colleges (15%)
3. Double check schools known to report oddly: Robert Morris University-Illinois specifically
4. Look for major shifts in grad rate at schools many Noble students attend and consider shifting to a 3year average

In all of these cases, change the grad rates and the "GR_Source" to designate that a non-standard practice was followed
