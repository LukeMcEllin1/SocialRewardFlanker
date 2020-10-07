#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul 15 18:04:09 2020

@author: mcellinluke
"""

import numpy as np
import pandas as pd
import scipy as sp
import seaborn as sns

parcount=11
alldata=np.empty([0,13])


for par in range(1,parcount): #DISABLED FOR LOOP TO DEBUG ON ONE DATA FILE
    

    filename = str(par)+'data'
    
    #coord phase: blocknumber,trial,phaseno,direection,knowledge,response,chooser,RT
    #battery phase: blocknumber,trial,phasenumber,direction,knowledge,totalpressed,spacecheck,pressed
    
    #load participant data in
    
    if par ==1:
        pardata = np.genfromtxt(filename,delimiter="\t")
    else:
        pardata = np.genfromtxt(filename,delimiter=",")
    
    #remove zeros
    pardata=pardata[pardata[:,0]>0]

    #remove too slows
    pardata=pardata[pardata[:,11]!=9999]
    
    
    #identify individual and joint block as first and last
    pardata[:,1]=pardata[:,3]>np.ceil(np.max(pardata[:,3])/2)
    
    #identify time overall
    pardata[:,2]=np.arange(len(pardata))
    
    
    #mean centered RTs
    MCRT=np.array(pardata[:,11]-np.mean(pardata[:,11]),ndmin=2)
    pardata=np.append(pardata,MCRT.T,axis=1)

    alldata=np.append(alldata,pardata,axis=0)
    

    
alldata=pd.DataFrame(alldata,columns=['Participant Number','Order','Trial_Num','Block','Trial','Social_Type','Trial_Type','targetDir','greyCount','ITI','Accuracy','RT','MCRT'])


#remove training
alldata=alldata[alldata['Block']>1]

#remove outliers
lower=np.mean(alldata['RT'])-(np.std(alldata['RT'])*3)
upper=np.mean(alldata['RT'])+(np.std(alldata['RT'])*3)

alldata=alldata[alldata['RT']>lower]
alldata=alldata[alldata['RT']<upper]


#add grand mean to mean centered 
alldata['MCRT']=alldata['MCRT']+np.mean(alldata['RT'])



#group means on participant level for each trial type
ov=alldata.groupby(['Trial_Type','Social_Type','Participant Number'],as_index=False).mean()


diffscore=alldata[alldata['Trial_Type']==1].groupby(['Social_Type','Participant Number'],as_index=False).mean()
incong=alldata[alldata['Trial_Type']==0].groupby(['Social_Type','Participant Number'],as_index=False).mean()

diffscore['RT_Diff']=incong['RT']-diffscore['RT']
diffscore['MC_Diff']=incong['MCRT']-diffscore['MCRT']




ov['Trial_Type']
#calculate IES
ov['IES']=ov['RT']*(1-ov['Accuracy'])

#remove outliers
#ov=ov[ov['Accuracy']<1]


#data plot

sns.catplot(x='Social_Type',y='MCRT',hue='Trial_Type',data=ov,kind='bar')

sns.catplot(x='Social_Type',y='MCRT',hue='Order',data=alldata,kind='bar')


for p in range(1,int(max(alldata['Participant Number']))):
    pardata=alldata[alldata['Participant Number']==int(p)]
    #sns.catplot(x='Social_Type',y='MCRT',hue='Trial_Type',data=pardata,kind='bar')
    sns.catplot(x='Block',y='MCRT',hue='Trial_Type',col='Social_Type',data=pardata,kind='bar')



#plot diffscore as an index of interference effect
sns.catplot(x='Social_Type',y='RT_Diff', data=diffscore,kind='bar')

sns.catplot(x='Social_Type',y='MCRT',hue='Trial_Type',col='Participant Number',data=alldata,kind='bar')

sns.catplot(x='Block',y='MCRT',hue='Trial_Type',col='Social_Type',data=alldata,kind='bar')

sns.lmplot(x='Trial_Num',y='RT',hue='Trial_Type',col='Social_Type',data=alldata)