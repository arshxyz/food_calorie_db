import requests
import time
import json

url = "https://api.x.com/api/v1/fooddbdiff/updateAndroid/"

db_version = 0

headers = {
    'Authorization': ''
}

with open('responses.json', 'w') as f:
    f.write('[')

foods = {}
measures = []
curr_food_len = 0
def writefile(data, filename):
    with open(filename, 'w+') as f:
        f.write(json.dumps(data, indent=4))


while True:
    params = {
        'format': 'json',
        'db_version': db_version,
        'approx_limit': 50000
    }
    
    try:
        response = requests.get(url, params=params, headers=headers)
        
        response.raise_for_status()
        
        data = response.json()
        
        
        for food in data['changes']['foods']:
            curr_food_len += 1
            # print(food)
            if (food['food_id'] in foods):
                foods[food['food_id']]['other_names'].append(food['food_name'])
            else:
                foods[food['food_id']] = food
                foods[food['food_id']]['measures'] = []
                foods[food['food_id']]['other_names'] = []

        measures += (data['changes']['food_measures'])

        new_db_version = data.get('new_db_version')
        
        remaining_food_measures = data.get('remaining_food_measures', 0)
        remaining_food_names = data.get('remaining_food_names', 0)
        
        print(f"remaining foods: {remaining_food_names}")
        print(f"remaining measures: {remaining_food_measures}")

        print(f"curr foods: {curr_food_len}")
        print(f"TOTAL: {curr_food_len + remaining_food_names}")

        if remaining_food_measures == 0 and remaining_food_names == 0:
            print("Both remaining_food_measures and remaining_food_names are 0. Stopping.")
            break
        
        # Update db_version for the next iteration
        db_version = new_db_version
        
        time.sleep(1)

    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        break

# apply measures
print("Applying measures")
for measure in measures:
        mfood_id = measure['food_id']
        if mfood_id not in foods:
            print(f"{mfood_id} not in DB. Something wrong.")
        else:
            del measure['food_id']
            foods[mfood_id]['measures'].append(measure)

print("Writing to file")
writefile(foods, "myfoods.json")


print("Data has been saved to 'myfoods.json'.")
