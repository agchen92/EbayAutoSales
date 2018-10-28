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
rows_price_too_big=(autos['price']>900000)
autos.drop(autos.index[rows_price_too_big], inplace=True)
autos['price'].value_counts().sort_index(ascending=True)

autos['registration_year'].unique()
autos['registration_year'].describe()
autos['registration_year'].isnull().sum()
autos['registration_year'].value_counts().sort_index(ascending=True)
#Some questionable years are found. Let's remove those with years <1800
#and those greater than 2019.
questionable_years=(autos['registration_year']<1800) | (autos['registration_year']>2018)
autos.drop(autos.index[questionable_years], inplace=True)
autos['registration_year'].value_counts().sort_index(ascending=True)
#Recheck dataframe
autos.info()
autos['registration_year'].value_counts(normalize=True)
#After removing the values that were outside the upper and lower bounds
#and then looking at the normalized distribution of the remaining values,
#we can see that the years from 1998-2006 were the most popular cars to be
#sold in this classified section

autos['date_crawled']
autos['ad_created']
autos['last_seen']
#With these time stamps, we most likely do not need the HH:MM:SS timestamp
#So, lets remove these from the 'date_crawled' and 'last_seen' in order to
#extract the information regarding the years, months, and days.

#Strategy: separate time values into two parts and drop the timestamp or do .str[:10]
#to just look at the necessary info about year, months, and days.
autos['date_crawled'].str[:10].value_counts(normalize=True)
#
autos['ad_created'].str[:10].value_counts(normalize=True)
#
autos['last_seen'].str[:10].value_counts(normalize=True)
#
#Looking at the distribution of the values, we can see that most of
#the listings were created around March-April of 2016. The listings crawl
#dates do not seem to have any trend as they are all fairly distributed
#among all the dates. The 'last_seen' dates' distribution is fairly the same
#as the distribution for date created. This is expected as all ads have the same
#expiration time.

brands_top6 = autos["brand"].value_counts().head(6)

avgprice_dict = {}   
brand_names = brands_top6.index    

for name in brand_names:
    avg = autos.loc[autos["brand"] == name, "price"].mean()
    avgprice_dict[name] = round(avg, 2)

print(avgprice_dict)

#Through this script, we can see the average selling price for the vehicles
#in the top brands. From the data, it is clear that Audi has the best resell
#price. Audi, BMW, and Mercedes Benz are more expensive and have higher resale
#value. Ford and Opel are less expensive and Volkswagen is in between.

avgmileage_dict={}
brand_names = brands_top6.index

for name in brand_names:
    avg = autos.loc[autos["brand"] == name, "odometer_km"].mean()
    avgmileage_dict[name] = round(avg, 2)

print(avgmileage_dict)

#By aggregating the mileage traveled by brand, we can see the
#mean mileage of the used cars of the top brands. We can further
#look into insights by making a dataframe of this and the previous
#aggregated information.

avgprice_series=pd.Series(avgprice_dict)
avgmileage_series=pd.Series(avgmileage_dict)
agg_df=pd.DataFrame(avgprice_series, columns=['average_price'])
agg_df['average_mileage_km']=avgmileage_series
agg_df

#Alternative method for making a dataframe from two dictionaries
#data_dict={'mean_price':bmp_series,'mean_mileage_km':bmm_series}
#df=pd.DataFrame(data_dict)
#df

#By looking at the resulting dataframe that consists of average price
#and mileage of the top brands, we can see that despite higher mileages,
#the top performing brands like Audi, Benz, and BMW still manage to keep
#their value.

#Let's do some basic data cleaning and see if we can find other insights
#within the dataset.
autos['vehicle_type'].unique()

#From the data, we can see that the vehicle type column has some German words.
#So, maybe if we convert this to their English counterparts, whoever looks here
#can find some insights of their own.
#kleinwagen=sedan, kombi=van, cabrio=convertible, andere=other
#Let's lump nan with andere, just because they are both unknown in a sense.

mapping_dict={
    'bus' : 'bus',
    'limousine' : 'limousine',
    'kleinwagen' : 'sedan',
    'kombi' : 'van',
    'nan' : 'other',
    'coupe' : 'coupe',
    'suv' : 'suv',
    'cabrio' : 'convertible',
    'andre' : 'other'
    }
autos['vehicle_type']=autos['vehicle_type'].map(mapping_dict)
autos['vehicle_type'].unique()