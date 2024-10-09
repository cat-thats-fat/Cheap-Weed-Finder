import os
import json
import requests
from urllib.parse import quote

#function to clear the console no matter what platform you are on
def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

# function which takes a dictionary and spits out a list sorted smallest dpg to biggest.
def sorter(extracted):
    items = [[key, item] for key, item in extracted.items()]
    sortedlist = sorted(items, key=lambda x: x[1]["options"][0][0])
    sorteddict = dict(sortedlist)
    return sorteddict


# function to handle requests to dutchie and extracting/formatting data from the response
def dutchrequest(info, config):

    dutchfilters = {
        "category": ["Flower", "Vaporizers", "Pre-Rolls", "Concentrate"],
        "strainType": ["Sativa", "Indica", "Hybrid", ""],
    }

    #print(config["choices"]["strain"])
    #print(dutchfilters["strainType"][config["choices"]["strain"]])
    #set match our chosen filters to the syntax of the api
    strainchoice = dutchfilters["strainType"][config["choices"]["strain"]]
    categorychoice = dutchfilters["category"][config["choices"]["category"]]

    # build the request
    url = "https://dutchie.com/graphql"

    variables = {
        "includeEnterpriseSpecials": False,
        "includeCannabinoids": True,
        "productsFilter": {
            "dispensaryId": info["id"],
            "pricingType": "rec",
            "subcategories": [],
            "Status": "Active",
            "types": [categorychoice],
            "useCache": False,
            "sortDirection": 1,
            "sortBy": "weight",
            "isDefaultSort": True,
            "bypassOnlineThresholds": False,
            "isKioskMenu": False,
            "removeProductsBelowOptionThresholds": True
        },
    }

    # only include strainTypes in variables if strainchoice is not an empty string
    if strainchoice:
        variables["productsFilter"]["strainTypes"] = [strainchoice]


    extensions = {
        "persistedQuery": {
            "version": 1,
            "sha256Hash": "c75ea6b6d5a7bd30e52aed3b09da754c712817244e43a794c127da602ea06fce"
        }
    }

    params = {
        "operationName": "FilteredProducts",
        "variables": json.dumps(variables),
        "extensions": json.dumps(extensions)
    }

    headers = {
        "sec-ch-ua": '"Microsoft Edge";v="119", "Chromium";v="119", "Not?A_Brand";v="24"',
        "apollographql-client-name": "Marketplace (production)",
        "Prefer": "safe",
        "sec-ch-ua-mobile": "?0",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36 Edg/119.0.0.0",
        "content-type": "application/json",
        "accept": "*/*",
        "sec-ch-ua-platform": '"Windows"',
    }

    # send the request
    responseraw = requests.get(url, params=params, headers=headers)

    #print(responseraw.text)

    response = json.loads(responseraw.text)

    # extract the useful data from the response

    extracted = {}

    discount = (1 - float(info["discount"]) / 100)

    for product in response["data"]["filteredProducts"]["products"]:

        # calculate dollars per gram
        prices = product["Prices"]
        weights = product["Options"]

        options = []

        for i in range(len(prices)):
            currentoffer = []
            weights[i] = weights[i].replace("g", "")
            dpg = float(prices[i]) / float(weights[i])
            if discount == 0:
                currentoffer.append(dpg)
            else:
                finaldpg = dpg * discount
                currentoffer.append(finaldpg)
            currentoffer.extend([prices[i], weights[i]])
            options.append(currentoffer)

        options.sort(key=lambda x: x[0])

        #format the data
        extracted[product["Name"]] = {
            "brand": product["brandName"],
            "strainType": product["strainType"],
            "options": options,
            "thc": {
                "unit": product["THCContent"]["unit"] if product["THCContent"] else "",
                "range": product["THCContent"]["range"] if product["THCContent"] else "",
            },
            "cbd": {
                "unit": product["CBDContent"]["unit"] if product["CBDContent"] else "",
                "range": product["CBDContent"]["range"] if product["CBDContent"] else "",
            },
        }

    #sort dictionary
    sorteddict = sorter(extracted)

    #return the sorted dictionary
    return sorteddict


#function to handle requests to iheartjane and extracting/formatting data from the response
def janerequest(info, config):

    maryfilters = {
        "category": ["flower", "pre-rolls", "vaporizer", "extract"],
        "strainType": ["Sativa", "Indica", "Hybrid", ""],
    }

    strainchoice = maryfilters["strainType"][config["choices"]["strain"]]
    categorychoice = maryfilters["category"][config["choices"]["category"]]

    #build the request

    filters = f"store_id = {info['id']} AND kind:\"{categorychoice}\" OR root_types:\"{categorychoice}\""

    #check if no strain preferance
    if strainchoice != "":
        filters += f" AND (category:\"{strainchoice}\")"

    request = {
        "method": "POST",
        "url": "https://search.iheartjane.com/1/indexes/menu-products-production/query?x-algolia-agent=Algolia%20for%20JavaScript%20(4.14.2)%3B%20Browser",
        "headers": {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36 Edg/123.0.0.0",
            "content-type": "application/x-www-form-urlencoded",
            "x-algolia-api-key": "edc5435c65d771cecbd98bbd488aa8d3",
            "x-algolia-application-id": "VFM4X0N23A"
        },
        "data": {
            "query": "",
            "filters": filters,
            "facets": ["*"],
            "hitsPerPage": 200
        }
    }

    #send the request

    response = requests.post(request['url'], headers=request['headers'], data=json.dumps(request['data']))

    jsoned = json.loads(response.text)

    #extract wanted data

    extraction = {}

    for product in jsoned["hits"]:
        extraction[product["name"]] = {
            "brand": product["brand"],
            "strainType": product["type"],
            "temp": {
                "price_gram": [product["price_gram"]],
                "discounted_price_gram": [product["discounted_price_gram"]],
                "price_two_gram": [product["price_two_gram"]],
                "discounted_price_two_gram": [product["discounted_price_two_gram"]],
                "price_eighth_ounce": [product["price_eighth_ounce"]],
                "discounted_price_eighth_ounce": [product["discounted_price_eighth_ounce"]],
                "price_quarter_ounce": [product["price_quarter_ounce"]],
                "discounted_price_quarter_ounce": [product["discounted_price_quarter_ounce"]],
                "price_half_ounce": [product["price_half_ounce"]],
                "discounted_price_half_ounce": [product["discounted_price_half_ounce"]],
                "price_ounce": [product["price_ounce"]],
                "discounted_price_ounce": [product["discounted_price_ounce"]],
                "price_half_gram": [product["price_half_gram"]],
                "discounted_price_half_gram": [product["discounted_price_half_gram"]],
                "price_each": [product["price_each"]],
                "discounted_price_each": [product["discounted_price_each"]],
            },
            "options": []
        }

    #process the data

    weightvals = {
        "priceeach": 1,
        "half_gram": 0.5,
        "price_gram": 1,
        "price_two_gram": 2,
        "eight": 3.5,
        "quarter": 7,
        "half": 14,
        "price_ounce": 28,
    }

    for product in extraction:

        current = extraction[product]
        keys2go = []

        for offer in current["temp"]:
            if not current["temp"][offer][0]:
                keys2go.append(offer)
            for key in weightvals:
                if key in offer:
                    current["temp"][offer].append(weightvals[key])

        for key in keys2go:
            del current["temp"][key]

        #calculate the dollars per gram

        for offer in current["temp"]:

            price = float(current["temp"][offer][0])
            weight = float(current["temp"][offer][1])

            dpg = (price / weight) * (1 - (info["discount"] / 100))

            current["options"].append([dpg, weight, price])

        #remove the temporary dictionary

        del current["temp"]

    #return the output
    sorteddict = sorter(extracted=extraction)
    return sorteddict