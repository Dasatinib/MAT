#!/usr/bin/env python
# coding: utf-8

# In[1]:


#Packages

import pandas as pd
import numpy as np
import calendar
import datetime


# In[2]:


#Dataframe

##filename = input("Enter the name of the file (without extension .csv)")

##IMS=pd.read_csv(filename+".csv", thousands=',', parse_dates=["Month"])
IMS=pd.read_csv("Example one INN.csv", thousands=',', parse_dates=["Month"])


# In[3]:


#Reading US$ MNF as numbers 1/2 (changing thousands, removing dollar signs and filling in NAs)

IMS["US$ MNF"] = IMS["US$ MNF"].str.replace(',', '').str.replace('$', '')
#IMS["US$ MNF"] = IMS["US$ MNF"].str.replace('$', '') -> Possible to split the row above into two, one for replacing commas and the other one for replacing $

##IMS["US$ MNF"].fillna(0, inplace=True)
#IMS["US$ MNF"] = IMS["US$ MNF"].fillna("") -> Possible to use instead of inplace above


# In[4]:


#Reading US$ MNF as numbers 2/2 (changing astype)

IMS["US$ MNF"] = IMS["US$ MNF"].astype(float)

# In[5]:


#Prepping nan column for MAT Year

print("Creating MAT Year column")

IMS["MAT Year"] = np.nan


# In[6]:


#Defining date breakpoints for MAT

print("Determining MAT Breakpoints")

recent_date_0 = IMS["Month"].max() + pd.DateOffset(seconds=1)
recent_date_1 = IMS["Month"].max() - pd.DateOffset(years=1) + pd.DateOffset(seconds=1)
recent_date_2 = IMS["Month"].max() - pd.DateOffset(years=2) + pd.DateOffset(seconds=1)
recent_date_3 = IMS["Month"].max() - pd.DateOffset(years=3) + pd.DateOffset(seconds=1)

print(recent_date_0, recent_date_1, recent_date_2, recent_date_3)


# In[7]:


#Filling in MAT column based on Month dates

print("Filling MAT Year column")

def Month_to_MAT(Month):
    if recent_date_0>Month>recent_date_1:
        return recent_date_0.to_period('M')
    elif recent_date_1>Month>recent_date_2:
        return recent_date_1.to_period('M')
    elif recent_date_2>Month>recent_date_3:
        return recent_date_2.to_period('M')

IMS["MAT Year"] = IMS.apply(lambda x: Month_to_MAT(x["Month"]),axis=1)


# In[8]:


#For checking of months (is the dataset complete? Did the MAT Year fill in for all?)

#IMS[(IMS["Month"] == "2017-07-01 00:00:00")]   
#IMS.groupby(["MAT Year"])[["Month"]].nunique().sort_values("Month", 0)


# In[9]:


#Dropping Month

print("Dropping Month column")

MAT_IMS = IMS.drop(["Month"], axis=1)


# In[10]:


#Selecting columns to groupby

print("Determining columns for groupby")

columns=MAT_IMS.head(0)
columns=MAT_IMS.drop(["Standard Units", "US$ MNF", "KG"], axis=1)
columns=list(columns.columns)


# In[20]:


#Creating final dataframe

print("Initiating groupby")

MAT_IMS=MAT_IMS.groupby(columns).sum()


# In[12]:


# Printing final dataframe OR continue to pivot

# print("Printing file")

# MAT_IMS.to_csv("MAT OUTPUT.csv")


# In[24]:


MAT_PIVOT=MAT_IMS.unstack("MAT Year")

MAT_PIVOT.columns = [f'{i} {j}' for i, j in MAT_PIVOT.columns]

MAT_PIVOT.to_csv("MAT PIVOT.csv")