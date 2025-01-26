import csv, json, requests, time
import datetime

from configuraton import BASE_URL, CONFIG, OURA_FIRST_DAY
from helper import recursive_fun


def wrapper(method:str, endpoint:str, **kwargs): 
	try: 
		kwargs["params"]
	except KeyError:
		pass

	headers = { 'Authorization': f'Bearer {CONFIG["token"]}' }   
	return  requests.request(method, BASE_URL + endpoint, headers=headers).json()

def write_csv_from_dicts(data, header, filename):
	header_found = None
	with open(filename, "r") as csv_file: #
		dict_writer = csv.DictWriter(csv_file, fieldnames=header)
		try:
			reader = csv.reader(csv_file)
			row1 = next(reader)
			print("Headers exist")
			header_found = True
		except:
			header_found = False

	with open(filename, "a") as csv_file:
		dict_writer = csv.DictWriter(csv_file, fieldnames=header)
		if not header_found:
			dict_writer.writeheader()
		for row in data:
			dict_writer.writerow(row) 

def daily_cardiovascular_age():
	from datetime import date, timedelta
	try:
		with open('file2.csv') as csv_file:
			rows = list(map(lambda x: tuple(x.strip("\n").split(",")), csv_file.readlines()))
			last_row = rows[-1][0]
			year, month, day = list(map(int, last_row.split("-")))
			date_obj = date(year, month, day)
			date_to_collect_from = date_obj + timedelta(1)

	except IndexError:
		date_to_collect_from = OURA_FIRST_DAY

	res = wrapper("GET", f"/v2/usercollection/daily_cardiovascular_age?start_date={date_to_collect_from}")
	header = ["day", "vascular_age"]
	write_csv_from_dicts(res["data"], header, "file2.csv")

def main():
	daily_cardiovascular_age()


if __name__ == "__main__":
	main()
