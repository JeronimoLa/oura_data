import csv, json, requests, time

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
		with open('docs/csv/sandbox_daily_cardiovascular_age.csv') as csv_file:
			rows = list(map(lambda x: tuple(x.strip("\n").split(",")), csv_file.readlines()))
			last_row = rows[-1][0]
			year, month, day = list(map(int, last_row.split("-")))
			date_obj = date(year, month, day)
			date_to_collect_from = date_obj + timedelta(1)

	except IndexError:
		date_to_collect_from = OURA_FIRST_DAY

	res = wrapper("GET", f"/v2/usercollection/daily_cardiovascular_age?start_date={date_to_collect_from}")
	# res = wrapper("GET", f"/v2/sandbox/usercollection/daily_cardiovascular_age?start_date=2022-01-25")

	header = ["day", "vascular_age"]
	write_csv_from_dicts(res["data"], header, "docs/csv/sandbox_daily_cardiovascular_age.csv")

def daily_sleep():
	res = wrapper("GET", f"/v2/usercollection/daily_activity?start_date={OURA_FIRST_DAY}")
	# print(res["data"][0].keys())
	header = ['id', 'class_5_min', 'score', 'active_calories', 'average_met_minutes', 'contributors', 'equivalent_walking_distance', 'high_activity_met_minutes', 'high_activity_time', 'inactivity_alerts', 'low_activity_met_minutes', 'low_activity_time', 'medium_activity_met_minutes', 'medium_activity_time', 'met', 'meters_to_target', 'non_wear_time', 'resting_time', 'sedentary_met_minutes', 'sedentary_time', 'steps', 'target_calories', 'target_meters', 'total_calories', 'day', 'timestamp']
	# print(json.dumps(res["data"], indent=4))
	write_csv_from_dicts(res["data"], header, "docs/csv/daily_activity.csv")
	# header = ["id", "contributors", "day", "score", "timestamp"]
	# write_csv_from_dicts(res["data"], header, "docs/csv/sleep_data.csv")


def main():
	# daily_cardiovascular_age()
	daily_sleep()

if __name__ == "__main__":
	main()
