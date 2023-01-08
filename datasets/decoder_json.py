import csv
import json

def convert_to_json(ads_csv, ads_json):
    mydata = {}

    with open(ads_csv, encoding='utf-8') as csvfile:

        csvRead = csv.DictReader(csvfile)
        print(csvRead)

        for rows in csvRead:
            mykey = rows['id']
            mydata[mykey] = rows
            print(rows)

    with open(ads_json, 'w', encoding='utf-8') as jsonfile:
        jsonfile.write(json.dumps(mydata, indent=4, ensure_ascii=False))


ads_csv = r'ads.csv'
ads_json = r'ads.json'
categories_csv = r'categories.csv'
categories_json = r'categories.json'
convert_to_json(categories_csv, categories_json)