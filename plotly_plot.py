#!/usr/bin/env python
# coding: utf-8

# In[82]:


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import plotly.express as px


# In[83]:


#get the data from github
df = pd.read_csv('https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv')
focus = df.copy().drop(['Lat','Long'], axis=1).set_index(['Country/Region','Province/State'])
confirm = focus.groupby('Country/Region').sum().T

df = pd.read_csv('https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_global.csv')
focus = df.copy().drop(['Lat','Long'], axis=1).set_index(['Country/Region','Province/State'])
death = focus.groupby('Country/Region').sum().T

df = pd.read_csv('https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_recovered_global.csv')
focus = df.copy().drop(['Lat','Long'], axis=1).set_index(['Country/Region','Province/State'])
recover = focus.groupby('Country/Region').sum().T

for i in [confirm, recover, death]:
    i.index = pd.to_datetime(i.index)

date = pd.to_datetime("today").strftime('_%m_%d')
print('Latest update time is:',date)

confirm['time'] = pd.to_datetime(confirm.index)
confirm.index = confirm.time.dt.strftime('%m/%d/%Y')
confirm.drop('time', axis=1, inplace=True)


# In[84]:


do_not_include = ['Antigua and Barbuda', 'Angola', 'Benin', 'Botswana', 
                  'Burundi', 'Cabo Verde', 'Chad', 'Comoros', 
                  'Congo (Brazzaville)', 'Congo (Kinshasa)', "Cote d'lvoire", 'Central African Republic',
                  'Diamond Princess', 'Equatorial Guinea',
                  'Eritrea', 'Eswatini', 'Gabon', 
                  'Gambia', 'Ghana', 'Grenada', 'Guinea', 'Guinea-Bissau',
                  'Guyana', 'Lesotho', 'Liberia', 'Libya', 'Madagascar',
                  'Malawi', 'Maldives', 'Mauritania', 'Mozambique',
                  'MS Zaandam', 'Namibia', 'Nicaragua', 'Papua New Guinea',
                  'Rwanda', 'Saint Lucia', 
                  'Saint Vincent and the Grenadines', 'Sao Tome and Principe',
                  'Seychelles', 'Sierra Leone', 'South Sudan', 'Suriname', 'Syria', 
                  'Tanzania', 'Togo', 'Uganda', 'West Bank and Gaza',
                  'Western Sahara', 'Yemen', 'Zambia', 'Zimbabwe']


# In[85]:


winning = []
nearly_there = [] 
needs_action = []

for j, country in enumerate(confirm.iloc[-1].sort_values(ascending=False).index[:]): #Taking the confirm dataframe that has all the dates till the last update


    #choosing offsets
    if country == 'China':
        offset = 0
    elif country == 'Korea, South':
        offset = 10
    else:
        offset = 30    


    
    #leaving out countries which haven't been vetted, or have bad data
    if country in do_not_include:
        continue 
        
    #choosing font sizes for the figure title
    if len(country) > 14:
        font_size = 100
    else: 
        font_size = 130        
        
        
    focus =  confirm.loc[:,[country]].copy()[offset:]
    focus['new'] = focus[country] - focus[country].shift(1)
    
    # Correcting some data
    if country == 'France':
        focus.at['06/02', 'new'] = 0
        focus.at['06/04', 'new'] = 767
    if country == 'Jordan':
        focus.at['07/21', 'new'] = 0
    if country == 'Luxembourg':
        focus.at['08/28', 'new'] = 0
    if country == 'Monaco':
        focus.at['09/02', 'new'] = 0
    if country == 'San Marino':
        focus.at['09/05', 'new'] = 0
    if country == 'Ecuador':
        focus.at['09/07', 'new'] = 0
    if country == 'Ecuador':    
        focus.at['05/07', 'new'] = 0
    if country == 'Ecuador':    
        focus.at['05/09', 'new'] = 0
    if country == 'Ecuador':    
        focus.at['05/12', 'new'] = 0
    
    #computing the average over the last d days
    d = 7 #the number of recent days to average over for new cases/day     
    avg=int(focus['new'][len(focus)-d:].sum()/d) #compute average new cases for the last d days

    #averaging window
    window = 7
    focus['average'] = focus['new'].rolling(window=window, min_periods=1, center=True).mean()
    
    #choosing colors
    n_0 = 20
    f_0 = 0.5
    f_1 = 0.2
    peak = focus['average'].max()
    
    if avg <= n_0*f_0 or avg <= n_0 and avg <= f_0*peak:
        
        winning.append(country)
    elif avg <= 1.5*n_0 and avg <= f_0*peak or avg <= peak*f_1:
        
        nearly_there.append(country)
    else:
        
        needs_action.append(country)

    #window = averaging window
    window = 7
    focus['average'] = focus['new'].rolling(window=window, min_periods=1, center=True).mean()
    
 

    #correcting country names
    if country == 'Taiwan*':
        country = 'Taiwan'
    if country == 'Korea, South':
        country = 'South Korea'
    if country == 'United Arab Emirates':
        country = 'U.A.E.'
    if country == 'Bosnia and Herzegovina':
        country = 'Bosnia'


print('green = ' + str(winning))
print('\t')
print('yellow = ' + str(nearly_there))
print('\t')
print('red = ' + str(needs_action))
#print('\t')
#print('not listed: ' + str(len(do_not_include)))



# In[86]:


green = len(winning)


# In[87]:


yellow = len(nearly_there)


# In[88]:


red = len(needs_action)


# In[89]:


excluded = len(do_not_include)


# In[90]:


green


# In[91]:


yellow


# In[92]:


red


# In[93]:


excluded


# In[94]:


d = {'date' : confirm.index[-1] , 'green' : green , 'yellow': yellow , 'red': red, 'excluded':excluded}


# In[95]:


df = pd.DataFrame(data = d, index = [0])


# In[96]:


df


# In[97]:


df['date'] = pd.to_datetime(df['date'], format  = '%m/%d/%Y')


# In[98]:


df.head()


# In[99]:


df.info()


# In[100]:


df_old = pd.read_csv('total_country.csv')


# In[101]:


df_old.head()


# In[102]:


df_old.info()


# In[103]:


df_old['date'] = pd.to_datetime(df_old['date'], format  = '%m/%d/%Y')


# In[104]:


df_old.info()


# In[105]:


df_old.sort_values(['date'], inplace = True)


# In[106]:


df_old.head()


# In[107]:


df_old.tail()


# In[108]:


new_df = pd.concat([df_old,df])


# In[109]:


new_df.tail()


# In[110]:


new_df.head()


# In[111]:


new_df.info()


# In[112]:


new_df.set_index('date', inplace = True)


# In[116]:


new_df.to_csv('mycsv.csv')


# In[117]:


a = pd.read_csv('mycsv.csv')


# In[118]:


a


# In[119]:


a.info()


# In[122]:


a['date'] = pd.to_datetime(a['date'])


# In[124]:


a.set_index('date',inplace =True)


# In[125]:


a


# In[129]:


green = go.Scatter(
    x=a.index,
    y=a.green, name = 'Winning', marker_color = px.colors.qualitative.D3[2], line = dict(width=4), 
)
yellow = go.Scatter(
    x=a.index,
    y=a.yellow, name = 'Nearly There', marker_color = px.colors.qualitative.G10[2],line = dict(width=4)
)
red = go.Scatter(
    x=a.index,
    y=a.red, name = 'Needs Action', marker_color = px.colors.qualitative.G10[1],line = dict(width=4)
)

data = [green, yellow, red]
layout = dict(template="simple_white",xaxis = dict(showgrid=False, ticks='outside', mirror=True,showline=True, tickformat = '%d-%b'),
                yaxis = dict(showgrid=False, ticks='outside', mirror = True, showline = True, title = 'Number of Countries'),
                font=dict(size=18),showlegend = True, legend=dict(x=0.77, y=1.3,traceorder='normal'))
fig = go.Figure(data=data, layout=layout)

fig.show()


# In[130]:


fig.write_html("countries.html",config=dict(
               displayModeBar=False), default_height = '550px', default_width = '900px' )


# In[ ]:




