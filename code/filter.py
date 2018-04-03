import csv
import re
import requests

from bs4 import BeautifulSoup


from datetime import datetime
import math
import socket  
import time  

name = '2017-12-01,2017-12-31'

spamReader = csv.reader(open(name + '.csv', newline=''))
	
def ensureUtf(s):
  try:
      if type(s) == unicode:
        return s.encode('utf8', 'ignore')
  except: 
    return str(s)
	
for row in spamReader:
	id = int(row[0])
	date = row[2]
	flag = False
	if date == 'unknow':
		print('unknow' + str(id))
		while 1:
			try:
				print('try get page id' + str(id))	
				titleWeb = 'http://www.imdb.com/title/tt'
				movie_page =  requests.get(titleWeb+ str(id))
			except:
				continue
			break
		
		moviesoup = BeautifulSoup(movie_page.text, 'html.parser')
		release_date = 'unknow'
		try:
			release_date = moviesoup.select('div.subtext a[title="See more release dates"] meta')
			release_date = re.search('(19|20)\d\d[- /.](0[1-9]|1[012])',release_date[0]['content']).group(0)
			print(release_date)
			row[2] = release_date
		except:
			try: 
				
				release_date = re.search('(19|20)\d\d',release_date[0]['content']).group(0)
				print(release_date)
				row[2] = release_date
			except:
				
				print('error in date finder')
				row[2] = 'unknow'
				pass
	
	if re.match('^2017-12', row[2]):
	
	
		with open(name+'_filted'+'.csv', 'a', newline='') as csvfile:
			spamwriter = csv.writer(csvfile)
			list1 = row
			list1 = list(map(lambda x:ensureUtf(x), list1))
			#print(list1)
			spamwriter.writerow(list1)
	elif re.match('^2017',row[2]):
		with open(name+'_2017_only'+'.csv', 'a', newline='') as csvfile:
			spamwriter = csv.writer(csvfile)
			list1 = row
			list1 = list(map(lambda x:ensureUtf(x), list1))
			#print(list1)
			spamwriter.writerow(list1)