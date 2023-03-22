import pandas as pd
import numpy as np
import statistics
import matplotlib.pyplot as plt
import seaborn as sns
import datetime as dt
import csv

#making data frames
activity = pd.read_csv(r'C:\Users\user\OneDrive\Documents\Track2Training\Activity.csv')
calories = pd.read_csv(r'C:\Users\user\OneDrive\Documents\Track2Training\dailyCalories_merged.csv')
intensities = pd.read_csv(r'C:\Users\user\OneDrive\Documents\Track2Training\dailyIntensities_merged.csv')
steps = pd.read_csv(r'C:\Users\user\OneDrive\Documents\Track2Training\dailySteps_merged.csv')
sleep = pd.read_csv(r'C:\Users\user\OneDrive\Documents\Track2Training\sleepDay_merged.csv')
weight = pd.read_csv(r'C:\Users\user\OneDrive\Documents\Track2Training\weightLogInfo_merged.csv')

#print and previews top 5
print(activity.head(),calories.head(),intensities.head(),steps.head(),sleep.head(),weight.head())


#look for the positions of null values per column
#activity
missing_values_count = activity.isnull().sum(), sleep.isnull().sum(), weight.isnull().sum()
missing_values_count[:]
print(missing_values_count)

#checking total number of entries in dataset
#total entries in activity
total_entries_activity = len(activity.index)
print('Total number of entries in activity:',total_entries_activity)

#total entries in weight
total_entries_weight = len(weight.index)
print('Total number of entries in weight:', total_entries_weight)

#total entries in sleep
total_entries_sleep = len(sleep.index)
print('Total number of entries in sleep:', total_entries_sleep)

#basic info
activity.info()
sleep.info()
weight.info()


#count distinct values of ID
unique_id_activity = len(pd.unique(activity['Id']))
unique_id_sleep = len(pd.unique(sleep['Id']))
unique_id_weight = len(pd.unique(weight['Id'])) 

unique_id = len(pd.unique(activity["Id"]))
print("No of unique Ids in activity, sleep and weight respectively: ", str(unique_id_activity ), str(unique_id_sleep ),  str(unique_id_weight))

#data manipulation
#date format
activity['ActivityDate'] = pd.to_datetime(activity['ActivityDate'])
sleep['SleepDay']= pd.to_datetime(sleep['SleepDay'])
weight['Date'] = pd.to_datetime(weight['Date'])
activity.info()
sleep.info()
weight.info()
#print top 5 entries
print(activity['ActivityDate'].head(), sleep['SleepDay'].head(),weight['Date'].head())

#rearrange and reindex the columns and add DayOfTheWeek as a column
df_activity= activity.reindex(columns=['Id', 'ActivityDate', 'DayOfTheWeek', 'TotalSteps', 'TotalDistance', 'TrackerDistance', 'LoggedActivitiesDistance', 'VeryActiveDistance', 'ModeratelyActiveDistance', 'LightActiveDistance','SedentaryActiveDistance', 'VeryActiveMinutes', 'FairlyActiveMinutes', 'LightlyActiveMinutes', 'SedentaryMinutes', 'Calories'])
#print first 5 rows to confirm
print(df_activity.head())

#to show the day of the week in data set
df_activity['DayOfTheWeek']= df_activity['ActivityDate'].dt.day_name()
print(df_activity["DayOfTheWeek"].head())

#rename columns
df_activity.rename(columns={'ActivityDate':'Date', 'ActivityDate':'Date', 'LoggedActivitiesDistance':'Logged_distance'}, inplace= True)
#print column names to confirm
print( df_activity.columns.values) 
df_activity.head()

#combine the dataset sleep, weight and activity in one dataframe
combined_data = df_activity.merge(sleep, on='Id').merge(weight, on='Id')
combined_data.info()



#total mins the device was logged in
df_activity['Total_mins'] = df_activity['VeryActiveMinutes'] + df_activity['FairlyActiveMinutes'] + df_activity['LightlyActiveMinutes'] + df_activity['SedentaryMinutes']
print (df_activity["Total_mins"].head(5))

#convert toal mins into total hours
df_activity['Total_hours'] = round(df_activity['Total_mins']/60)
sleep['Total_sleep'] = round(sleep['TotalMinutesAsleep']/60)
print(df_activity['Total_hours'].head(),"\n",sleep['Total_sleep'].head())

#Data Analyzation
#pull general statistics
print(combined_data.describe())

#Data Visualization
#plotting histogram
plt.style.use("default")
plt.figure(figsize=(6,4)) # specify size of the chart
plt.hist(df_activity.DayOfTheWeek, bins = 7, width = 0.6, color = "lightpink", edgecolor = "black")


#adding annotations and visuals
plt.xlabel("Day Of The Week")
plt.ylabel("Frequency")
plt.title("No of times the user logged in app across the week")
plt.grid(True)
plt.show()

#Histogram for total steps for each user
#make dataframe
plt.style.use("default")
plt.figure(figsize=(6,4))
plt.hist(df_activity.VeryActiveMinutes, bins = 25, alpha = 0.6, color = "red", edgecolor='black')
plt.hist(df_activity.FairlyActiveMinutes, bins = 25, alpha = 0.6, color = "blue", edgecolor='black')
plt.hist(df_activity.LightlyActiveMinutes, bins = 25, alpha = 0.6, color = "yellow", edgecolor='black')
plt.hist(df_activity.SedentaryMinutes, bins = 25, alpha = 0.6, color = "green", edgecolor='black')
  
#annotations and visuals
plt.title("Histogram with multiple variables (overlapping histogram)")
plt.xlabel("User Type")
plt.ylabel("Steps")
plt.grid(True) 
plt.legend(['VeryActiveMinutes', 'FairlyActiveMinutes', 'LightlyActiveMinutes','SedetaryMinutes'])
plt.show()

#histogram of weight vs sleep
plt.style.use("default")
plt.figure(figsize=(6,3))
plt.hist(combined_data.TotalTimeInBed, width=0.6, color="blue", edgecolor="darkblue")
plt.hist(combined_data.WeightKg, width= 0.6, color="red", edgecolor="darkred")

#annotations and visuals
plt.xlabel("Sleep")
plt.ylabel("Weight")
plt.title("Weight vs Sleep")
plt.show()


#scatter plot for total steps vs sleep
plt.style.use("default")
plt.figure(figsize=(7,4))
plt.scatter(combined_data.TotalSteps,combined_data.TotalTimeInBed, alpha=0.8, c=combined_data.TotalTimeInBed,cmap="Spectral")

#annotations and visuals
median_steps=7637
median_sleep=6
plt.colorbar(orientation='horizontal')
plt.axvline(median_steps, color='Red', label='Median Steps')
plt.axhline(median_sleep, color='Purple', label='Median Sleep')
plt.title("Total sleep vs Total steps")
plt.legend()
plt.grid()
plt.show()


#scatter plot for total step vs calories

plt.style.use("default")
plt.figure(figsize=(6,4))
plt.scatter(combined_data.TotalSteps, combined_data.Calories, alpha=0.8, c=combined_data.Calories, cmap="Spectral")

#annotations and visuals
median_steps= 7637
median_calories= 2206
plt.colorbar(orientation='horizontal')
plt.axvline(median_steps, color='Red', label='Median Steps')
plt.axhline(median_calories, color='Purple', label='Median Calories')
plt.title('Total Calories vs Total Steps')
plt.legend()
plt.grid()
plt.show()



