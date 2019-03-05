import csv

def makeCSV_from_flat_list(fileName, my_list):
	print('\ncreating a csv named', fileName, 'from list:', my_list, '\n')
	with open(fileName, "w") as output:
		writer = csv.writer(output, lineterminator='\n')
		for val in my_list:
			writer.writerow([val])

def makeCSV_from_list_of_lists(fileName, my_list):
	print('\ncreating a csv named', fileName, 'from list:', my_list, '\n')
	with open(fileName, "w") as output:
		writer = csv.writer(output, lineterminator='\n')
		writer.writerows(my_list)

def appendCSV_from_flat_list(fileName, item):
	print('\nappending the csv named', fileName, 'with item:', item)
	with open(fileName, "a") as output:
		writer = csv.writer(output, lineterminator='\n')
		writer.writerow([item])

def appendCSV_from_list_of_lists(fileName, my_list):
	print('\ncreating a csv named', fileName, 'from list:', my_list, '\n')
	with open(fileName, "a") as output:
		writer = csv.writer(output, lineterminator='\n')
		writer.writerows(my_list)

def getFromCSV(fileName):
	with open(fileName, 'r') as f:
		reader = csv.reader(f)
		data = list(reader)
	return data

'''
def getFromCSV_ISO(fileName):
	with open(fileName, 'r', encoding = "ISO-8859-1") as f:
		reader = csv.reader(f)
		data = list(reader)
	return data
'''
def getFromCSV_UTF16(fileName):
	with open(fileName, 'r', encoding='utf-16') as f:
		reader = csv.reader(f)
		data = list(reader)
	return data



