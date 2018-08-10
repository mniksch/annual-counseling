
# coding: utf-8

# # Processing of Barrons ratings
# 
# ## This step is relatively complicated and has the following components:
# 
# 1. _(Completed previously)_Log into a Barrons online account and use DownThemAll! to download every page using [this hack of a webpage](../raw_inputs/barrons_grab_html_page.html)
# 2. _(Completed previously)_Run the code from [this repository](https://github.com/NobleNetworkCharterSchools/barrons-ratings) to extract the raw Barrons ratings into a simple CSV file with college names and initial Barrons ratings (this is saved locally in the raw_inputs directory)
# 3. Match the rows in the last step to rows in the master table _(done in this workbook)_
# 4. Use the admissions results data file to: _(done in this workbook)_
# 
#  a. Infer Barrons ratings for unrated colleges  
#  b. Create a "Most Competitive+" rating for Most Competitive schools that admit 25% or less of applicants

# In[1]:


import pandas as pd
import numpy as np
from fuzzywuzzy import process #for matching names
import os

# Edit these to reflect any changes
os.chdir('../inputs')
directory_file = 'hd2017.csv'
admissions_file = 'adm2016.csv'
inst_char_file = 'ic2017.csv'
barrons_file = '../raw_inputs/barrons_scrapes.csv'
matched_barrons_file = 'draft_barrons.csv'
clean_barrons_file = '../raw_inputs/true_barrons.csv'


# In[ ]:


# Load the master directory for names and alias
dir_df = pd.read_csv(directory_file, index_col=['UNITID'],
                     usecols=['UNITID','INSTNM','IALIAS','CITY','STABBR','ZIP'],
                     dtype={'ZIP':str},
                     encoding='latin-1')
dir_df['ZIP'] = dir_df['ZIP'].apply(lambda x: x[:5]) #lop off any plus 4 codes
dir_df.head()


# In[ ]:


#then load the result of the Barrons scrapes
barron_df = pd.read_csv(barrons_file, dtype={'ZipCode':str}, keep_default_na=False)
barron_df['ZipCode'] = barron_df['ZipCode'].apply(lambda x: x[:5]) #lop off any plus 4 codes
barron_df.head()


# In[ ]:


# Now we'll create a simple dictionary with the (HD) name:states:zips as keys and the UNITID as values
dir_df['NameStateZip']=dir_df.INSTNM+':'+dir_df.STABBR+':'+dir_df.ZIP
dict_names = dir_df.NameStateZip.to_dict() # has key as UNITID and value as name:state
dict_unitids = {y:x for x,y in dict_names.items()}


# In[ ]:


# Now, we're going to flag any rows in the Barrons file that already have college names that are duplicates of each other
# When comparing the name, state, and zip; we'll need to inspect those manually
barron_df['NameStateZip'] = barron_df['College Name']+':'+barron_df.State+':'+barron_df.ZipCode
barrons_name_count = barron_df[['NameStateZip','file_name']].groupby(['NameStateZip']).count()
names_with_dupes = barrons_name_count[barrons_name_count.file_name > 1].index
barron_df['check'] = barron_df['NameStateZip'].apply(lambda x: 'internal dupe' if (x in names_with_dupes) else 'clean')
print('Total Barrons list names with duplicates: %d' % sum(barron_df['check']=='internal dupe'))
barron_df.head()


# In[ ]:


# Now that we've started to catch duplicates, lets append exact matches to the Barrons table
def match_exact(df, ref_dict):
    name = df['NameStateZip']
    if name in ref_dict:
        return ref_dict[name], name[:(name.find(':'))], name[-5:], 100
    else:
        return 'TBD', 'TBD', 'TBD', 0

barron_df[['UNITID','MatchName','MatchZip','MatchConfidence']]=barron_df.apply(match_exact, axis=1, args=(dict_unitids,),
                                                                   result_type="expand")
barron_df.head()


# In[ ]:


print('After exact matches, still need to match %d colleges' % sum(barron_df['MatchName']=='TBD'))


# In[ ]:


# This code here is a little fancy, but is for creating a resource to use in the next section
def create_statematch_dicts(source_dict):
    """
    For each unique state, creates a dict of name->name:state:zip for only those states.
    We'll use this to (a) send the keys to a matching analysis per state and (b) dereference
    (with the value) back to the main UNITID dict
    """
    states = [y for x,y,z in [tups.split(sep=':') for tups in source_dict.keys()]]
    states = set(states)
    out_dict = {}
    for state in states:
        state_names = [names for names in source_dict.keys() if ':'+state+':' in names]
        out_dict[state] = {(x[:(x.find(':'))]):x for x in state_names}
    return out_dict

statematch_dict = create_statematch_dicts(dict_unitids)


# In[ ]:


# Rather than using the apply feature of Pandas, we're going to loop through with an index in
# order to report out progress since fuzzy matching can take a long time and we want to make
#sure the process doesn't hang.
ix_for_match = barron_df[barron_df['MatchName']=='TBD'].index
for i in range(len(ix_for_match)):
    if i%5 == 0:
        print('%d.' % i, flush=True, end='')
    ix = ix_for_match[i]
    current_name = barron_df.loc[ix,'College Name']
    current_state = barron_df.loc[ix,'State']
    if current_state in statematch_dict: #this only runs for American states
        names_for_match = statematch_dict[current_state].keys()
        match_name, confidence = process.extractOne(current_name, names_for_match)
        barron_df.loc[ix,'MatchName'] = match_name
        barron_df.loc[ix,'MatchConfidence'] = confidence
        barron_df.loc[ix,'MatchZip'] = statematch_dict[current_state][match_name][-5:]
        barron_df.loc[ix,'UNITID'] = dict_unitids[statematch_dict[current_state][match_name]]


# In[ ]:


barron_df.head()


# In[ ]:


# Now, we'll use the "check" field to flag any matches that might be suspect--low confidence and/or
# those without matching zip codes
def update_check(df):
    check = df['check']
    if check == 'clean':
        if df['MatchConfidence'] < 100:
            if df['ZipCode'] != df['MatchZip']:
                check = 'MismatchedZips'
        if df['MatchConfidence'] < 90:
            check = 'LowConfidence'
    
    return check

barron_df['check']=barron_df.apply(update_check, axis=1, result_type="expand")


# In[ ]:


# Before saving this off to vet by hand, we'll add the aliases field of the master directory to make it easier
# to compare and drop NameStateZip
barron_df.drop(columns=['NameStateZip'], inplace=True)
barron_df['Aliases'] = barron_df.UNITID.map(dir_df.IALIAS)


# ## After running the code above, you should save the result for manual inspection
# ### The goal is to result in a single new input csv with UNITID and Selectivity columns for as many
# ### colleges as can be matched (throw out rows that aren't found in the master directory)

# In[ ]:


barron_df.to_csv(matched_barrons_file, na_rep="N/A")


# ## In between these two lines, we're checking the file and saving the result
# ## with the same name; pay attention specifically to lower scored matches
# ### You can use the original Barrons web pages for assistance
# 
# As a summary, of the 1,502 colleges in the original file, 46 ended up being colleges not in the federal directory (mostly international schools), and 72 needed to be manually matched because the initial match was wrong.

# ## Now we have Barrons ratings for everything from the Barrons site, correctly matched to the directory.
# ## We still have to do the following:
# 
# 4. Use the admissions results data file to: _(done in this workbook)_
# 
#  a. Infer Barrons ratings for unrated colleges  
#  b. Create a "Most Competitive+" rating for Most Competitive schools that admit 25% or less of applicants
#  
# ## We'll pick these next steps up in a new workbook
# 
# ## As part of this process, we'll exclude Trade institutions from the list (e.g. schools must at least grant associate's degrees
