import requests
import re
from bs4 import BeautifulSoup
import csv
from datetime import datetime
import math
import socket  
import time  

from lxml import html
from requests.packages.urllib3 import add_stderr_logger
import urllib
from urllib.error import HTTPError
from urllib.request import urlopen
import re, random, datetime
random.seed(datetime.datetime.now())

add_stderr_logger()
login_page = requests.get('http://58921.com/user/login')
login_soup = BeautifulSoup(login_page.text, 'html.parser')
token = login_soup.select('input[name="form_token"]')[0]['value']


session = requests.Session()
login_url = 'http://58921.com/user/login'
session_requests = requests.session()
result = session_requests.get(login_url)

login_soup = BeautifulSoup(result.text, 'html.parser')
token = login_soup.select('input[name="form_token"]')[0]['value']
payload = {
	"mail": "shenmizhe1906@gmail.com", 
	"pass": "19061906a", 
	"form_id": "user_login_form",
	"form_token": token
}
authenticity_token = token
login_url = 'http://58921.com/user/login/ajax?ajax=submit&__q=user/login'

result = session_requests.post(
	login_url, 
	data = payload, 
	headers = dict(referer=login_url)
)

url = 'http://58921.com/user/center'
result = session_requests.get(
	url, 
	headers = dict(referer = url)
)


socket.setdefaulttimeout(20)
url = 'http://58921.com/alltime/2017?page='

page_num = 0

page = session_requests.get(url + str(page_num))

if page.status_code == '200':
	print('return 200')
	
soup = BeautifulSoup(page.text, 'html.parser')

count_text = soup.select('li.pager_count span.pager_number')[0].get_text()
count_groups = re.search('\d+\/(\d+)', count_text)
count = int(count_groups.group(1))
	

	
	
def ensureUtf(s):
  try:
      if type(s) == unicode:
        return s.encode('utf8', 'ignore')
  except: 
    return str(s)
	
def movie_data(movie):
	id = re.search('\d+', movie['href']).group(0)
	print('movie id' + str(id))
	name = movie.get_text()
	titleWeb = 'http://58921.com/film/'
	while 1:
		try:
			movie_page =  session_requests.get(titleWeb+ id)
		except:
			continue
		break
	
	moviesoup = BeautifulSoup(movie_page.text, 'html.parser')
	dirctor = moviesoup.select('ul.dl-horizontal li:nth-of-type(2) a')
	area = moviesoup.select('ul.dl-horizontal li:nth-of-type(6) a')
	try:
		if not (re.match('\/tag\/film\/36',area[0]['href'])):
			print('not in china')
			with open('not_china'+'.csv', 'a', newline='', encoding='utf-8') as csvfile:
				spamwriter = csv.writer(csvfile)
				list1 = [int(id)]
				list1 = list(map(lambda x:ensureUtf(x), list1))
				spamwriter.writerow(list1)
			return
	except: 
		print('exception in find china')
		with open('not_china'+'.csv', 'a', newline='', encoding='utf-8') as csvfile:
				spamwriter = csv.writer(csvfile)
				list1 = [int(id)]
				list1 = list(map(lambda x:ensureUtf(x), list1))
				spamwriter.writerow(list1)
		return
	try:
		dirctor_id = dirctor[0]['href']
		dirctor_id = re.search('\d+', dirctor_id).group(0)
		
		stars = moviesoup.select('ul.dl-horizontal li:nth-of-type(3) a')
		print('find dirctor')
		with open('director'+'.csv', 'a', newline='', encoding='utf-8') as csvfile:
			spamwriter = csv.writer(csvfile)
			list1 = [int(id), int(dirctor_id)]
			list1 = list(map(lambda x:ensureUtf(x), list1))
			spamwriter.writerow(list1)
			
		for star in range(len(stars)):
			star = stars[star]
			star_id = re.search('\d+', star['href']).group(0)
			with open('stars'+'.csv', 'a', newline='', encoding='utf-8') as csvfile:
				spamwriter = csv.writer(csvfile)
				list1 = [int(id), int(star_id)]
				list1 = list(map(lambda x:ensureUtf(x), list1))
				spamwriter.writerow(list1)
	except:
		with open('error'+'.csv', 'a', newline='', encoding='utf-8') as csvfile:
				spamwriter = csv.writer(csvfile)
				list1 = [int(id)]
				list1 = list(map(lambda x:ensureUtf(x), list1))
				spamwriter.writerow(list1)
				

for page_num in range(0, count+1) :
	print('page'+str(page_num))
	while 1:
		try:
			page = session_requests.get(url + str(page_num))
		except:
			continue
		break		
	soup = BeautifulSoup(page.text, 'html.parser')
		
	movies = soup.select("td a")
	for movie in movies:
		if re.match('\/film\/\d+',movie['href']):
			movie_data( movie )