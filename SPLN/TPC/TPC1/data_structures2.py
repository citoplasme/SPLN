#!/usr/bin/python3

import csv

def media(lst): 
    return sum(lst) / len(lst) 

dic = {}
with open('../../Data/candies.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    line_count = 0
    for row in csv_reader:
        if line_count == 0:
        	print(row[0] + ' ' + row[1])
        else:
        	year,month,date = row[0].split('-')
        	if month in dic: 
        		dic[month].append((int(year), float(row[1])))
        	else:
        		dic[month] = [(int(year), float(row[1]))]
        line_count += 1
    print(f'Processed {line_count} lines.')
print(dic)

for key in dic: 
	print('Month: ' + key +  ' Mean: ' + str(media(dic[key][1])))
