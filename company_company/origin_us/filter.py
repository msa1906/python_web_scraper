import csv
import re
import requests

from bs4 import BeautifulSoup


from datetime import datetime
import math
import socket  
import time  
year_list = ['2017-01-01,2017-01-31','2017-02-02,2017-02-28','2017-03-01,2017-03-31','2017-04-01,2017-04-30','2017-05-01,2017-05-31','2017-06-01,2017-06-30','2017-07-01,2017-07-31','2017-08-01,2017-08-31','2017-09-01,2017-09-30','2017-10-01,2017-10-31','2017-11-01,2017-11-30','2017-12-01,2017-12-31']


	
def ensureUtf(s):
  try:
      if type(s) == unicode:
        return s.encode('utf8', 'ignore')
  except: 
    return str(s)
def filt_file(name):
	spamReader = csv.reader(open(name + '.csv', newline=''))
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
		
		if re.match('^' + name[:7], row[2]):
		
		
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

for name in year_list:
	filt_file(name)