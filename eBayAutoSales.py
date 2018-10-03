#Exploring Ebay Car Sales Data
#Taking dataset from Kaggle
#Dataset name: eBay Kleinanzeigen
#Classified section of German eBay website featuring sales of used cars
import numpy as np
import pandas as pd
autos=pd.read_csv('autos.csv',encoding='Latin-1')

#Previewing data to determine strategy
autos.info()
autos.head()
#Data contains a total of 20 columns, most of which are string
#Some columns contain null values, but none have more than 20% null
#Column names are presented in camelcase, not snakecase


#Strategy...
#Convert columns names from camelcase to snakecase and rename columns
#based on the data dictionary to be more descriptive
autos = autos.rename(columns={"yearOfRegistration": "registration_year", "monthOfRegistration": "registration_month", 
                              "notRepairedDamage": "unrepaired_damage", "dateCreated": "ad_created", "offerType": "offer_type", 
                              "fuelType": "fuel_type", "dateCrawled": "date_crawled", "nrOfPictures":"number_of_pictures", "postalCode":"postal_code", 
                              "lastSeen":"last_seen", "vehicleType": "vehicle_type", "powerPS" : "power_ps" })

autos.columns

#By changing column names to use snakecase, we can replace spaces with
#underscores and have an easier way to extract data to look into insights

#Perform some basic data edxploration to determine what cleaning tasks are needed
#Text columns that are nearly all the same values can be dropped
#since no insight can gained from that circumstance
#Columns with numeric data that are stored as tect can be cleaned and converted
autos.describe(include='all')
autos['price'].head(50)


#FINDINGS:
#Columns 'seller' and 'offer_type' has nearly the same value for each row.
#These two will be prime candidates to be dropped first
#'price' and 'odometer' are represented as objects (hence, strings) rather than integers
#These two columns should be cleaned and modified
autos=autos.drop(columns=['seller','offer_type'])
autos['price']=(autos['price'].str.replace('$','').str.replace(',','').astype(int))
autos['odometer']=(autos['odometer'].str.replace(',','').str.replace('km','').astype(int))
#Rename odometer
autos=autos.rename(columns={'odometer':'odometer_km'})


#Begin data exploration, to find outliers or discrepancys in the data
autos['odometer_km'].unique()
autos['odometer_km'].describe()
autos['odometer_km'].isnull().sum()
autos['odometer_km'].value_counts().sort_index(ascending=True)
#Through exploring the data in the 'odometer_km' column, we can see that
#there is no unreasonable outlier in the data and also no null values.
#The distribution is reasonable, so we can use every data in these columns.

autos['price'].unique()
autos['price'].describe()
autos['price'].isnull().sum()
autos['price'].value_counts().sort_index(ascending=True)
#Through exploring the data in the 'price' column, we can see that there
#is a larger number of 0USD and 1USD pricing. This is most likely a tactic
#to encourage viewers to click on the post itself. I will keep these data points.
#However, there is a few outliers surpassing >=1million USD. I will like to remove
#these since nothing that valuable would be advertised on eBay.
