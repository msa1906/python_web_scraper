import csv
import re
import os

name = '2017-01-01,2017-01-31_filted'


def ensureUtf(s):
  try:
      if type(s) == unicode:
        return s.encode('utf8', 'ignore')
  except: 
    return str(s)


directory = r'C:\Users\Logan\Desktop\python_web_scraper\company_company\filted-data\filted'
film = {}

for filename in os.listdir(directory):
	if filename.endswith(".csv"):
		print(filename)
		spamReader = csv.reader(open(filename, newline=''))
		for row in spamReader:
			if len(row) > 5:
				#more than one company
				for i in range(4, len(row) ):
					for j in range(i, len(row) ):
						if row[i] not in film:
							film[row[i]] = len(film)
						if row[j] not in film:
							film[row[j]] = len(film)


		Matrix = [[0 for x in range(len(film))] for y in range(len(film))] 

		spamReader = csv.reader(open(filename, newline=''))					
		for row in spamReader:
			if len(row) > 5:
				#more than one company
				for i in range(4, len(row) ):
					for j in range(i + 1, len(row) ):
						Matrix[film[row[i]]][film[row[j]]]+= 1
						Matrix[film[row[j]]][film[row[i]]]+= 1
						print('com1' + row[i] + 'coom2' + row[j]+'counter' + str(Matrix[film[row[i]]][film[row[j]]]))
						
		print(Matrix)
		continue
	else:
		continue
with open('2017'+'.csv', 'a', newline='') as csvfile:
	spamwriter = csv.writer(csvfile)
	list1 = ['']
	list1.extend(film)
	list1 = list(map(lambda x:ensureUtf(x), list1))
	spamwriter.writerow(list1)
	
	for (k, v) in film.items():
		list1 = [k]
		list1.extend(Matrix[v])
			
		list1 = list(map(lambda x:ensureUtf(x), list1))
		spamwriter.writerow(list1)