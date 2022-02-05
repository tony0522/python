import csv
import requests
from bs4 import BeautifulSoup

# global variables
base_url = "https://www.cac.edu.tw/star111/system/0ColQry_for111star_5f9g8t4q/html/111_00808.htm?v=1.0"
uni_url = base_url + "/SGroup3.htm"
headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.80 Safari/537.36'}

# init environment setting 
requests.adapters.DEFAULT_RETRIES = 1
s = requests.session()
s.keep_alive = False

# make the request connection
response = requests.get(uni_url, headers=headers)
soup = BeautifulSoup(response.content, "html.parser")

# rows = soup.find_all([style="border-bottom-style:none", style="border-top-style:none ;border-bottom-style:none"])
rows = soup.find_all(
    style=["border-bottom-style:none", "border-top-style:none ;border-bottom-style:none"]
    )

tmpcols = [x.text.replace(' ','') for x in rows]

print(tmpcols)
# # write data list into csv
# with open('output-sub.csv', 'w', newline='') as csvfile:
# 	writer = csv.writer(csvfile)
# 	writer.writerow(tmpcols)
