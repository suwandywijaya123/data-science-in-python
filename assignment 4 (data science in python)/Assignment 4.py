# # Assignment 4 - Hypothesis Testing
# This assignment requires more individual learning than previous assignments - you are encouraged to check out the [pandas documentation](http://pandas.pydata.org/pandas-docs/stable/) to find functions or methods you might not have used yet, or ask questions on [Stack Overflow](http://stackoverflow.com/) and tag them as pandas and python related. And of course, the discussion forums are open for interaction with your peers and the course staff.
# 
# Definitions:
# * A _quarter_ is a specific three month period, Q1 is January through March, Q2 is April through June, Q3 is July through September, Q4 is October through December.
# * A _recession_ is defined as starting with two consecutive quarters of GDP decline, and ending with two consecutive quarters of GDP growth.
# * A _recession bottom_ is the quarter within a recession which had the lowest GDP.
# * A _university town_ is a city which has a high percentage of university students compared to the total population of the city.
# 
# **Hypothesis**: University towns have their mean housing prices less effected by recessions. Run a t-test to compare the ratio of the mean price of houses in university towns the quarter before the recession starts compared to the recession bottom. (`price_ratio=quarter_before_recession/recession_bottom`)
# 
# The following data files are available for this assignment:
# * From the [Zillow research data site](http://www.zillow.com/research/data/) there is housing data for the United States. In particular the datafile for [all homes at a city level](http://files.zillowstatic.com/research/public/City/City_Zhvi_AllHomes.csv), ```City_Zhvi_AllHomes.csv```, has median home sale prices at a fine grained level.
# * From the Wikipedia page on college towns is a list of [university towns in the United States](https://en.wikipedia.org/wiki/List_of_college_towns#College_towns_in_the_United_States) which has been copy and pasted into the file ```university_towns.txt```.
# * From Bureau of Economic Analysis, US Department of Commerce, the [GDP over time](http://www.bea.gov/national/index.htm#gdp) of the United States in current dollars (use the chained value in 2009 dollars), in quarterly intervals, in the file ```gdplev.xls```. For this assignment, only look at GDP data from the first quarter of 2000 onward.
# 


# Use this dictionary to map state names to two letter acronyms
states = {'OH': 'Ohio', 'KY': 'Kentucky', 'AS': 'American Samoa', 'NV': 'Nevada', 'WY': 'Wyoming', 'NA': 'National', 'AL': 'Alabama', 'MD': 'Maryland', 'AK': 'Alaska', 'UT': 'Utah', 'OR': 'Oregon', 'MT': 'Montana', 'IL': 'Illinois', 'TN': 'Tennessee', 'DC': 'District of Columbia', 'VT': 'Vermont', 'ID': 'Idaho', 'AR': 'Arkansas', 'ME': 'Maine', 'WA': 'Washington', 'HI': 'Hawaii', 'WI': 'Wisconsin', 'MI': 'Michigan', 'IN': 'Indiana', 'NJ': 'New Jersey', 'AZ': 'Arizona', 'GU': 'Guam', 'MS': 'Mississippi', 'PR': 'Puerto Rico', 'NC': 'North Carolina', 'TX': 'Texas', 'SD': 'South Dakota', 'MP': 'Northern Mariana Islands', 'IA': 'Iowa', 'MO': 'Missouri', 'CT': 'Connecticut', 'WV': 'West Virginia', 'SC': 'South Carolina', 'LA': 'Louisiana', 'KS': 'Kansas', 'NY': 'New York', 'NE': 'Nebraska', 'OK': 'Oklahoma', 'FL': 'Florida', 'CA': 'California', 'CO': 'Colorado', 'PA': 'Pennsylvania', 'DE': 'Delaware', 'NM': 'New Mexico', 'RI': 'Rhode Island', 'MN': 'Minnesota', 'VI': 'Virgin Islands', 'NH': 'New Hampshire', 'MA': 'Massachusetts', 'GA': 'Georgia', 'ND': 'North Dakota', 'VA': 'Virginia'}

## Question 1
#Returns a DataFrame of towns and the states they are in from the university_towns.txt list. 
#The format of the DataFrame should be: DataFrame( [ ["Michigan", "Ann Arbor"], ["Michigan", "Yipsilanti"] ], columns=["State", "RegionName"]  )
    
#The following cleaning needs to be done:

#1. For "State", removing characters from "[" to the end.
#2. For "RegionName", when applicable, removing every character from " (" to the end.
#3. Depending on how you read the data, you may need to remove newline character '\n'. '''


import pandas as pd
import numpy as np
from scipy.stats import ttest_ind


def get_list_of_university_towns():
    df = pd.read_csv('university_towns.txt', sep=";", names=['Region Name'])
    df.insert(0, 'State', df['Region Name'].str.extract('(.*)\[edit\]', expand=False).ffill())
    df['Region Name'] = df['Region Name'].str.replace(r' \(.+$', '')
    df = df[~df['Region Name'].str.contains('\[edit\]')].reset_index(drop=True)
    df.replace('^\s+', '', regex=True, inplace=True) 
    df.replace('\s+$', '', regex=True, inplace=True)
    df=df.rename(columns={'Region Name': 'RegionName'})
    return df

get_list_of_university_towns()

## Question 2    
#Returns the year and quarter of the recession start time as a string value in a format such as 2005q3'''.

#Returns the year and quarter of the recession end time as a string value in a format such as 2005q3'''.

#Returns the year and quarter of the recession bottom time as a string value in a format such as 2005q3'''


getlev= pd.read_excel("gdplev.xls", sheetname="Sheet1", skiprows= range(0,5), usecols=[4,5,6])
getlev.dropna(inplace=True)
getlev.rename(columns={"Unnamed: 4":"Quarter","GDP in billions of current dollars.1":"GDP in billions of current dollars",
                      "GDP in billions of chained 2009 dollars.1":"GDP in billions of chained 2009 dollars"}, inplace=True)
getlev.set_index(['Quarter'], inplace=True)

getlev['change']=getlev.loc[:,'GDP in billions of chained 2009 dollars'].diff()

getlev1=getlev.loc['2000q1':,:]


lst_start = []
lst_qtrbeforestart= []
lst_end = []
lst_bottom=[]
recession = False
for i in range(1, len(getlev1)-1):
    if not recession and (getlev1.iloc[i-1, 1] > getlev1.iloc[i, 1] > getlev1.iloc[i+1, 1]):
        recession = True
        lst_start.append(getlev1.index[i])
        lst_qtrbeforestart.append(getlev1.index[i-1])
    elif recession and (getlev1.iloc[i-1, 1] > getlev1.iloc[i, 1] < getlev1.iloc[i+1, 1]):
        recession = True
        lst_bottom.append(getlev1.index[i])
    elif recession and (getlev1.iloc[i-1, 1] < getlev1.iloc[i, 1] < getlev1.iloc[i+1, 1]):
        recession = False
        lst_end.append(getlev1.index[i+1])  

def get_recession_start():
    str1=""
    for i in lst_start:
        str1+=i

    return  str1

get_recession_start()


def get_recession_end():
    str1=""
    for i in lst_end:
        str1+=i
    
    return str1

get_recession_end()


def get_recession_bottom():
    str1=""
    for i in lst_bottom:
        str1+=i
    
    return str1

get_recession_bottom()


## Question 3 
#Converts the housing data to quarters and returns it as mean values in a dataframe. This dataframe should be a dataframe with columns for 2000q1 through 2016q3, 
#and should have a multi-index in the shape of ["State","RegionName"].
    
#Note: Quarters are defined in the assignment description, they are not arbitrary three month periods.
    
#The resulting dataframe should have 67 columns, and 10,730 rows.


def convert_housing_data_to_quarters():
    house_prices_table=pd.read_csv('City_Zhvi_AllHomes.csv')
    house_prices_table.drop(house_prices_table.iloc[:,3:51].columns, axis=1, inplace=True)
    house_prices_table.drop(house_prices_table.columns[0], axis=1, inplace=True)

    states = {'OH': 'Ohio', 'KY': 'Kentucky', 'AS': 'American Samoa', 'NV': 'Nevada', 'WY': 'Wyoming', 'NA': 'National', 'AL': 'Alabama', 'MD': 'Maryland', 'AK': 'Alaska', 'UT': 'Utah', 'OR': 'Oregon', 'MT': 'Montana', 'IL': 'Illinois', 'TN': 'Tennessee', 'DC': 'District of Columbia', 'VT': 'Vermont', 'ID': 'Idaho', 'AR': 'Arkansas', 'ME': 'Maine', 'WA': 'Washington', 'HI': 'Hawaii', 'WI': 'Wisconsin', 'MI': 'Michigan', 'IN': 'Indiana', 'NJ': 'New Jersey', 'AZ': 'Arizona', 'GU': 'Guam', 'MS': 'Mississippi', 'PR': 'Puerto Rico', 'NC': 'North Carolina', 'TX': 'Texas', 'SD': 'South Dakota', 'MP': 'Northern Mariana Islands', 'IA': 'Iowa', 'MO': 'Missouri', 'CT': 'Connecticut', 'WV': 'West Virginia', 'SC': 'South Carolina', 'LA': 'Louisiana', 'KS': 'Kansas', 'NY': 'New York', 'NE': 'Nebraska', 'OK': 'Oklahoma', 'FL': 'Florida', 'CA': 'California', 'CO': 'Colorado', 'PA': 'Pennsylvania', 'DE': 'Delaware', 'NM': 'New Mexico', 'RI': 'Rhode Island', 'MN': 'Minnesota', 'VI': 'Virgin Islands', 'NH': 'New Hampshire', 'MA': 'Massachusetts', 'GA': 'Georgia', 'ND': 'North Dakota', 'VA': 'Virginia'}
    hprices.replace({'State':states}, inplace = True)
    
    house_prices_table.set_index(['State','RegionName'],inplace = True)

    house_price = house_prices_table.groupby(pd.PeriodIndex(house_prices_table.columns, freq='Q'), axis=1).mean()
    
    return house_price

convert_housing_data_to_quarters()


## Question 4 
#First creates new data showing the decline or growth of housing pricesbetween the recession start and the recession bottom. 
#Then runs a ttestcomparing the university town values to the non-university towns values, return whether the alternative hypothesis (that the two groups are the same) is true or not as well as the p-value of the confidence. 
#Return the tuple (different, p, better) where different=True if the t-test is True at a p<0.01 (we reject the null hypothesis), or different=False if otherwise (we cannot reject the null hypothesis). 
#The variable p should be equal to the exact p value returned from scipy.stats.ttest_ind(). 
#The value for better should be either "university town" or "non-university town" depending on which has a lower mean price ratio (which is equivilent to a reduced market loss).'''

      
def run_ttest():
    str_qtrbeforestart=''
    for i in lst_qtrbeforestart:
            str_qtrbeforestart+=i
    college = get_list_of_university_towns().set_index(['State','RegionName'])      
    
    begins = get_recession_start()
    endings = get_recession_end()
    low = get_recession_bottom()
    house = convert_housing_data_to_quarters()
    
    prices_qtrbeforestart = house[str_qtrbeforestart]
    prices_bottom = house[low]
    ratio = pd.DataFrame(prices_qtrbeforestart.divide(prices_bottom))
    
    mergingdata=pd.merge(ratio,college, how='outer',left_index=True, right_index=True,indicator=True)
    ratio_college=mergingdata[(mergingdata['_merge']=='both')]
    ratio_not_college=mergingdata[(mergingdata['_merge'] == 'left_only')]
    
    statistic, p_value = tuple(ttest_ind(ratio_college.iloc[:,0], ratio_not_college.iloc[:,0], nan_policy="omit"))
    outcome = statistic < 0
    different = p_value < 0.01
    better = ["non-university town", "university town"]
    (different, p_value, better[outcome])
    
    return (different, p_value, better[outcome])
    
run_ttest()





