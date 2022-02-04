import csv
import requests
from bs4 import BeautifulSoup

base_url = "https://www.cac.edu.tw/star111/system/0ColQry_for111star_5f9g8t4q"
uni_url = base_url + "/SGroup3.htm"

headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.80 Safari/537.36'}

requests.adapters.DEFAULT_RETRIES = 1
s = requests.session()
s.keep_alive = False

response = requests.get(uni_url, headers=headers)
soup = BeautifulSoup(response.content, "html.parser")

tables = soup.findChildren('table')
my_table = tables[0]
rows = my_table.findChildren(['tr'])

# init data list
data = []
data.append(['校系名稱及代碼','詳細資料'])

for row in rows:
	# cols1 finder
	cols1=row.find_all(title="校系名稱及代碼")
	# cols2 finder
	cols2=row.find_all('a')
	# list combine
	tmpcols1 = [x.text.replace(' ','') for x in cols1]
	tmpcols2 = [base_url + x1['href'].replace('./','/') for x1 in cols2]
	# export final data if cols1 not empty
	if (tmpcols1):
		cols3 = tmpcols1 + tmpcols2
		data.append(cols3)

# print(data)
# write data list into csv
with open('output.csv', 'w', newline='') as csvfile:
	writer = csv.writer(csvfile)
	writer.writerows(data)
