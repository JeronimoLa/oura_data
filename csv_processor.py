import ast, csv, time, json

def tool():
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

tool()
