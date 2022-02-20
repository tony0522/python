import re, csv, sys, requests
from bs4 import BeautifulSoup

# global variables
base_url = "https://www.cac.edu.tw/star111/system/0ColQry_for111star_5f9g8t4q"
headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.80 Safari/537.36'}

try:
	# need more check for sys.arv by package
	uni_url = base_url + "/SGroup" + sys.argv[1] + ".htm"
except:
	uni_url = base_url + "/SGroup8.htm"

# init environment setting 
requests.adapters.DEFAULT_RETRIES = 1
s = requests.session()
s.keep_alive = False

# make the request connection
response = requests.get(uni_url, headers=headers)

if (response.status_code == 200):
	soup = BeautifulSoup(response.content, "html.parser")

	tables = soup.findChildren('table')
	my_table = tables[0]
	rows = my_table.findChildren(['tr'])

	# init data list
	data = []
	data.append(['學校名稱','校系名稱','校系代碼',
		'國文','國文','英文','英文','數學A','數學A',
		'數學B','數學B','社會','社會','自然','自然','英聽','英聽',
		'詳細資料'
		]
	)

	# get the master grid
	for row in rows:
		# cols1 finder
		cols1=row.find_all(title="校系名稱及代碼")
		# list combine and space to comma handling
		tmpcols1 = [re.sub(' +', ',', x1.text) for x1 in cols1 if x1.text]
		tmpcols1 = ",".join(str(x4) for x4 in tmpcols1)
		tmpcols1 = tmpcols1.split(',')
		if (len(tmpcols1) != 3):
			continue

		# cols2 finder, find all hyperlink
		cols2=row.find_all('a')
		# handling the cols2 and its sub data
		tmpcols2 = [base_url + x2['href'].replace('./','/') for x2 in cols2]

		# get the detail grid
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


	# final the list, remove uselses
	removeIndex = [3,5,7,9,11,13,15] # The indices you want to remove
	for l in data:
		for index,value in enumerate(removeIndex):
			# Because after pop, the list index will minor 1
			l.pop(value-index)

	# write data list into csv
	try:
		output_filename = sys.argv[2]
	except:
		output_filename = 'output.csv'

	with open(output_filename, 'w', newline='') as csvfile:
		writer = csv.writer(csvfile)
		writer.writerows(data)

	print("prcoess done!!")

else:
	print("website or pages not found or error, quit!!")
