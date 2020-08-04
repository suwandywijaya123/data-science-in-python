# The following code loads the olympics dataset (olympics.csv), which was derrived from the Wikipedia entry on [All Time Olympic Games Medals](https://en.wikipedia.org/wiki/All-time_Olympic_Games_medal_table), and does some basic data cleaning. 
# 
# The columns are organized as # of Summer games, Summer medals, # of Winter games, Winter medals, total # number of games, total # of medals. Use this dataset to answer the questions below.


#load csv file

import pandas as pd

df = pd.read_csv('olympics.csv', index_col=0, skiprows=1)

for col in df.columns:
    if col[:2]=='01':
        df.rename(columns={col:'Gold'+col[4:]},inplace=True)
    if col[:2]=='02':
        df.rename(columns={col:'Silver'+col[4:]}, inplace=True)
    if col[:2]=='03':
        df.rename(columns={col:'Bronze'+col[4:]}, inplace=True)
    if col[:1]=='№':
        df.rename(columns={col:'#'+col[1:]}, inplace=True)
        
names_ids = df.index.str.split('\s\(') # split the index by '('

df.index = names_ids.str[0] # the [0] element is the country name (new index) 
df['ID'] = names_ids.str[1].str[:3] # the [1] element is the abbreviation or ID (take first 3 characters from that)

df = df.drop('Totals')
 
df.head()


# ### Question 1
# Which country has won the most gold medals in summer games?
# *This function should return a single string value.*

def answer_one():
    return df['Gold'].idxmax()

answer_one()


# ### Question 2
# Which country had the biggest difference between their summer and winter gold medal counts?
# 
# *This function should return a single string value.*

# In[4]:

def answer_two():
    df['diff']=df['Gold.1']-df['Gold']
    df['diff']=df['diff'].abs()
    return df['diff'].idxmax()

answer_two()


# ### Question 3
# Which country has the biggest difference between their summer gold medal counts and winter gold medal counts relative to their total gold medal count? 
# 
# $$\frac{Summer~Gold - Winter~Gold}{Total~Gold}$$
# 
# Only include countries that have won at least 1 gold in both summer and winter.
# 
# *This function should return a single string value.*

def answer_three():
    df1=df[(df['Gold.1'] > 0) & (df['Gold'] > 0)]
    df1['diff_goldcount']= (df1['Gold']-df1['Gold.1'])/df1['Gold.2']
    df1['diff_goldcount']= df1['diff_goldcount'].abs()
    return df1['diff_goldcount'].idxmax()

answer_three()


# ### Question 4
# Write a function that creates a Series called "Points" which is a weighted value where each gold medal (`Gold.2`) counts for 3 points, silver medals (`Silver.2`) for 2 points, and bronze medals (`Bronze.2`) for 1 point. The function should return only the column (a Series object) which you created, with the country names as indices.
# 
# *This function should return a Series named `Points` of length 146*

def answer_four():
    df['points']= df['Gold.2']*3+ df['Silver.2']*2 + df['Bronze.2']*1
    points= df['points']
    return points

answer_four()



# ## Part 2
# For the next set of questions, we will be using census data from the [United States Census Bureau](http://www.census.gov). Counties are political and geographic subdivisions of states in the United States. This dataset contains population data for counties and states in the US from 2010 to 2015. [See this document](https://www2.census.gov/programs-surveys/popest/technical-documentation/file-layouts/2010-2015/co-est2015-alldata.pdf) for a description of the variable names.
# 
# The census dataset (census.csv) should be loaded as census_df. Answer questions using this as appropriate.


#load csv file

census_df = pd.read_csv('census.csv')
census_df.head()


# ### Question 5
# Which state has the most counties in it? (hint: consider the sumlevel key carefully! You'll need this for future questions too...)
# 
# *This function should return a single string value.*

def answer_five():
    state_sum= census_df.groupby('STNAME').COUNTY.sum()
    return state_sum.idxmax()

answer_five()


# ### Question 6
# **Only looking at the three most populous counties for each state**, what are the three most populous states (in order of highest population to lowest population)? Use `CENSUS2010POP`.
# 
# *This function should return a list of string values.*

def answer_six():
    census_df_table=census_df.query("SUMLEV==50")
    census_df1=census_df_table.groupby(['STNAME','CTYNAME']).CENSUS2010POP.sum()
    census_df2=pd.DataFrame(census_df1.groupby(level='STNAME').nlargest(3).reset_index(level=0,drop=True))
    census_df3=census_df2.reset_index().groupby('STNAME').CENSUS2010POP.sum().nlargest(3)
    return list(census_df3.index)

answer_six()



# ### Question 7
# Which county has had the largest absolute change in population within the period 2010-2015? (Hint: population values are stored in columns POPESTIMATE2010 through POPESTIMATE2015, you need to consider all six columns.)
# 
# e.g. If County Population in the 5 year period is 100, 120, 80, 105, 100, 130, then its largest change in the period would be |130-80| = 50.
# 
# *This function should return a single string value.*

def answer_seven():
    census_df_table=census_df.query("SUMLEV==50")
    census_df_table['change']=census_df_table.loc[:,'POPESTIMATE2010':'POPESTIMATE2015'].max(axis=1)-census_df_table.loc[:,'POPESTIMATE2010':'POPESTIMATE2015'].min(axis=1)
    census_df_table['change']=census_df_table['change'].abs()
    difference=census_df_table.groupby('CTYNAME').change.max()
    return  difference.idxmax()

answer_seven()


# ### Question 8
# In this datafile, the United States is broken up into four regions using the "REGION" column. 
# 
# Create a query that finds the counties that belong to regions 1 or 2, whose name starts with 'Washington', and whose POPESTIMATE2015 was greater than their POPESTIMATE 2014.
# 
# *This function should return a 5x2 DataFrame with the columns = ['STNAME', 'CTYNAME'] and the same index ID as the census_df (sorted ascending by index).*

def answer_eight():
    filter_query=census_df["CTYNAME"].str.startswith('Washington') 
    filter_query=census_df[filter_query]
    filter_query=filter_query.query("SUMLEV==50 & REGION==1 | REGION ==2")
    filter_query=filter_query.query("POPESTIMATE2015>POPESTIMATE2014")
    final_filter_query=filter_query.iloc[:, [5,6]]
    return  final_filter_query

answer_eight()






