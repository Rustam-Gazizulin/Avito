import csv
import json

def convert_to_json(csv_file, json_file, model_name):
    mydata = []

    with open(csv_file, encoding='utf-8') as csvfile:
        for row in csv.DictReader(csvfile):
            to_add = {'model': model_name, 'pk': int(row['Id'] if 'Id' in row else row['id'])}

            if 'Id' in row:
                del row['Id']
                print(to_add)
            else:
                del row['id']
            if 'price' in row:
                row['price'] = int(row['price'])
            if "is_published" in row:
                if row["is_published"] == 'TRUE':
                    row["is_published"] = True
                else:
                    row["is_published"] = False


            to_add['fields'] = row
            mydata.append(to_add)

    with open(json_file, 'w', encoding='utf-8') as jsonfile:
        jsonfile.write(json.dumps(mydata, ensure_ascii=False))


ads_csv = r'ads.csv'
ads_json = r'ads.json'
model = 'ads.ads'
model_cat = 'ads.category'
categories_csv = r'categories.csv'
categories_json = r'categories.json'

convert_to_json(ads_csv, ads_json, model)
convert_to_json(categories_csv, categories_json, model_cat)
