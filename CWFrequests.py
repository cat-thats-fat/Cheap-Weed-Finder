import os
import json
import requests

url = "https://vfm4x0n23a-2.algolianet.com/1/indexes/menu-products-production/query?x-algolia-agent=Algolia%20for%20JavaScript%20(4.14.2)%3B%20Browser"

params = {
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
    "x-algolia-application-id": "VFM4X0N23A"
}

data = {
    "query": "",
    "filters": "store_id :  4556 AND (root_types:\"flower\")",
    "userToken": "XssZ5RgH1tpicdzUVCsrH",
    "hitsPerPage": 48
}

r = requests.post(url, headers=params, json=data)

json_data = json.loads(r.text)

json.dumps(json_data, indent=4, sort_keys=True)


weed_dir = {}
for hit in json_data['hits']:
    weed_dir[hit['name']] = {
        'description': hit['description'],
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

    for key, value in weed_dir[hit['name']].items():
        if "price" in key:
            if value is None:
                continue
            if 'price_eighth_ounce' in key:
                weed_dir[hit['name']]['dpg'].append((float(value) / 3.5)*0.85)
                continue
            elif 'price_quarter_ounce' in key:
                weed_dir[hit['name']]['dpg'].append((float(value) / 7)*0.85)
                continue
            elif 'price_half_ounce' in key:
                weed_dir[hit['name']]['dpg'].append((float(value) / 14)*0.85)
                continue
            elif 'price_ounce' in key:
                weed_dir[hit['name']]['dpg'].append((float(value) / 28)*0.85)
                continue
            elif 'price_gram' in key:
                weed_dir[hit['name']]['dpg'].append((float(value))*0.85)
                continue
            elif 'price_two_gram' in key:
                weed_dir[hit['name']]['dpg'].append9((float(value) / 2)*0.85)
                continue
            elif 'price_half_gram' in key:
                weed_dir[hit['name']]['dpg'].append((float(value) / 0.5)*0.85)
                continue
            else:
                print("Error at DPG calculation")
        else:
            continue
    weed_dir[hit['name']]['dpg'].sort()

weed_dir = dict(sorted(weed_dir.items(), key=lambda item: item[1]['dpg'][0]))

if os.path.exists('weed_dir.json'):
    os.remove('weed_dir.json')

with open('weed_dir.json', 'w') as f:
    json.dump(weed_dir, f, indent=4)
    f.close


