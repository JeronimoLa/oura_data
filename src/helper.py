
import requests
import ast, json, time, os, csv

from typing import Optional
from src.configuraton import CONFIG

def request(method:str, endpoint:str,
			start_date: Optional[str] = None,
			end_date: Optional[str] = None,
			today_date_range: Optional[dict] = None) -> list:
	# TODO: 
	# 1. Rely on the urllib standard library instead of requests
	# 2. Have the network requests handle exceptions
	base = "https://api.ouraring.com"
	if today_date_range is None:
		params = { 
			'start_date': start_date, 
			'end_date': end_date 
    	}
	else:
		params = today_date_range
	headers = {'Authorization': f'Bearer {CONFIG["token"]}'}
	res = requests.request(method, base+endpoint, headers=headers, params=params).json()
	return res["data"]

def to_html(data:list) -> str:
    html = """
    <style>
        p {
            margin: 0;
            padding: 0;
        }
        table, th, td {
            border:1px solid black;
        }
    </style> """
    html += '<table style="width:100%">\n'

    if isinstance(data, list):
        keys = data[0].keys()
        html += '<tr>\n'
        for key in keys:
            html += f'<th>{key}</th>\n'
        html += '</tr>\n'

        for item in data:
            values = list(item.values())
            html += f"<tr>"
            for i in range(len(values)):
                html += f'<td>{values[i]}</td>'
            html += f'</tr>\n'
        html += '</table>'

    elif isinstance(data, dict):
        pass
    else:
        print(f"Exiting...\nobj of type {type(data)} instead of list or dict")
        sys.exit()
    return html

def recursive_fun(spec:dict, result=None, path=None):
    if isinstance(spec, dict): # sometimes its a list 
        if result == None:
            result = {}
        for key, value in spec.items():
            if isinstance(value, dict):
                result[key] = recursive_fun(value)
            else:
                result[key] = type(value).__name__
    return result

def write_csv_from_dicts(data, header, filename):
    file_exists = os.path.isfile(filename)
    
    with open(filename, 'a' if file_exists else 'w', newline='') as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=header)
        if not file_exists:
            writer.writeheader()
        writer.writerows(data)

def recursive_enchancement(spec:dict, target="name", result=None):
	if isinstance(spec, dict): # sometimes its a list 
		if result == None:
			result = {}
		for key, value in spec.items():
			# if target == key:
				# print(value)
				# yield result =  
				# print(json.dumps(value, indent=4))
			if isinstance(value, dict):
				result[key] = recursive_fun(value)
				
			elif isinstance(value, list):
				for v in value:
					if isinstance(v, dict):
						keys = v.keys()
						for key in keys:
							# print(key)
							value_of_key = v.get(key)
							if isinstance(value_of_key, dict):
								print(type(value_of_key))
								print(value_of_key)
								result[key] = recursive_fun(value_of_key)
						# recursive_fun(v.get(v))
						# result[key] = value

			else:
				result[key] = type(value).__name__			
	return result


def list_files(parent_directory, current_filepath=""):
	# if isinstance(parent_directory, str):
	# 	return [current_filepath]

	# if isinstance(parent_directory, list):
	# 	return parent_directory

	# if isinstance(parent_directory, bool):
	# 	return parent_directory

	file_paths = []
	if isinstance(parent_directory, dict):

		for key in parent_directory.keys():
			new_filepath = current_filepath + "/" + key
			value = parent_directory.get(key, None)
			if value == None:
				file_paths.append(new_filepath)
				
			else: 
				file_paths.extend(list_files(value, new_filepath))
	else:
		file_paths.append(parent_directory)	
	return file_paths


def tool():
    # TODO bring in nested dict/list if they are nested inside a column
    with open("docs/csv/daily_readiness.csv") as f:
        csvReader = csv.DictReader(f) 
        data = list(csvReader)

    full_data = []
    keys_to_remove = set()
    for row in data:
        my_dict = {}
        for key, value in row.items():
            if is_valid_dict_string(value):
                temp_dict = ast.literal_eval(value)
                if isinstance(temp_dict, dict):
                    if key not in keys_to_remove:
                        keys_to_remove.add(key)
                    my_dict.update(temp_dict)

        list(map(lambda x: row.pop(x, None), keys_to_remove))
        temp = row | my_dict
        full_data.append(temp)


    for new_dict in full_data:
        time.sleep(0.2)
        print(json.dumps(new_dict, indent=4))
 
def is_valid_dict_string(s):
    try:
        data = ast.literal_eval(s)
        return True
    except (ValueError, SyntaxError):
        return False


def main():
	with open("docs/json/openapi-1.23.json", "r+") as file:
		data = json.loads(file.read())
		print(data.keys())

	# data = {
    # "Documents": {
    #     "Proposal.docx": None,
    #     "Receipts": {
    #         "January": {
    #             "receipt1.txt": None,
    #             "receipt2.txt": None
    #         	},
	# 			"February": {
	# 				"receipt3.txt": None
	# 				"wtf" : []
	# 			}
    #     	}
    # 	},
	# }
	for file in list_files(data):
		time.sleep(.2)
		print(file)
	tool()

if __name__ == "__main__":
    main()