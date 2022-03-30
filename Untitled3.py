#!/usr/bin/env python
# coding: utf-8

# In[35]:


import pandas as pd
import numpy as np
import math


# In[1]:


sales_casanblanca = pd.read_excel('C:/laragon/www/stat_vente/Sales_Casanblanca.xls', converters={'REF':str,'DESIGNATION':str})
sales_dekon = pd.read_excel('C:/laragon/www/stat_vente/Sales_Dekon.xls', converters={'REF':str,'DESIGNATION':str})
sales = pd.concat([sales_casanblanca, sales_dekon]).reset_index(drop=True)
#sales = pd.read_excel('E:/DollarStore/Modele_Previsions/sales_all.xlsx', converters={'REF':str,'DESIGNATION':str})
sales['DATE'] = pd.to_datetime(sales['DATE'], errors='coerce')

#print(sales_casanblanca.shape)
#print(sales_dekon.shape)
print(sales.shape)
sales.head()


# In[9]:


sales = sales[sales.REF.notnull()]
first_period= min(sales['DATE'])
last_period= max(sales['DATE'])

all_dates=pd.date_range(start=first_period, end=last_period, freq='M')

#all_period = pd.to_datetime([first_period, last_period])
all_period = all_dates.to_period("M")

#aaa= all_period.to_period("M")
print(all_dates)
print(all_period)
df_period= all_period.to_frame()
df_period.columns = ['period']
print (df_period)


# In[11]:


sales['period'] = sales['DATE'].dt.to_period("M")
sales.head()


# In[12]:


period_sales=sales.groupby(['REF','DESIGNATION', 'period'], as_index=False)['QTE'].sum()
period_sales.head()


# In[13]:


unique_items=period_sales.drop_duplicates(['REF','DESIGNATION'])[['REF','DESIGNATION']]
#period_sales.groupby(['REF','DESIGNATION'], as_index=False)
unique_items.head()
#print (unique_items)
tb=pd.DataFrame()
for row in df_period['period']:
    tmp = unique_items.copy()
    tmp['period']=row
    tb = pd.concat([tb, tmp]).reset_index(drop=True)
#aaaa = tb[tb.REF=='1']
print (tb)
print (unique_items)


# In[14]:


all_period_sales = pd.merge(period_sales, tb, on=['REF', 'DESIGNATION', 'period'], how='right')
#all_period_sales.to_excel("E:/DollarStore/Modele_Previsions/output1.xlsx")
#all_period_sales.index = all_period_sales['period']
#all_period_sales.to_excel("E:/DollarStore/Modele_Previsions/output2.xlsx")

#all_period_sales = (all_period_sales.groupby(['REF', 'DESIGNATION'])['QTE'].apply(lambda x: x.resample('M').interpolate()))

#all_period_sales['QTE2'] = all_period_sales.groupby(['REF', 'DESIGNATION', 'period']).apply(lambda group: group.interpolate(method='linear'))

#all_period_sales.groupby(['REF', 'DESIGNATION', 'period']).interpolate()

#all_period_sales= all_period_sales.groupby(['REF', 'DESIGNATION', 'period']).mean()
#all_period_sales.to_excel("E:/DollarStore/Modele_Previsions/output3.xlsx")
#period_sales = period_sales.merge(tb, how='rigth', on='None')
#aaaa = all_period_sales[all_period_sales.REF=='3470']
print(all_period_sales)


# In[16]:


tb_all_items=pd.DataFrame()   
for index, row_item in unique_items.iterrows():
    ref = row_item['REF']
    designation = row_item['DESIGNATION']
    tb_item = all_period_sales[(all_period_sales["REF"]==ref) & (all_period_sales["DESIGNATION"]==designation)]
    tb_item = tb_item.sort_values(by=['period'], ascending=True)
    #print(tb_item)
    #tb_item.interpolate(method ='linear')
    tb_item['QTE'].interpolate(method="linear", inplace=True)
    tb_item['QTE_MA'] = tb_item['QTE'].rolling(3).mean()
    tb_all_items = pd.concat([tb_all_items, tb_item]).reset_index(drop=True)
    #print(tb_item)
print(tb_all_items)


# In[17]:


#tb_all_items['month'] = tb_all_items['period'].dt.to_period("M")
tb_all_items['mois'] = tb_all_items['period'].dt.month
print(tb_all_items)


# In[46]:


#tb_all_items_by_month=tb_all_items.groupby(['REF','DESIGNATION', 'mois'], as_index=False)['QTE_MA'].mean()
#tb_all_items_by_month=tb_all_items.groupby(['REF','DESIGNATION', 'mois'], as_index=False)['QTE_MA'].mean().round(0)
tb_all_items_by_month=tb_all_items.groupby(['REF','DESIGNATION', 'mois'], as_index=False)['QTE_MA'].mean()
tb_all_items_by_month["QTE_MA_Entier"] = np.floor(tb_all_items_by_month["QTE_MA"])
tb_all_items_by_month["QTE_MA_Modulo"] = tb_all_items_by_month["QTE_MA"]%1
#tb_all_items_by_month["QTE_MA_plus"] = tb_all_items_by_month["QTE_MA"]*1.10
#tb_all_items_by_month["QTE_MA_plus_round"] = tb_all_items_by_month["QTE_MA_plus"].round(0)
tb_all_items_by_month['QTE_MA_Round'] = np.where(tb_all_items_by_month['QTE_MA_Modulo'] > 0, tb_all_items_by_month["QTE_MA_Entier"]+1,tb_all_items_by_month["QTE_MA_Entier"])
tb_all_items_by_month.to_excel("E:/DollarStore/Modele_Previsions/tb_all_items_by_month.xlsx")
print(tb_all_items_by_month)


# In[ ]:




