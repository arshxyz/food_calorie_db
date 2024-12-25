import json
import os

with open('myfoods.json', 'r') as file:
    data = json.load(file)

clean_foods = []
keep_keys = ['calorie', 'carbs', 'fats', 'fibre', 'proteins', 'food_name', 'measures', 'other_names']

for food_id in data:
    food = data[food_id]
    for m in food['measures']:
        del m['id']
    clean_foods.append({key: food[key] for key in keep_keys})

with open('food_macros_dataset.clean.json', 'w+') as f:
    f.write(json.dumps(clean_foods, indent=4))

os.system("zip -r food_macros_dataset.clean.json.zip food_macros_dataset.clean.json")