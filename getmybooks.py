import requests
from bs4 import BeautifulSoup
import os.path
import datetime

homepage = 'http://books.goalkicker.com/'

use_proxy = False

http_proxy  = "http://10.10.1.10:3128"
https_proxy = "https://10.10.1.11:1080"
ftp_proxy   = "ftp://10.10.1.10:3128"

r = requests.get(url, headers=headers, proxies=proxyDict)

if use_proxy is True:
	proxyDict = { 
				"http"  : http_proxy, 
				"https" : https_proxy, 
				"ftp"   : ftp_proxy
				}
else:
	proxyDict = {}

today = datetime.date.today()
today_iso = today.isocalendar()
save_path = str(today_iso[0]) + str(today_iso[1]) + '/'

with requests.session() as s:

	home = s.get(homepage, proxies=proxyDict)
	bowl = BeautifulSoup(home.content, 'html.parser')

	# get the URLS for each book subpage from the homepage

	book_urls = []

	for books in bowl.find_all('div', {'class': 'bookContainer grow'}):
		deepsearch = books.find_all('a')

		for i in deepsearch:

			book_url = homepage + i['href']
			book_urls.append(book_url)

	# get book download link from each subpage and download it

	for book_front in book_urls:

		book_site = s.get(book_front, proxies=proxyDict)
		book_code = BeautifulSoup(book_site.content, 'html.parser')

		for dummy in book_code.find_all('div', {'id': 'frontpage'}):
			link_elem = dummy.findAll('a')

			for link in link_elem:

				download_payload = book_front + '/' + link['href']

				if('.pdf' in download_payload):
					download_link = download_payload

					print('Downloading ' + link['href'] + ' ...')
					file = s.get(download_link, proxies=proxyDict)

					if os.path.isdir(save_path) is False:
							os.mkdir(save_path)
					with open(save_path + link['href'], 'wb') as f:
						f.write(file.content)