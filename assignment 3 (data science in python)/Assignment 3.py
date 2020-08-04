# # Assignment 3 - More Pandas
# This assignment requires more individual learning then the last one did - you are encouraged to check out the [pandas documentation](http://pandas.pydata.org/pandas-docs/stable/) to find functions or methods you might not have used yet, or ask questions on [Stack Overflow](http://stackoverflow.com/) and tag them as pandas and python related. And of course, the discussion forums are open for interaction with your peers and the course staff.



# ### Question 1
# Load the energy data from the file `Energy Indicators.xls`, which is a list of indicators of [energy supply and renewable electricity production](Energy%20Indicators.xls) from the [United Nations](http://unstats.un.org/unsd/environment/excel_file_tables/2013/Energy%20Indicators.xls) for the year 2013, and should be put into a DataFrame with the variable name of **energy**.
#
# Keep in mind that this is an Excel file, and not a comma separated values file. Also, make sure to exclude the footer and header information from the datafile. The first two columns are unneccessary, so you should get rid of them, and you should change the column labels so that the columns are:
# 
# `['Country', 'Energy Supply', 'Energy Supply per Capita', '% Renewable']`
# 
# Convert `Energy Supply` to gigajoules (there are 1,000,000 gigajoules in a petajoule). For all countries which have missing data (e.g. data with "...") make sure this is reflected as `np.NaN` values
# 
# Rename the following list of countries (for use in later questions):
# 
# ```"Republic of Korea": "South Korea",
# "United States of America": "United States",
# "United Kingdom of Great Britain and Northern Ireland": "United Kingdom",
# "China, Hong Kong Special Administrative Region": "Hong Kong"```
# 
# There are also several countries with numbers and/or parenthesis in their name. Be sure to remove these, 
# 
# e.g. 
# 
# `'Bolivia (Plurinational State of)'` should be `'Bolivia'`, 
# 
# `'Switzerland17'` should be `'Switzerland'`.
# 
#
# Next, load the GDP data from the file `world_bank.csv`, which is a csv containing countries' GDP from 1960 to 2015 from [World Bank](http://data.worldbank.org/indicator/NY.GDP.MKTP.CD). Call this DataFrame **GDP**. 
# 
# Make sure to skip the header, and rename the following list of countries:
# 
# ```"Korea, Rep.": "South Korea", 
# "Iran, Islamic Rep.": "Iran",
# "Hong Kong SAR, China": "Hong Kong"```
# 
# Finally, load the [Sciamgo Journal and Country Rank data for Energy Engineering and Power Technology](http://www.scimagojr.com/countryrank.php?category=2102) from the file `scimagojr-3.xlsx`, which ranks countries based on their journal contributions in the aforementioned area. Call this DataFrame **ScimEn**.
# 
# Join the three datasets: GDP, Energy, and ScimEn into a new dataset (using the intersection of country names). Use only the last 10 years (2006-2015) of GDP data and only the top 15 countries by Scimagojr 'Rank' (Rank 1 through 15). 
# 
# The index of this DataFrame should be the name of the country, and the columns should be ['Rank', 'Documents', 'Citable documents', 'Citations', 'Self-citations',
#        'Citations per document', 'H index', 'Energy Supply',
#        'Energy Supply per Capita', '% Renewable', '2006', '2007', '2008',
#        '2009', '2010', '2011', '2012', '2013', '2014', '2015'].
# 
# *This function should return a DataFrame with 20 columns and 15 entries.*


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
 

def answer_one():
    
    energy = pd.read_excel("Energy Indicators.xls", sheetname='Energy',skiprows = range(0, 16),parse_cols=[2,3,4,5] )
        
    energy=energy.iloc[1:228 ,].rename(columns={'Unnamed: 0': 'Country', 
                                                'Energy Supply per capita':'Energy Supply per Capita',
                                                'Renewable Electricity Production': '% Renewable'})
    
    energy['Country'].replace(' \([^()]*\)','',regex=True,inplace=True)
    energy['Country'].replace('(\d)','',regex=True,inplace=True)
    
    energy['Country'].replace({'United Kingdom of Great Britain and Northern Ireland': 'United Kingdom',
                               "United States of America": "United States",
                               "Republic of Korea": "South Korea",
                               "China, Hong Kong Special Administrative Region": "Hong Kong"},inplace=True)    
    
    energy['Energy Supply']= energy['Energy Supply']*1000000
    energy['Energy Supply'].replace('.', np.nan,regex=True,inplace=True)
    energy.set_index(['Country'], inplace=True)
    
    GDP = pd.read_csv('world_bank.csv', skiprows=range(0,4))
    
    GDP['Country Name'].replace({"Korea, Rep.": "South Korea","Iran, Islamic Rep.": "Iran",
                                "Hong Kong SAR, China": "Hong Kong"}, inplace=True)

    
    GDP.set_index(['Country Name'], inplace=True)
    GDP= GDP.loc[:,'2006':'2015']
      
    ScimEn=pd.read_excel("scimagojr-3.xlsx", sheetname='Sheet1')
    ScimEn=ScimEn.iloc[0:15,:]
    ScimEn.set_index(['Country'], inplace=True)
    
    
    merge1=pd.merge(ScimEn,energy,how='inner',left_index=True, right_index=True)
    merge2=pd.merge(merge1,GDP,how='inner',left_index=True, right_index=True)

    Top15_table= merge2.sort_values(by ='Rank' , ascending=True)
    
    return Top15_table

answer_one()


# ### Question 2 
# The previous question joined three datasets then reduced this to just the top 15 entries. When you joined the datasets, but before you reduced this to the top 15 items, how many entries did you lose?
# 
# *This function should return a single number.*


def answer_two():
    
    merge1= pd.merge(ScimEn,energy,how='outer',left_index=True, right_index=True)
    merge2= pd.merge(merge2,GDP,how='outer',left_index=True, right_index=True)
    lose_entries=len(merge2)-len(answer_one())
    return int(lose_entries)

answer_two()


# ## Answer the following questions in the context of only the top 15 countries by Scimagojr Rank (aka the DataFrame returned by `answer_one()`)

# ### Question 3 
# What is the average GDP over the last 10 years for each country? (exclude missing values from this calculation.)
# 
# *This function should return a Series named `avgGDP` with 15 countries and their average GDP sorted in descending order.*


averageGDP['Average']=answer_one().loc[:,'2006':'2015'].mean(axis=1,skipna=True)
averageGDP=averageGDP.sort_values(by ='Average' , ascending=False)

def answer_three():
    avgGDP=averageGDP.loc[:,'Average']
    return avgGDP

answer_three()


# ### Question 4
# By how much had the GDP changed over the 10 year span for the country with the 6th largest average GDP?
# 
# *This function should return a single number.*


def answer_four():
    gdpchange_table=averageGDP
    gdpchange_table['Change']=gdpchange_table.loc[:,'2015']-gdpchange_table.loc[:,'2006']
    valueschange1 = gdpchange.iloc[5,-1]
    valueschange2 = np.float64(valueschange1)
    return valueschange2

answer_four()


# ### Question 5 
# What is the mean `Energy Supply per Capita`?
# 
# *This function should return a single number.*


def answer_five():
    mean_energy_supply=answer_one().loc[:,'Energy Supply per Capita'].mean(axis=0)
    return float(mean_energy_supply)

answer_five()


# ### Question 6 
# What country has the maximum % Renewable and what is the percentage?
# 
# *This function should return a tuple with the name of the country and the percentage.*


def answer_six():
    country_percent_rnw=answer_one()['% Renewable'].idxmax()
    value_max_percent_rnw=answer_one().loc[:,'% Renewable'].max(axis=0)
    tuple_rnw=(country_percent_rnw, value_max_percent_rnw)
    return tuple_rnw

answer_six()


# ### Question 7
# Create a new column that is the ratio of Self-Citations to Total Citations. 
# What is the maximum value for this new column, and what country has the highest ratio?
# 
# *This function should return a tuple with the name of the country and the ratio.*


def answer_seven():
    table_max_ratio=answer_one()
    table_max_ratio['RatioCitation']=table_max_ratio.loc[:,'Self-citations']/table_max_ratio.loc[:,'Citations']
    country_max_ratio=table_max_ratio['RatioCitation'].idxmax()
    max_ratio=table_max_ratio.loc[:,'RatioCitation'].max(axis=0)
    tuple_ratio=(country_max_ratio,max_ratio)
    return tuple_ratio

answer_seven()


# ### Question 8 
# 
# Create a column that estimates the population using Energy Supply and Energy Supply per capita. 
# What is the third most populous country according to this estimate?
# 
# *This function should return a single string value.*


def answer_eight():
    most_population = answer_one()
    most_population['Totalpop']=most_population.loc[:,'Energy Supply']/most_population.loc[:,'Energy Supply per Capita'].astype('float64')
    most3rdpop= most_population.sort_values(by ='Totalpop' , ascending=False).iloc[0:3,:]
    return most3rdpop.index[2]

answer_eight()


# ### Question 9 
# Create a column that estimates the number of citable documents per person. 
# What is the correlation between the number of citable documents per capita and the energy supply per capita? Use the `.corr()` method, (Pearson's correlation).
# 
# *This function should return a single number.*
# 
# *(Optional: Use the built-in function `plot9()` to visualize the relationship between Energy Supply per Capita vs. Citable docs per Capita)*


def answer_nine():
    correlation_table = answer_one()
    correlation_table['Totalpop']=correlation_table['Energy Supply']/correlation_table['Energy Supply per Capita']
    correlation_table['citabledoc/capita']=correlation_table['Citable documents']/correlation_table['Totalpop']
    correlation_table['citabledoc/capita']=pd.to_numeric(correlation_table['citabledoc/capita'])
    correlation_table['Energy Supply per Capita']=pd.to_numeric(correlation_table['Energy Supply per Capita'])
    
    correlation=correlation_table['citabledoc/capita'].corr(correlation_table['Energy Supply per Capita'])
    return correlation

answer_nine()


def plot9():
    import matplotlib as plt
    get_ipython().magic('matplotlib inline')
    
    Top15 = answer_one()
    Top15['PopEst'] = Top15['Energy Supply'] / Top15['Energy Supply per Capita']
    Top15['Citable docs per Capita'] = Top15['Citable documents'] / Top15['PopEst']
    Top15.plot(x='Citable docs per Capita', y='Energy Supply per Capita', kind='scatter', xlim=[0, 0.0006])

plot9() 


# ### Question 10 
# Create a new column with a 1 if the country's % Renewable value is at or above the median for all countries in the top 15, and a 0 if the country's % Renewable value is below the median.


def answer_ten():
    median_renewable_table=answer_one()
    median_renewable=median_renewable_table['% Renewable'].median(axis=0,skipna=True)
    median_renewable_table.loc[median_renewable_table['% Renewable'] >= median_renewable, 'above median'] = 1 
    median_renewable_table.loc[median_renewable_table['% Renewable'] < median_renewable, 'above median'] = 0 
    
    return median_renewable_table

answer_ten()

# ### Question 11 
# Use the following dictionary to group the Countries by Continent, then create a dateframe that displays the sample size (the number of countries in each continent bin), and the sum, mean, and std deviation for the estimated population of each country.
# 
# ```python
# ContinentDict  = {'China':'Asia', 
#                   'United States':'North America', 
#                   'Japan':'Asia', 
#                   'United Kingdom':'Europe', 
#                   'Russian Federation':'Europe', 
#                   'Canada':'North America', 
#                   'Germany':'Europe', 
#                   'India':'Asia',
#                   'France':'Europe', 
#                   'South Korea':'Asia', 
#                   'Italy':'Europe', 
#                   'Spain':'Europe', 
#                   'Iran':'Asia',
#                   'Australia':'Australia', 
#                   'Brazil':'South America'}
# ```
# 
# *This function should return a DataFrame with index named Continent `['Asia', 'Australia', 'Europe', 'North America', 'South America']` and columns `['size', 'sum', 'mean', 'std']`*


def answer_eleven():
    stat_continent_table = answer_one()
    stat_continent_table['Totalpop']=stat_continent_table.loc[:,'Energy Supply']/stat_continent_table.loc[:,'Energy Supply per Capita'].astype('float64')
    stat_continent_table = stat_continent_table.assign(ContinentDict = ['Asia', 'North America', 'Asia', 'Europe', 'Europe', 'North America',  
                                        'Europe', 'Asia','Europe', 'Asia', 'Europe', 'Europe', 'Asia','Australia', 
                                        'South America'])
    stat_continent=stat_continent_table.reset_index().groupby('ContinentDict').Totalpop.agg(['size','sum','mean','std'])
    return stat_continent

answer_eleven()


# ### Question 12 
# Cut % Renewable into 5 bins. Group Top15 by the Continent, as well as these new % Renewable bins. How many countries are in each of these groups?
# 
# *This function should return a __Series__ with a MultiIndex of `Continent`, then the bins for `% Renewable`. Do not include groups with no countries.*


def answer_twelve():
    group_rnw_cont_table = answer_one()
    group_rnw_cont_table['Totalpop']=group_rnw_cont_table.loc[:,'Energy Supply']/group_rnw_cont_table.loc[:,'Energy Supply per Capita'].astype('float64')
    group_rnw_cont_table = group_rnw_cont_table.assign(ContinentDict = ['Asia', 'North America', 'Asia', 'Europe', 'Europe', 'North America',  
                                                                        'Europe', 'Asia','Europe', 'Asia', 'Europe', 'Europe', 'Asia','Australia', 
                                                                        'South America'])
    group_rnw_cont_table['Bin']= pd.cut(group_rnw_cont_table['% Renewable'],5)
    group_rnw_cont_table=group_rnw_cont_table.reset_index().rename(columns={'index': 'Country'})
    group_nrw_cont= group_rnw_cont_table.groupby(['ContinentDict','Bin']).Country.agg(['size'])
    
    return group_nrw_cont.loc[:,'size']

answer_twelve()



