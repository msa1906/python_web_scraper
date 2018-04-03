import requests
import re
from bs4 import BeautifulSoup
import csv
from datetime import datetime
import math
import socket  
import time  
  
socket.setdefaulttimeout(20)
url = 'http://www.imdb.com/search/title?title_type=feature&release_date='
year = '2017-05-01,2017-05-31'

page_num = 1

page = requests.get(url + year +'&count=250&page=' + str(page_num))

if page.status_code == '200':
	print('return 200')
	
soup = BeautifulSoup(page.text, 'html.parser')

count_text = soup.select('div.nav div.desc')[0].get_text()
count_groups = re.search('(\d+) titles', count_text)
count = math.ceil(int(count_groups.group(1)) / 250)

if count > 10000: 
	print('too many result')
	exit()

	
def ensureUtf(s):
  try:
      if type(s) == unicode:
        return s.encode('utf8', 'ignore')
  except: 
    return str(s)
	
def movie_data(movie):
	id = re.search('\d+', movie['href']).group(0)
	
	name = movie.get_text()
	titleWeb = 'http://www.imdb.com/title/tt'
	movie_page =  requests.get(titleWeb+ id)
	print(name)
	print(id)
	
	moviesoup = BeautifulSoup(movie_page.text, 'html.parser')
	release_date = 'unknow'
	try:
		release_date = moviesoup.select('div.subtext a[title="See more release dates"] meta')
		release_date = re.search('(19|20)\d\d[- /.](0[1-9]|1[012])[- /.](0[1-9]|[12][0-9]|3[01])',release_date[0]['content']).group(0)
		print(release_date)
		
	except :
		release_date = 'unknow'
		pass
	while 1:
		try:
		
			company_page = requests.get('http://www.imdb.com/title/tt'  +id+'/companycredits')
		except:
			continue
		break
	
	
	companySoup = BeautifulSoup(company_page.text, 'html.parser')
	companys = companySoup.select('#production + ul.simpleList a')
	companys = list(map(lambda x: x.text, companys))
			
	print(companys)
	with open(year+'.csv', 'a', newline='', encoding='utf-8') as csvfile:
		spamwriter = csv.writer(csvfile)
		list1 = [id, name, release_date, datetime.now()]
		list1.extend(companys)
		list1 = list(map(lambda x:ensureUtf(x), list1))
		print(list1)
		spamwriter.writerow(list1)
for page_num in range(1, count+1) :
	while 1:
		try:
			page = requests.get(url + year +'&count=250&page=' + str(page_num))
		except:
			continue
		break
	
	soup = BeautifulSoup(page.text, 'html.parser')
		

	movies = soup.select("h3.lister-item-header a")
	for movie in movies:
		movie_data(movie)