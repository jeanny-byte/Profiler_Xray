import requests
from bs4 import BeautifulSoup
link = "https://recruitmentgeek.com/tools/linkedin#gsc.tab=0&gsc.q=%22william%20shakesspere%22%20AND%20%22tea%22&gsc.sort="

header = { "header":'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.5112.79 Safari/537.36'}
data = requests.get(link)
soup = BeautifulSoup(data.text, "html.parser")
first_data = soup.findAll('a')
print(first_data)
# web_data = soup.findAll('div', class_='gs-bidi-start-align gs-visibleUrl gs-visibleUrl-long')
# for div in web_data:
#     print(div.text)

# first_result = soup.findall('div', class_="gs-bidi-start-align gs-visibleUrl gs-visibleUrl-long")
# print (first_result)



