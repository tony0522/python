import requests
from bs4 import BeautifulSoup

uni_url = "https://www.cac.edu.tw/star111/system/0ColQry_for111star_5f9g8t4q/SGroup3.htm"
headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.80 Safari/537.36'}

requests.adapters.DEFAULT_RETRIES = 1
s = requests.session()
s.keep_alive = False

response = requests.get(uni_url, headers=headers)
soup = BeautifulSoup(response.content, "html.parser")

titles = soup.find_all(title="校系名稱及代碼")

for title in titles: 
    title = str(title)
    title = title.replace('<br/>', '')
    title = title.replace('<font color="#FF0000">', '')
    title = title.replace('  ', '')
    title = title.replace('<td title="校系名稱及代碼"><b>', '')
    title = title.replace('</font></b></td>', '')
    print(title)

# print(Title1.prettify())
# print(soup.prettify())
