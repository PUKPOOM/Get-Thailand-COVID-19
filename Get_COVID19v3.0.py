import http.client as httplib
import requests

from datetime import *
import time
import os
import os.path

import csv
import matplotlib.pyplot as plt

## 1) NewConfirmed
## 2) NewRecovered
## 3) NewHospitalized
## 4) NewDeaths
## 5) Confirmed
## 6) Recovered
## 7) Hospitalized
## 8) Deaths

# -----------------------------------------------------------------------------------
#	G E T | D A T A
# -----------------------------------------------------------------------------------
url = 'https://covid19.th-stat.com/api/open/timeline'	# Shared API for Thailand COVID-19 update
start_date = '03_01_2020'
data_list = {}

raw_data = requests.get(url)
data = raw_data.text[167:].split(',')
##print(data)
##print('Type of Data : ', type(data))
##print('Length of Data : ', len(data))

n = int(len(data)/9)
print('Count of Day : ', n)

j = 9
for idx in range(n):
	index = idx * j
	print('Day : ', idx+1)
	##print('idx : {} | Index : {}'.format(idx, index))
	date = data[index].split(':')
	date = date[1].replace('\/','_')
	date = date.replace('"','')

	NewConfirmed	= data[index+1].split(':')
	NewConfirmed 	= int(NewConfirmed[1])
	NewRecovered	= data[index+2].split(':')
	NewRecovered 	= int(NewRecovered[1])
	NewHospitalized	= data[index+3].split(':')
	NewHospitalized 	= int(NewHospitalized[1])
	NewDeaths	= data[index+4].split(':')
	NewDeaths 	= int(NewDeaths[1])

	Confirmed	= data[index+5].split(':')
	Confirmed 	= int(Confirmed[1])
	Recovered	= data[index+6].split(':')
	Recovered 	= int(Recovered[1])
	Hospitalized	= data[index+7].split(':')
	Hospitalized 	= int(Hospitalized[1])
	Deaths	= data[index+8].split(':')
	Deaths = Deaths[1]
	Deaths = Deaths.replace('}','')
	Deaths = Deaths.replace(']','')
	Deaths 	= int(Deaths)

	print('NewConfirmed : {} NewRecovered : {} NewHospitalized : {} NewDeaths : {}'.format(NewConfirmed, NewRecovered, NewHospitalized, NewDeaths))
	print('Confirmed : {} Recovered : {} Hospitalized : {} Deaths : {}'.format(Confirmed, Recovered, Hospitalized, Deaths))
	print()

	data_list.update({date: [('NewConfirmed', NewConfirmed), ('NewRecovered', NewRecovered), ('NewHospitalized', NewHospitalized), ('NewDeaths', NewDeaths),
							('Confirmed', Confirmed), ('Recovered', Recovered), ('Hospitalized', Hospitalized), ('Deaths', Deaths)]})

##print(data_list)
for idx in data_list:
	print('Date : ', idx)
	print('NewConfirmed : ', 	data_list[idx][0][1])
	print('NewRecovered : ', 	data_list[idx][1][1])
	print('NewDeaths : ', 		data_list[idx][3][1])
	print()

# -----------------------------------------------------------------------------------
#	W R I T E | D A T A
# -----------------------------------------------------------------------------------
homepath = os.environ['HOMEPATH']
print('Home path : ', homepath)
folder_path = 'C:' + homepath + '\Desktop'
print('Folder path : ', folder_path)
os.chdir(folder_path)
print()

ymd = datetime.now()
file_date = str(ymd.strftime('%m_%d_%Y'))
filename = 'COVID19_' + file_date + '.csv'
file_exists = os.path.isfile(filename)
with open(filename,'a', newline="") as f:
	fw = csv.writer(f)
	row_list = []
	if not file_exists:
		row_list = ['Thialand', 'Date', 'NewConfirmed', 'NewRecovered', 'NewHospitalized', 'NewDeaths', 'Confirmed', 'Recovered', 'Hospitalized', 'Deaths']
		fw.writerow(row_list)
	row_list.clear()
	index = reversed(sorted(data_list.keys()))
	for idx in index:
		row_list = []
		row_list.append('Thailand')
		row_list.append(idx)
		row_list.append(data_list[idx][0][1])
		row_list.append(data_list[idx][1][1])
		row_list.append(data_list[idx][2][1])
		row_list.append(data_list[idx][3][1])
		row_list.append(data_list[idx][4][1])
		row_list.append(data_list[idx][5][1])
		row_list.append(data_list[idx][6][1])
		row_list.append(data_list[idx][7][1])
		fw.writerow(row_list)

# -----------------------------------------------------------------------------------
#	P L O T | D A T A
# -----------------------------------------------------------------------------------
x = [] ; y1 = [] ; y2 = [] ; y3 = [] ; y4 = []
start = 'FALSE'
for idx in data_list:
	if idx == start_date:
		start = 'TRUE'
		x.append(idx)
		y1.append(data_list[idx][4][1])
		y2.append(data_list[idx][5][1])
		y3.append(data_list[idx][6][1])
		y4.append(data_list[idx][7][1])

	else:
		if start == 'TRUE':
			x.append(idx)
			y1.append(data_list[idx][4][1])
			y2.append(data_list[idx][5][1])
			y3.append(data_list[idx][6][1])
			y4.append(data_list[idx][7][1])

##print(x) ; print(y1) ; print(y2) ; print(y3) ; print(y4)
plt.plot(x, y1, label = 'Confirmed', linestyle='dashed', marker='o', markersize=3)
plt.plot(x, y2, label = 'Recovered', linestyle='dashed', marker='x', markersize=3)
plt.plot(x, y3, label = 'Hospitalized', linestyle='dashed')
plt.plot(x, y4, label = 'Deaths', linestyle='dashed')
plt.xlabel('Date') 		# naming the x axis
plt.ylabel('Count') 		# naming the y axis
plt.title('COVID19 Update {} from {}'.format(file_date, start_date)) 	# giving a title to my graph
plt.legend()
plt.show()
