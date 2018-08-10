# annual-counseling
## Process and Notebook for annual college counseling tool refresh
The code here is used for creating an updated college directory and
all other source tables for Noble college counseling tools

### To follow the process, click through the Markdown workbooks linked to below
### To replicate the process, run the code in order in either the notebooks
### (Notebooks) or the source code (src) after pulling the repository

Note that the best practice is probably to run through the Workbooks
because there are references to data files (e.g. HD2017) that you'll want
to refresh annually. If you use the source code directly, you'll need to
edit each file to ensure you have the latest. _(In the future, we could
potentially edit this repository to look for the existence of the newest
files and push those names to a master list)_  

Development has been conducted in a private repo, but most of this process
should eventually be made public (private data marked in the list below as
such)

### This repo is divided into three main sections:

# Markdown Workbooks (interactive, commented description of the work):
0. [Grabbing the NCES data files](Markdown/Step_0_Grab_data.md)
1. [Calculating distance from Chicago](Markdown/Step_1_distance_calcs.md)
2. [Cleanup Barrons Ratings](Markdown/Step_2_get_Barrons.md)
2. [Part 2: Cleanup Barrons Ratings](Markdown/Step_2_5_Get_Barrons_inferred.md)
3. [Calculate Grad Rates](Markdown/Step_3_get_Grad_Rates.md)
4. [Combine the files](Markdown/Step_4_combine_files.md)

## More data/tools

5. [Affordability analysis](ph) (should be added to the Noble directory)
6. [Odds analysis](ph)
7. [Target calculation](ph)
8. [Playbook creation](ph)
9. [College Bot creation](ph)

# iPython Notebooks
[Notebook format of the interactive sessions shown in the Markdown](Notebooks)

# Python source
[Downloads of the Python code contained in the notebooks](src)
