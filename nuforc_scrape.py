from bs4 import BeautifulSoup
import requests
import pandas as pd

#Load main page to into BeautifulSoup object.
url = "http://www.nuforc.org/webreports/ndxevent.html"
website = requests.get(url)
soup = BeautifulSoup(website.content, 'html.parser')

#Extract page links and write to list.
sub_pages = ['http://www.nuforc.org/webreports/' + tag.get('href') 
             for tag in soup.find_all('a')]

#Use the same column headers for all dataframes.
cols = ['Date_Time','City','State','Shape','Duration','Summary','Posted']

#Visit each linked page and extract table data.
#First and last page are skipped because they do not contain UFO data.
panda_rows = []
for url in sub_pages[1:-1]:
    print('Fetching data from',url)
    website = requests.get(url)
    soup = BeautifulSoup(website.content, 'html.parser')
    table = soup.find('table')
    year = url.split('ndxe')[1][0:4]
    for row in table.find_all('tr')[1:]:
        t_row = []
        date_col = True
        for col in row.find_all('td'):
            if date_col:
                t_col = col.get_text().split('/')
                t_left = t_col[0] + '/' + t_col[1] + '/'
                t_right = year + t_col[2][2:]
                t_row.append(t_left + t_right)
                date_col = False
            else:
                t_row.append(col.get_text())
        pd_row = pd.DataFrame(data=[t_row], columns=cols)
        panda_rows.append(pd_row)

#Merge single row dataframes into one dataframe.
full_data = pd.concat(panda_rows, ignore_index=True)

#Write to CSV
full_data.to_csv('ufo.csv')
print('Data saved!')