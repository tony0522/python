import csv
import re
import requests
from bs4 import BeautifulSoup

# global variables
base_url = "https://www.cac.edu.tw/star111/system/0ColQry_for111star_5f9g8t4q"
uni_url = base_url + "/SGroup2.htm"
headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.80 Safari/537.36'}

# init environment setting 
requests.adapters.DEFAULT_RETRIES = 1
s = requests.session()
s.keep_alive = False

# make the request connection
response = requests.get(uni_url, headers=headers)
soup = BeautifulSoup(response.content, "html.parser")

tables = soup.findChildren('table')
my_table = tables[0]
rows = my_table.findChildren(['tr'])

# init data list
data = []
data.append(['學校名稱','校系名稱','校系代碼','詳細資料'])

for row in rows:
	# cols1 finder
	cols1=row.find_all(title="校系名稱及代碼")
	# cols2 finder
	cols2=row.find_all('a')
	# list combine and space handling
	tmpcols1 = [re.sub(' +', ' ', x.text) for x in cols1]
	print(tmpcols1)
	# handling the cols2 and its sub data
	tmpcols2 = [base_url + x1['href'].replace('./','/') for x1 in cols2]

	uni_detail_urls = tmpcols2
	for uni_detail_url in uni_detail_urls:
		# make the request connection
		response_sub = requests.get(uni_detail_url, headers=headers)
		soup_sub = BeautifulSoup(response_sub.content, "html.parser")

		rows_sub = soup_sub.find_all(
			style=[
				"border-bottom-style:none", 
				"border-top-style:none ;border-bottom-style:none",
				"border-top-style:none "]
			)
		tmpcols2_sub = [x.text.replace(' ','') for x in rows_sub]
		# print(tmpcols2_sub)

	# export final data if cols1 not empty
	if (tmpcols1):
		cols3 = tmpcols1 + tmpcols2 + tmpcols2_sub
		data.append(cols3)

# write data list into csv
with open('output.csv', 'w', newline='') as csvfile:
	writer = csv.writer(csvfile)
	writer.writerows(data)
