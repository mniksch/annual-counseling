# annual-counseling
## Process and Notebook for annual college counseling tool refresh
The code here is used for creating an updated college directory and
all other source tables for Noble college counseling tools

### To follow the process, click through the workbooks linked to below
### To replicate the process, run the ipynb files in Jupyter
### after pulling the repository

Note that as you run through the Workbooks you'll want to increment
the year on the core source files, so you'll need to edit the file
reference based on the newest available file (downloaded in Step 0)
_(In the future, we could potentially edit this code to look for the
existence of the newest files and push those names to a master list)_  

Development has been conducted in a private repo, but most of this process
should eventually be made public (private data marked in the list below as
such)

### These links will take you to the individual notebook for each section:
_(they should view nicely within Github and can be executed locally)_

# Jupyter Notebooks (interactive, commented description of the work):
0. [Grabbing the NCES data files](Notebooks/Step_0_Grab_data.ipynb)
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
