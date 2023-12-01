#Title: CWFrequests
#Purpose: To get the cheapest weed from the cloest four dispensaries
#Version: 2.0
#Date: 30/11/2023
#To Do: 
#   add comments

import os
import json
import requests
from urllib.parse import parse_qs, unquote

def janeRequest(data):
    url = "https://vfm4x0n23a-1.algolianet.com/1/indexes/menu-products-production/query?x-algolia-agent=Algolia%20for%20JavaScript%20(4.14.2)%3B%20Browser"

    headers = {
        "Accept": "*/*",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "en-US,en;q=0.9",
        "Connection": "keep-alive",
        "Content-Length": "166",
        "Host": "vfm4x0n23a-2.algolianet.com",
        "Origin": "https://www.iheartjane.com",
        "Prefer": "safe",
        "Referer": "https://www.iheartjane.com/",
        "content-type": "application/x-www-form-urlencoded",
        "sec-ch-ua": '"""Microsoft Edge";v="119", "Chromium";v="119", "Not?A_Brand";v="24"""',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "Windows",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "cross-site",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36",
        "x-algolia-api-key": "b499e29eb7542dc373ec0254e007205d",
        "x-algolia-application-id": "VFM4X0N23A",
    }
    
    data = {
        "query": "",
        "filters": filters_str,
        "userToken": "XssZ5RgH1tpicdzUVCsrH",
        "hitsPerPage": 200,
    }

    r = requests.post(url, headers=headers, json=data)

    json_data = json.loads(r.text)

    json.dumps(json_data, indent=4, sort_keys=True)


    mary_dir = {}
    for hit in json_data['hits']:
        mary_dir[hit['name']] = {
            'category': hit['category'],
            'brand': hit['brand'],
            'discounted_price_eighth_ounce': hit['discounted_price_eighth_ounce'],
            'discounted_price_gram': hit['discounted_price_gram'],
            'discounted_price_half_gram': hit['discounted_price_half_gram'],
            'discounted_price_half_ounce': hit['discounted_price_half_ounce'],
            'discounted_price_ounce': hit['discounted_price_ounce'],
            'discounted_price_quarter_ounce': hit['discounted_price_quarter_ounce'],
            'discounted_price_two_gram': hit['discounted_price_two_gram'],
            'price_eighth_ounce': hit['price_eighth_ounce'],
            'price_gram': hit['price_gram'],
            'price_half_gram': hit['price_half_gram'],
            'price_half_ounce': hit['price_half_ounce'],
            'price_ounce': hit['price_ounce'],
            'price_quarter_ounce': hit['price_quarter_ounce'],
            'price_two_gram': hit['price_two_gram'],
            'dpg': [],
        }

        removekeys = []
        for key, value in mary_dir[hit['name']].items():
            if "price" in key:
                if value is None:
                    removekeys.append(key)
                    continue
                if 'price_eighth_ounce' in key:
                    dpg = (float(value) / 3.5)
                    mary_dir[hit['name']]['dpg'].append([dpg, "3.5", value])
                    removekeys.append(key)
                    continue
                elif 'price_quarter_ounce' in key:
                    dpg = (float(value) / 7)
                    mary_dir[hit['name']]['dpg'].append([dpg, "7", value])
                    removekeys.append(key)
                    continue
                elif 'price_half_ounce' in key:
                    dpg = (float(value) / 14)
                    mary_dir[hit['name']]['dpg'].append([dpg, "14", value])
                    removekeys.append(key)
                    continue
                elif 'price_ounce' in key:
                    dpg = (float(value) / 28)
                    mary_dir[hit['name']]['dpg'].append([dpg, "28", value])
                    removekeys.append(key)
                    continue
                elif 'price_gram' in key:
                    dpg = (float(value))
                    mary_dir[hit['name']]['dpg'].append([dpg, "1", value])
                    removekeys.append(key)
                    continue
                elif 'price_two_gram' in key:
                    dpg = (float(value) / 2)
                    mary_dir[hit['name']]['dpg'].append9([dpg , "2", value])
                    removekeys.append(key)
                    continue
                elif 'price_half_gram' in key:
                    dpg = (float(value) / 0.5)
                    mary_dir[hit['name']]['dpg'].append([dpg, "3", value])
                    removekeys.append(key)
                    continue
                else:
                    print("Error at DPG calculation")
                
            else:
                continue


        mary_dir[hit['name']]['dpg'].sort()

        for key in removekeys:
            del mary_dir[hit['name']][key]

    mary_dir = dict(sorted(mary_dir.items(), key=lambda item: item[1]['dpg'][0])[:5])

    return mary_dir

def dutchrequest(dutchID):
    url = "https://dutchie.com/graphql"
    params = {
        "operationName": "FilteredProducts",
        "variables": unquote(f"%7B%22includeEnterpriseSpecials%22%3Afalse%2C%22includeCannabinoids%22%3Atrue%2C%22productsFilter%22%3A%7B%22dispensaryId%22%3A%22{dutchID}%22%2C%22pricingType%22%3A%22rec%22%2C%22strainTypes%22%3A%5B%5D%2C%22subcategories%22%3A%5B%5D%2C%22Status%22%3A%22Active%22%2C%22types%22%3A%5B%22Flower%22%5D%2C%22useCache%22%3Afalse%2C%22sortDirection%22%3A1%2C%22sortBy%22%3A%22weight%22%2C%22isDefaultSort%22%3Atrue%2C%22bypassOnlineThresholds%22%3Afalse%2C%22isKioskMenu%22%3Afalse%2C%22removeProductsBelowOptionThresholds%22%3Atrue%7D%2C%22page%22%3A0%2C%22perPage%22%3A200%7D"),
        "extensions": unquote("%7B%22persistedQuery%22%3A%7B%22version%22%3A1%2C%22sha256Hash%22%3A%22c75ea6b6d5a7bd30e52aed3b09da754c712817244e43a794c127da602ea06fce%22%7D%7D")
    }
    headers = {
        "sec-ch-ua": '"Microsoft Edge";v="119", "Chromium";v="119", "Not?A_Brand";v="24"',
        "apollographql-client-name": "Marketplace (production)",
        "Prefer": "safe",
        "sec-ch-ua-mobile": "?0",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36 Edg/119.0.0.0",
        "content-type": "application/json",
        "accept": "*/*",
        #"Referer": "https://dutchie.com/embedded-menu/710-kingston/products/flower?page=3&potencycbd=0%2C50&potencythc=0%2C50",
        #"url": "https://dutchie.com/embedded-menu/710-kingston/products/flower?page=3&potencycbd=0%2C50&potencythc=0%2C50",
        "sec-ch-ua-platform": '"Windows"',
    }

    response = requests.get(url, params=params, headers=headers)

    json_data = json.loads(response.text)

    json.dumps(json_data, indent=4, sort_keys=True)

    dutch_dir = {}
    for product in json_data["data"]["filteredProducts"]["products"]:
        dutch_dir[product["Name"]] = {
            "category": product["strainType"],
            "brand": product["brandName"],
            "weights": product["Options"],
            "prices": product["recPrices"],
            "specialPrices": product["recSpecialPrices"],
            "dpg": []
        }

        current = dutch_dir[product["Name"]]

        if current["specialPrices"] is None:
            del current["specialPrices"]
            continue
        elif current["specialPrices"] is not None:
            for price in range(len(current["specialPrices"])):
                current["prices"][price] = current["specialPrices"][price]
            del current["specialPrices"]

        dpgtemp = []
        for offer in range(len(current["prices"])):
            current["weights"][offer] = current["weights"][offer].replace("g", "")
            dpg = float(current["prices"][offer]) / float(current["weights"][offer])
            dpgtemp.append([dpg, current["weights"][offer], current["prices"][offer]])
            dpgtemp.sort(key=lambda x: x[0])
        current["dpg"] = dpgtemp
        del dpgtemp

        del current["prices"]
        del current["weights"]


    dutch_dir = dict(sorted(dutch_dir.items(), key=lambda item: item[1]['dpg'][0])[:5])

    return dutch_dir


dutchIDs = {"710": "5fefa138b2782100c5acd671", "Giggles": "62e858e63967b40082a6aba1"}
janeIDs = {"MaryJ's" : 3217, "Inspired" : 4556}

output = {}

for key, value in janeIDs.items():
    filters_str = f"store_id : {value} AND (root_types:\"flower\")"
    output[key] = janeRequest(filters_str)

for key, value in dutchIDs.items():
    output[key] = dutchrequest(value)


if os.path.exists('output.json'):
    os.remove('output.json')

with open('output.json', 'w') as f:
   json.dump(output, f, indent=4)
   f.close