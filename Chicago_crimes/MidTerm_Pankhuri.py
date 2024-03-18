#Author: Pankhuri
#description: Crime analysis

#importing the libraries
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import folium
# reading the file
df = pd.read_csv("chicago_crimes_2017.csv")
df.info()

#Data cleaning process
print('\n')
shape = df.shape
print("The Shape of Chicago dataset:", shape)

# dropped if there is any duplicate in the unique key
df.drop_duplicates(subset ="ID",keep = False, inplace = True)

null = df.isnull().sum()
print('\n')
print("The null values is the dataset is: \n", null)

# Drop rows with missing values
crime_df = df.dropna()

# Convert to correct format
crime_df.index = pd.DatetimeIndex(crime_df.Date)
crime_df.loc[:, 'Ward'] = crime_df['Ward'].astype(float)
crime_df.loc[:, 'X Coordinate'] = crime_df['X Coordinate'].astype(float)
crime_df.loc[:, 'Y Coordinate'] = crime_df['Y Coordinate'].astype(float)
crime_df.loc[:, 'Latitude'] = crime_df['Latitude'].astype(float)
crime_df.loc[:, 'Longitude'] = crime_df['Longitude'].astype(float)

shape1 = crime_df.shape
print("The Shape of Chicago dataset:", shape1)
print(crime_df.describe())
print('\n')

#Data Analysis

#Number of primary crimes in chicago
crime = pd.DataFrame(crime_df[['Primary Type']].groupby('Primary Type').size().sort_values(ascending=False).rename('counts').reset_index()).iloc[:20, :]
print('The top 20 crimes in chicago at the year 2017:\n', crime)

crime.plot(x="Primary Type", y="counts", kind="barh", color = "#ff3419")
plt.title("Number of top 20 crimes in the city of Chicago")
plt.show()
print('\n')
#Number of arrest made in 2017
arrest = crime_df.groupby('Arrest')['Arrest'].agg('count').sort_values(ascending=False)
print('Number of arrest in year 2017\n', arrest)

arrest.plot(kind='pie',figsize=(5,5),autopct="%3.0f%%",colors=['#000000','#861600'],fontsize=20,explode=[0.05,.02])
plt.title('Number of arrest in year 2017',fontsize=25)
plt.tight_layout()
plt.show()
print('\n')
#Crimes per month in Chicago
plt.figure(figsize=(11,5))
crime_df.resample('M').size().plot(legend=False)
print('Number of crimes per month:\n',crime_df.resample('M').size() )
plt.title('Number of crimes per month')
plt.xlabel('Months')
plt.ylabel('Number of crimes')
plt.show()
#Crimes per day in Chicago
plt.figure(figsize=(11,5))
crime_df.resample('D').size().plot(legend=False)
print('Number of crimes per day in 2017\n', crime_df.resample('D').size())
plt.title('Number of crimes per day')
plt.xlabel('Months')
plt.ylabel('Number of crimes')
plt.show()
print('\n')
#Location where the most crimes are held
crime_loc = pd.DataFrame(crime_df[['Location Description']].groupby('Location Description').size().sort_values(ascending=False).rename('counts').reset_index()).iloc[:20, :]
print('Frequent Location\n',crime_loc)
plt.figure(figsize = (15, 10))
sns.countplot(y= 'Location Description', data = crime_df, order = crime_df['Location Description'].value_counts().iloc[:20].index)
plt.show()
print('\n')
#relation between crime and location
#top 20 primary types of crime
top_primary = crime_df['Primary Type'].value_counts().nlargest(20).index

#top 20 locations where those crimes occur
top_locations = crime_df['Location Description'].value_counts().nlargest(20).index

filtered_df = crime_df[crime_df['Primary Type'].isin(top_primary) & crime_df['Location Description'].isin(top_locations)]

pivot_table = pd.pivot_table(filtered_df, values='ID', index=['Primary Type'], columns=['Location Description'], aggfunc=np.count_nonzero)
print('The top 20 locations for the crimes in Chicago is:\n', pivot_table)
# Create a heatmap of the pivot table
plt.figure(figsize=(20, 10))
sns.heatmap(pivot_table, cmap='YlOrRd', annot=True, fmt='.0f', cbar=False)
plt.title('Relationship between Top 20 Crimes and its location in the year 2017')
plt.xlabel('Location Description')
plt.ylabel('Primary Type')
plt.show()
print('\n')

# Calculate the number of domestic and non-domestic crimes
domestic_count = df['Domestic'].value_counts()
print("Number of domestic and non-domestic crimes:\n", domestic_count)
labels = ['Non-Domestic', 'Domestic']
plt.pie(domestic_count, labels=labels, autopct='%1.1f%%', startangle=90)
plt.title('Domestic vs. Non-Domestic Crimes')
plt.show()
print('\n')

# Count the number of crimes per district
district_counts = crime_df['District'].value_counts()
district_counts = crime_df.groupby('District').size().reset_index(name='Crimes')

# Get the top 10 districts with the highest number of crimes
top_10_districts = district_counts.nlargest(10, 'Crimes')
print('Districts with highest number of cases reported:\n',top_10_districts)

plt.figure(figsize=(10, 6))
sns.barplot(x='District', y='Crimes', data=top_10_districts)
plt.title('Number of Crimes by District')
plt.xlabel('District')
plt.ylabel('Number of Crimes')
plt.show()
print('\n')

#where the crimes happened in 2017
chicago_map = folium.Map(location=[41.864073,-87.706819],
                        zoom_start=11,
                        tiles="CartoDB dark_matter")
locations = df.groupby('Community Area').first()
new_locations = locations.loc[:, ['Latitude', 'Longitude', 'Location Description', 'Arrest']]
popup_text = """Community Index : {}<br
                Arrest : {}<br>
                Location Description : {}<br>"""
for i in range(len(new_locations)):
    lat = new_locations.iloc[i][0]
    long = new_locations.iloc[i][1]
    popup_text = """Community Index : {}<br>
                Arrest : {}<br>
                Location Description : {}<br>"""
    popup_text = popup_text.format(new_locations.index[i],
                               new_locations.iloc[i][-1],
                               new_locations.iloc[i][-2]
                               )
    folium.CircleMarker(location = [lat, long], popup= popup_text, fill = True).add_to(chicago_map)

    chicago_map.save('chicago.html')

print('\n End of the program')
