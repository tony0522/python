import re
import csv
import sys
import requests
from bs4 import BeautifulSoup

# global variables
base_url = "https://www.cac.edu.tw/star111/system/0ColQry_for111star_5f9g8t4q"
headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.80 Safari/537.36'}

try:
	# need more check for sys.arv by package
	uni_url = base_url + "/SGroup" + sys.argv[1] + ".htm"
except:
	uni_url = base_url + "/SGroup2.htm"

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
data.append(['學校名稱','校系名稱','校系代碼','國文','標準','英文','標準','數學A','標準','數學B','標準','社會','標準','自然','標準','英聽','標準','詳細資料'])

for row in rows:
	# cols1 finder
	cols1=row.find_all(title="校系名稱及代碼")
	# cols2 finder
	cols2=row.find_all('a')
	# list combine and space to comma handling
	tmpcols1 = [re.sub(' +', ',', x1.text) for x1 in cols1 if x1.text]
	tmpcols1 = ",".join(str(x4) for x4 in tmpcols1)
	tmpcols1 = tmpcols1.split(',')
	if (len(tmpcols1) != 3):
		continue

	# handling the cols2 and its sub data
	tmpcols2 = [base_url + x2['href'].replace('./','/') for x2 in cols2]

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
		tmpcols2_sub = [x3.text.replace(' ','') for x3 in rows_sub]

	# export final data if cols1 not empty
	if (tmpcols1):
		cols3 = tmpcols1 + tmpcols2_sub + tmpcols2
		data.append(cols3)

	# print(data)

# write data list into csv
try:
	output_filename = sys.argv[2]
except:
	output_filename = 'output.csv'

with open(output_filename, 'w', newline='') as csvfile:
	writer = csv.writer(csvfile)
	writer.writerows(data)
