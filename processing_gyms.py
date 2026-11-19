#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Aug 15 18:55:18 2024

@author: isabel_orlando
"""
import pandas as pd
import os
import webbrowser as wb
import matplotlib.pyplot as plt
import seaborn as sns
import seaborn.objects as so

#%%

#creating new dataframes for each gym from the relevant columns
#day of the week, date, time (for gym) and gym live count

df = pd.read_csv('main_data copy.csv')

df_helen = pd.DataFrame(df.iloc[:, :4])

df_noyes= pd.DataFrame(df.iloc[:, [0,1,4,5]])

df_down= pd.DataFrame(df.iloc[:, [0,1,6,7]])

df_up= pd.DataFrame(df.iloc[:, [0,1,8,9]])

df_toni= pd.DataFrame(df.iloc[:, [0,1,10,11]])

df_list=[df_helen, df_noyes, df_down, df_up, df_toni]

#%%

#convert columns to time object in pandas, create rounded intervals,
#remove duplicates for each of my 5 dataframes

#helen
df_helen['datetime']=pd.to_datetime(df_helen['Date']+' '+df['Time - Helen Newman'],
                                               format = '%m/%d/%Y %I:%M %p')
df_helen['rounded time']=df_helen['datetime'].dt.floor('30T')

df_helen=df_helen.drop_duplicates()

df_noyes['datetime']=pd.to_datetime(df_noyes['Date']+' '+df['Time - Noyes'],
                                               format = '%m/%d/%Y %I:%M %p')
#noyes
df_noyes['rounded time']=df_noyes['datetime'].dt.floor('30T')

df_noyes=df_noyes.drop_duplicates()

#down
df_down['datetime']=pd.to_datetime(df_down['Date']+' '+df['Time - Teagle Down'],
                                               format = '%m/%d/%Y %I:%M %p')
df_down['rounded time']=df_down['datetime'].dt.floor('30T')

df_down=df_down.drop_duplicates()

#up
df_up['datetime']=pd.to_datetime(df_up['Date']+' '+df['Time - Teagle Up'],
                                               format = '%m/%d/%Y %I:%M %p')
df_up['rounded time']=df_up['datetime'].dt.floor('30T')

df_up=df_up.drop_duplicates()

#toni
df_toni['datetime']=pd.to_datetime(df_toni['Date']+' '+df['Time - Toni Morrison'],
                                               format = '%m/%d/%Y %I:%M %p')
df_toni['rounded time']=df_toni['datetime'].dt.floor('30T')

df_toni=df_toni.drop_duplicates()

#%%

#visualizations 

# Group by the hour of the day and calculate the mean count for 'Helen Newman'
hourly_count = df_helen.groupby(df_helen['rounded time'].dt.hour)['Helen Newman'].mean()

# Plot the result
fig, axs = plt.subplots(figsize=(12, 4))
hourly_count.plot(kind='bar', rot=0, ax=axs)
axs.set_xlabel("Hour of the Day")
axs.set_ylabel("Mean Count for Helen Newman")
plt.title("Count for Helen Newman by Hour")

plt.savefig('/Users/isabel_orlando/Desktop/gym_project/count_per_hour_HelenNewman.png', 
            dpi=300, bbox_inches='tight')
plt.show()


