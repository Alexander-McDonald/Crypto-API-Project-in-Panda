#!/usr/bin/env python
# coding: utf-8

# In[1]:


import json
import ssl
import urllib.parse
import urllib.request
import certifi
import pandas as pd
import os
from time import sleep
import seaborn as sns
import matplotlib.pyplot as plt


# ====================== SINGLE TEST CALL (works as in austin.md) ======================
params = urllib.parse.urlencode({
    "start": "1",
    "limit": "15",
    "convert": "USD",
})

request = urllib.request.Request(
    f"https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest?{params}",
    headers={
        "Accept": "application/json",
        "X-CMC_PRO_API_KEY": "9ed3229aa30a4cc8a7f135016e54e639",   # ← your key from austin.md
    },
)

context = ssl.create_default_context(cafile=certifi.where())

with urllib.request.urlopen(request, context=context) as response:
    data = json.load(response)

# Normalize to DataFrame
df = pd.json_normalize(data['data'])
df['timestamp'] = pd.to_datetime('now')
print("Initial data pull successful!")
df.head()


# In[2]:


# ====================== CLEAN api_runner FUNCTION ======================
def api_runner(df):
    params = urllib.parse.urlencode({
        "start": "1",
        "limit": "15",
        "convert": "USD",
    })

    request = urllib.request.Request(
        f"https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest?{params}",
        headers={
            "Accept": "application/json",
            "X-CMC_PRO_API_KEY": "9ed3229aa30a4cc8a7f135016e54e639",
        },
    )

    context = ssl.create_default_context(cafile=certifi.where())

    with urllib.request.urlopen(request, context=context) as response:
        data = json.load(response)

    df2 = pd.json_normalize(data['data'])
    df2['timestamp'] = pd.to_datetime('now')

    if not os.path.isfile(r'C:\Users\alexa\Desktop\Panda Tutorials\api_pull.csv'):
        df.to_csv(r'C:\Users\alexa\Desktop\Panda Tutorials\api_pull.csv', index=False)
    else:
        df.to_csv(r'C:\Users\alexa\Desktop\Panda Tutorials\api_pull.csv', mode='a', header=False, index=False)


    # Append safely
    if df.empty:
        return df2
    else:
        return pd.concat([df, df2], ignore_index=True)


# In[3]:


# ====================== RUN THE LOOP (mirrors original) ======================
df = pd.DataFrame()   # start empty

for i in range(333):
    try:
        df = api_runner(df)
        print(f'API Runner completed - iteration {i+1}/333')
        sleep(60)  # sleep for 1 minute
    except Exception as e:
        print(f'Error on iteration {i+1}: {e}')
        sleep(60)  # still wait to avoid hammering the API

print("Loop finished!")
df


# In[ ]:


# ====================== POST-PROCESSING (same as original notebook) ======================

# Show full columns
pd.set_option('display.max_columns', None)
#pd.set_option('display.max_rows', None)

# Disable scientific notation for nicer numbers
pd.set_option('display.float_format', lambda x: '%.5f' % x)

# Coin trends over time
df3 = df.groupby('name', sort=False)[[
    'quote.USD.percent_change_1h',
    'quote.USD.percent_change_24h',
    'quote.USD.percent_change_7d',
    'quote.USD.percent_change_30d',
    'quote.USD.percent_change_60d',
    'quote.USD.percent_change_90d'
]].mean()
df3


# In[6]:


df72 = pd.read_csv(r'C:\Users\alexa\Desktop\Panda Tutorials\api_pull.csv')
df72


# In[5]:


pd.options.display.float_format = '{:,.2f}'.format


# In[7]:


df


# In[11]:


df9 = df.groupby('name', sort=False)[['infinite_supply', 'circulating_supply', 'total_supply', 'max_supply']].mean()
df9


# In[12]:


df10 = df9.stack()
df10


# In[14]:


type(df10)


# In[21]:


df11 = df10.to_frame(name='values')
df11


# In[17]:


df10.count()


# In[33]:


index = pd.Index(range(52))

df11 = df10.reset_index()
df11


# In[43]:


df12 = df11.rename(columns={'level_1': 'supply'})
df13 = df12.rename(columns={0: 'values'})
df13


# In[49]:


df13['supply'] = df13['supply'].replace(['max_supply', 'infinite_supply', 'total_supply', 'circulating_supply'],['max', 'infinite', 'total', 'circulating'])
df13


# In[46]:


import seaborn as sns
import matplotlib.pyplot as plt


# In[50]:


sns.catplot(x='supply', y='values', hue='name', data=df13, kind='point')


# In[55]:


df14 = df[['name', 'quote.USD.price','timestamp']]
df14 = df14.query("name == 'Bitcoin'")
df14


# In[56]:


sns.set_theme(style="darkgrid")

sns.lineplot(x='timestamp', y='quote.USD.price', data = df14)


# In[ ]:




