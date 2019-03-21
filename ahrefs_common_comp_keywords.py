import os
import CSV_actions
cwd  = os.getcwd()
#download the ahrefs competitor kewyords as UTF-16, and place them in this folder:
path = os.path.join(cwd, "competitor_keywords")
print(path)
#download the ahrefs client kewyords as UTF-16, and place them in this folder:
path_2 = os.path.join(cwd, "client_keywords")
print(path_2)
# get headers from first file
#first_file = os.listdir(path)[0]
#first_file_data = CSV_actions.getFromCSV(path+'/'+first_file)
#headers = first_file_data[0]
#print(headers)

#Change this as needed. Filters rows with volume less than integer
volume_filter = 200
ranking_filter = 10

def parse_ahrefs_data(data):
	new_data = []
	for row in data:
		new_row = []
		old_row = row[0].split('\t')
		for item in old_row:
			item = item.strip('\"')
			new_row.append(item)
		new_data.append(new_row)
	return new_data

def count_kw_competitors_UNIQUE(kw_list):
	new_list = []
	global ranking_filter
	print('\n\ncounting how many competitors ranking for each keyword in resulting list\n\n')
	index = 0
	for row in kw_list:
		new_list.append(row)
	for row in new_list:
		#if index == 0:
		#	heading = "Count of Competitors Ranking in Top " + str(ranking_filter)
		#	row.append(heading)
		#	index = index+1
		#	continue
		keyword = row[1]
		print(keyword)
		competitors_ranking = []
		for row_ in new_list:
			if row_[1] == keyword:
				print(row_[1], keyword)
				competitor = row_[0]
				if competitor not in competitors_ranking:
					competitors_ranking.append(competitor)
		row.append(len(competitors_ranking))
		index = index+1
	return new_list

def delete_cols(arry, cols, row_len):
	for row in arry:
		print(row)
		print(len(row))
		index = 0
		if len(row) == row_len:
			for item in cols:
				item = item - index
				index = index + 1
				del row[item]
	return arry


#get client kws
source_data_CLIENT = []
client_kws = os.listdir(path_2)
for file in client_kws:
	if file.endswith(".csv"):
		client_kws = file
client_kws = CSV_actions.getFromCSV_UTF16(path_2+'/'+client_kws)
parsed_client_kws = parse_ahrefs_data(client_kws)

client_ranking_terms = []
client_ranking_terms_lookup = []
for row in parsed_client_kws:
	if len(row) == 13:
		kw = row[1]
		pos = row[2]
		client_ranking_terms.append(kw)
		client_ranking_terms_lookup.append([kw,pos])
print("client ranking terms length is:")
print(len(client_ranking_terms))
source_data_COMP = []
for file in os.listdir(path):
	if not file.startswith('.'):
		file_rows = CSV_actions.getFromCSV_UTF16(path+'/'+file)
		competitor = file[:file.find('-organic-')]
		for row in file_rows:
			print(row)
			if row[0][:row[0].find('\t')] != "#":
				row[0] = competitor+row[0][row[0].find("\t"):] #finds whatever is prior to first tab, replaces with competitor name
			source_data_COMP.append(row)

parsed_competitor_terms = parse_ahrefs_data(source_data_COMP)
print("parsed comp terms is", len(parsed_competitor_terms), "long.")
#print(parsed_competitor_terms)

filtered_comp_data_CLIENT_ALSO_RANKS = []
filtered_comp_data_CLIENT_DOES_NOT_RANK = []


#CSV_actions.makeCSV_from_list_of_lists('new_list0.csv', new_data)

#filter through competitor keywords based on volume, KD, etc.
#...and check if keyword is in client KW rankings
#...sep into list of client ranking also and client not ranking
#...to be used for further research

#index = 1
for row in parsed_competitor_terms:
	#if index == 1:
	#	headers = row
	if len(row) == 13:
		if row[0] != "#":
			if int(row[5]) >= volume_filter:
				#filter out 'page url inside' results:
				if len(row[11]) == 0:
					#filter out pages ranking deep:
					if int(row[2]) < ranking_filter:
						#filter out high KD:
						if int(row[7]) < 30:
							#separate into two lists based on whether client ranks for the kw
							if row[1] in client_ranking_terms:
								print(row)
								filtered_comp_data_CLIENT_ALSO_RANKS.append(row)
							else:
								filtered_comp_data_CLIENT_DOES_NOT_RANK.append(row)
	#index = index+1
#headers[0] = "Competitor"
#filtered_comp_data_CLIENT_ALSO_RANKS.insert(0, headers)
#filtered_comp_data_CLIENT_DOES_NOT_RANK.insert(0, headers)

filtered_comp_data_CLIENT_ALSO_RANKS = count_kw_competitors_UNIQUE(filtered_comp_data_CLIENT_ALSO_RANKS)
#this next thing may take a very long time...
filtered_comp_data_CLIENT_DOES_NOT_RANK = count_kw_competitors_UNIQUE(filtered_comp_data_CLIENT_DOES_NOT_RANK)

#headers = ['Competitor', 'Keyword',	'Position',	'MSV',	'URL', 'KD', 'Traff (desc)', 'CPC', 'Count of Comp in Top '+str(ranking_filter)]

delcols = [3,4,10,11,12]
filtered_comp_data_CLIENT_ALSO_RANKS = delete_cols(filtered_comp_data_CLIENT_ALSO_RANKS,delcols,14)
filtered_comp_data_CLIENT_DOES_NOT_RANK = delete_cols(filtered_comp_data_CLIENT_DOES_NOT_RANK,delcols,14)

#filtered_comp_data_CLIENT_ALSO_RANKS[0] = headers
#filtered_comp_data_CLIENT_DOES_NOT_RANK[0] = headers

#find client rank to compare to comps in client also ranks...
for row in filtered_comp_data_CLIENT_ALSO_RANKS:
	keyword = row[1]
	#TODO uncomment print(keyword)
	if keyword in client_ranking_terms:
		for term in client_ranking_terms_lookup:
			if term[0] == keyword:
				row.append(term[1])
				break

#column headers


filtered_comp_data_CLIENT_ALSO_RANKS.insert(0,['Competitor','Keyword','Position','MSV','URL','KD','Traff (desc)','CPC','Count of Comp in Top '+str(ranking_filter),"Client Rank"])
filtered_comp_data_CLIENT_DOES_NOT_RANK.insert(0,['Competitor','Keyword','Position','MSV','URL','KD','Traff (desc)','CPC','Count of Comp in Top '+str(ranking_filter)])


CSV_actions.makeCSV_from_list_of_lists('comp_kws_client_also_ranks.csv', filtered_comp_data_CLIENT_ALSO_RANKS)
CSV_actions.makeCSV_from_list_of_lists('comp_kws_client_does_not_rank.csv', filtered_comp_data_CLIENT_DOES_NOT_RANK)



