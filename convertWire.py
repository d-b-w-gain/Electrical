#!/usr/bin/env python
# coding: utf-8

# # Convert from AWG to CSA mm^2 using the ASTM B258-02 #
# This utility is provided for ROM convenience only.  Engineering calculation must be preformed directly from standards.

# In[3]:


import csv
import os
def AWG2CSA(gauge) :
    path=os.path.abspath('.')
    #print(path)
    fileName='B258-02-T1.csv';
    filePath=path+'/'+fileName;
    with open(filePath, mode='r') as infile:
        reader = csv.reader(infile)
        mydict = {rows[0]:rows[5] for rows in reader}
    CSA=mydict.get(str(gauge));
    return CSA


# In[4]:


## For testing
# AWG = int(input("Enter required AWG: "))
# print('For an AWG of: '+str(AWG))
# print('The Nominal CSA is: '+AWGtoCSA(AWG)+' mm\u00b2')


# In[ ]:


def CSA2AWG(CSA):
    fileName='B258-02-T1.csv';
    with open(fileName, mode='r') as infile:
        reader = csv.reader(infile)
        mydict = {rows[5]:rows[0] for rows in reader}
    del mydict["mm2"]
    with open(fileName, mode='r') as infile:
        reader = csv.reader(infile)
        mydict2 = {rows[0]:rows[5] for rows in reader}
    del mydict2["AWG"]
    AWG=mydict.get(list(dict((k, v) for k, v in mydict.items() if float(k) >= CSA).keys())[0]);
    return AWG

