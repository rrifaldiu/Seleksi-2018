from urllib.request import urlopen
from bs4 import BeautifulSoup
from time import sleep
import json

#url
url = 'https://www.tripadvisor.com/Hotel_Review-g297704-d505226-Reviews-Padma_Hotel_Bandung-Bandung_West_Java_Java.html'
page = urlopen(url).read()

#small picture scraper
def scrape_small_picture(url):
	result = []
	page = urlopen(url).read()
	soup = BeautifulSoup(page, 'html.parser')

	# get name
	name = soup.find(class_="header heading masthead masthead_h1 ").get_text()
	result.append(name)

	# get address
	address = soup.find(class_="street-address").get_text()
	result.append(address)
	return result

# res = scrape_small_picture(url)
# print("test")
# print(res)
# print("test2")

def scrape_big_picture(url):

	#initialization
	result = []
	page = urlopen(url).read()
	soup = BeautifulSoup(page, 'html.parser')

	# iterate each page of list of hotels
	list_hotel_attr = list(set(soup.find_all(target="_blank")))
	for hotel_attr in soup.find_all(target="_blank"):
		
		#get hotel page
		hotel_page = 'https://www.tripadvisor.com/' + hotel_attr.get('href')
		
		# call small picture scraper
		func_res = scrape_small_picture(hotel_page)
		print(func_res)

		#join the scraper
		result.append(func_res)
		sleep(0.1)
		# print(urls)
	return result

	# for urlz in soup.find_all(target="_blank"):
	# 	print(urlz.get('href'))
	# # print(urls)
	# return result

def scrape_iterator(url):
	#initialization
	result = []
	page = urlopen(url).read()
	soup = BeautifulSoup(page, 'html.parser')

	#iterate each page of list of hotels
	for page in range(1,2):
		if (page == 1):
			hotel_list_url = 'https://www.tripadvisor.com/Hotels-g297704-Bandung_West_Java_Java-Hotels.html'
		else:
			hotel_list_url = 'https://www.tripadvisor.com/Hotels-g297704-oa'+ str((page-1) * 30) + '-Bandung_West_Java_Java-Hotels.html'
		func_res = scrape_big_picture(hotel_list_url)
		result.extend(func_res)
		sleep(0.1)
	return result

result = scrape_iterator('https://www.tripadvisor.com/Hotels-g297704-Bandung_West_Java_Java-Hotels.html')
print(result)

with open('data/data.json', 'w') as outfile:
    json.dump(result, outfile)

print(result)