import csv

def read_and_parse_city_file():

	city_list = []
	with open('city_list.txt', 'r') as file:
		read_csv = csv.reader(file)
		for line in read_csv:
			city_state_pair = []
			city_state_pair.append(line[1])
			city_state_pair.append(line[2])
			city_list.append(city_state_pair)

	return city_list


