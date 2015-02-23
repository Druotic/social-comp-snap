### SNAP Facebook Network Analysis

This project is here only for archival purposes. There are hardcoded pieces and certain project
requirements existed which made reusability less than ideal.

Project for Social Computing Course at NCSU

Script accepts a path to a SNAP Facebook graph directory (see facebook dir) and output
file to output results. 

See README for pre-requisites/dependencies

### Usage:
 
- **Run:**

  `python p1_jjbeaver.py <path to graph directory> <output filepath>`

   e.g.

   `python p1_jjbeaver.py facebook results_jjbeaver`


Script has two primary functions:

1) Output social circle info, output format:

ego1:  
c#: <size> <#common attributes>  
.  
.  
.  
c#: <size> <#common attributes>   

ego2:  
c#: <size> <#common attributes>  
.  
.  
.  
c#: <size> <#common attributes>  

The above is printed for scenario (a) with ego part of circle and (b) with ego not part of circle.


2) Output degree of nodes, output format:

ego1:  
lowestid#: <degree>  
.  
.  
.  
highestid#: <degree>   

ego2:  
lowestid#: <degree>  
.  
.  
.  
highestid# <degree>  


See results_jjbeaver for sample output.


##### Reference: 

- [Dataset, Info, and related Paper](http://snap.stanford.edu/data/egonets-Facebook.html)
