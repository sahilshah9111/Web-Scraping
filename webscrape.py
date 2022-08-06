import requests
from bs4 import BeautifulSoup
import pandas as pd 

url = 'https://www.eqsis.com/nse-derivative-scanners/'
response = requests.get(url)

#print(response.status_code)
#print(response.content)

soup = BeautifulSoup(response.content, 'html.parser')
stat_table = soup.find('table', id= 'table_1')
#stat_table= stat_table[0]

res=[]
for row in stat_table.find_all('tr'):
    #for cell in row.find_all('td'):
        #print(cell.text)
    td = row.find_all('td')
    tr = [row.text.strip() for row in td if row.text.strip()]
    if tr:
        res.append(tr)


df = pd.DataFrame(res, columns=["Symbol", "T.Price", "Price %CHG", "OI %CHG", "OI CHG QTY", "OI Strength", "Delivery%", "Volume%CHG", "Open Interest Filter", "Volume Filter"])
#print(df)

df = df.drop(df.index[len(df)-1])
#print(df)

#with open ('nse_stats.txt','w') as r:
   # for row in stat_table.find_all('tr'):
       # for cell in row.find_all('td'):
        #    r.write(cell.text.ljust(20))
        #r.write('\n')

#def volume_surge(row):
   # if row['Open Interest Filter'] == 'Volume Surge' or row['Volume Filter'] == 'Volume Surge':
      #  return True



df['Long Added'] = 0
df.loc[df['Open Interest Filter'] == 'Long Added', 'Long Added'] = 1
df.loc[df['Volume Filter'] == 'Long Added', 'Long Added'] = 1

df['Long Unwinding'] = 0
df.loc[df['Open Interest Filter'] == 'Long Unwinding', 'Long Unwinding'] = 1
df.loc[df['Volume Filter'] == 'Long Unwinding', 'Long Unwinding'] = 1

df['Short Added'] = 0
df.loc[df['Open Interest Filter'] == 'Short Added', 'Short Added'] = 1
df.loc[df['Volume Filter'] == 'Short Added', 'Short Added'] = 1

df['Short Covering'] = 0
df.loc[df['Open Interest Filter'] == 'Short Covering', 'Short Covering'] = 1
df.loc[df['Volume Filter'] == 'Short Covering', 'Short Covering'] = 1

df['Top Traded'] = 0
df.loc[df['Open Interest Filter'] == 'Top Traded', 'Top Traded'] = 1
df.loc[df['Volume Filter'] == 'Top Traded', 'Top Traded'] = 1

df['Volume Surge'] = 0
df.loc[df['Open Interest Filter'] == 'Volume Surge', 'Volume Surge'] = 1
df.loc[df['Volume Filter'] == 'Volume Surge', 'Volume Surge'] = 1

#print(df)
print(df.to_csv('WSData.csv',index = False))






 



