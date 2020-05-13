from bs4 import BeautifulSoup as soup
import requests
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from time import sleep as wait
try: 
	from playsound import playsound
except: pass

# Function untuk mendeklarasikan module playsound
def voice (mp3):
	try: playsound(mp3)
	except: pass

# Variable List yang ada pada program
Table, country, cases, death, recovered = [],[],[],[],[]

print('\n<'+'='*19+'>\n'+'|  COVID-19 REPORT  |'+'\n<'+'='*19+'>\n\n');voice('info.mp3')
print('Wait a Minutes..\n');voice('wait.mp3')

# mengambil data dari website
web = requests.get('https://www.worldometers.info/coronavirus/')
parsing = soup(web.text, 'html.parser')

# mengambil serta menampilkan data dari element dalam website
all_data = parsing.find_all('div',id='maincounter-wrap')
data =[(data.text.strip()) for data in all_data]

print('\n<|  Coronavirus OutBreak  |>\n\n<'+'='*28+'>')
for i in data:
    x=i.replace('\n\n',' ')
    print('| '+x)
print('<'+'='*28+'>\n')
voice('world.mp3');wait(2)

# mencari dan mengambil data dalam table
table_body = parsing.find('tbody').find_all('tr')
for data_table in table_body:
    Table.append(data_table.find_all('td'))

# mengambil dan memasukan data yang lebih spesifik ke dalam variable list
country = [columns[0].text.strip() for columns in Table]
cases = [0 if columns[1].text.strip()=='' else int(columns[1].text.strip().replace(',','')) for columns in Table]
death = [0 if columns[3].text.strip()=='' else int(columns[3].text.strip().replace(',','')) for columns in Table]
recovered = [0 if columns[5].text.strip()=='' else int(columns[5].text.strip().replace(',','')) for columns in Table]

# mengelompokkan data yang sudah diambil
data = list(zip(country,cases,death,recovered))
column = ('Country', 'Total Cases', 'Total Deaths', 'Total Recovered')

# membuat dataframe 
Index = np.arange(1,(len(country)+1))
Final_Data = pd.DataFrame(data,index=Index,columns=column)
pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
voice('country.mp3')
print('\n<|  Confirmed Cases by Country  |>\n\n',Final_Data)
wait(2)
# membuat file csv
print('\n|>  Data Saved in your document...');voice('saved.mp3')
Final_Data.to_csv('CoronaVirus-Update.csv')

# membuat data grafik
def dataGraph(value, title, x, y):
    co = list(range(len(country)))
    if value == cases:
        plt.bar(co[:10],value[:10],width=0.5,color='orange')
    else:
        plt.plot(co[:10],value[:10],color='red')
    plt.title(title+'\nCovid-19 (realtime)')
    plt.xticks(co[:10],country[:10],fontsize=7,rotation=70)
    plt.xlabel(x)
    plt.ylabel(y)
    plt.show()
    
voice('graphc.mp3')
dataGraph(value=cases , title="10 Higest Corona Cases by Country", x="Country", y="Coronavirus Case")
voice('graphd.mp3')
dataGraph(value=death , title="Death Rate from 10 Higest cases by Country", x="Country", y="Death Rate")