#Purpose: send a request to the inputed dispenaries and then extract data from the response and sort it.
#Author: cat-thats-fat
#Date: 10-04-2024
#Version: 2.2
#Current Task: Add support for iheartjane
#To-Do:
    # Create menu option for finding a stores ID given a link to store
    # Create menu option to add/remove stores


import os
import json
import requests
from urllib.parse import quote
from config import dutchIDS, path

#function to clear terminal and return home
def home(currentchoice):
    os.system('cls' if os.name == 'nt' else 'clear')
    main(currentchoice)

#function which takes a dictionary and spits out a list sorted smallest dpg to biggest.
def sorter(extracted):
    items = [[key, item] for key, item in extracted.items()]
    sortedlist = sorted(items, key=lambda x: x[1]["options"][0][0])
    sorteddict = dict(sortedlist)
    return sorteddict

#function to handle requests to dutchie and extracting/formatting data from the response
def dutchrequest(info , dutchfilters, currentchoice):

    #build the request
    
    url = "https://dutchie.com/graphql"
    
    variables = {
        "includeEnterpriseSpecials": False,
        "includeCannabinoids": True,
        "productsFilter": {
            "dispensaryId": info["id"],
            "pricingType": "rec",
            "strainTypes": [dutchfilters["strainType"][currentchoice[0]]],
            "subcategories": [],
            "Status": "Active",
            "types": [dutchfilters["category"][currentchoice[1]]],
            "useCache": False,
            "sortDirection": 1,
            "sortBy": "weight",
            "isDefaultSort": True,
            "bypassOnlineThresholds": False,
            "isKioskMenu": False,
            "removeProductsBelowOptionThresholds": True
        },
        "page": 0,
        "perPage": 200
    }

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

    response = json.loads(responseraw.text)

    # extract the useful data from the response

    extracted = {}

    for product in response["data"]["filteredProducts"]["products"]:
        
        # calculate dollars per gram
        prices = product["Prices"]
        weights = product["Options"]
        discount = info["discount"]

        options = []

        for i in range(len(prices)):
            currentoffer = []
            weights[i] = weights[i].replace("g", "")
            dpg = float(prices[i])/float(weights[i])
            if discount == 0: currentoffer.append(dpg)
            else:
                finaldpg = dpg*(1-discount/100)
                currentoffer.append(finaldpg)
            currentoffer.extend([prices[i], weights[i]])
            options.append(currentoffer)
            
        options.sort(key=lambda x: x[0])



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
        
    #Return the sorted dictionary

    return sorteddict

#function to handle requests to iheartjane and extracting/formatting data from the response
def maryrequest(maryID , category):
    #Build the request
    #send the request
    #Format the response
    #Return the response
    return 

#dutchie filter keys
dutchfilters = {
    "category": ["Flower", "Vaporizers", "Pre-Rolls", "Concentrate" ],
    "strainType": ["Sativa", "Indica", "Hybrid", ""],
}

filters = {
    "category": ["Flower", "Vaporizers", "Pre-Rolls", "Concentrate" ],
    "strainType": ["Sativa", "Indica", "Hybrid", ""],
}
# first is type second is cate
currentchoice = [0, 0]

def main(currentchoice):

    cate = filters["category"][currentchoice[0]]
    type = filters["strainType"][currentchoice[1]]

    print("Cheap Weed Finder")
    print()
    print(f"Current parameters: \n  Category: {cate} \n  Type: {type}")
    print()
    print("1. Change search parameters")
    print("2. Search")
    print("3. Exit")

    choice = int(input(">"))

    if choice == 1:
        print("Change Search Parameters")
        print()
        print("Available Categories: Flower(1), Vaporizers(2), Pre-rolls(3), Concentrate)(4)")
        print()
        print("Strain types: Sativa(1), Indica(2), Hybrid(3), No Prefrence(4)")
        print()
        
        currentchoice[1] = int(input("Enter the category you'd like to search.")) - 1
        currentchoice[0] = int(input("Enter the type of strain you'd like to search.")) - 1
        home(currentchoice)
    elif choice == 2:

        os.system('cls' if os.name == 'nt' else 'clear')
        count = 1
        print("Requesting Data")
        
        output = {}

        #Loop through the IDs and request the data
        if len(dutchIDS) > 0:
            for name, info in dutchIDS.items():
                output[name] = (dutchrequest(info, dutchfilters, currentchoice))
                print(f"{count}/{len(dutchIDS)} stores searched")
                count += 1
            print("Search Complete")

#write the output
        with open(f"{path}/output.json", "w") as f:
            json.dump(output, f, indent=4)
            f.close

        print("Results Saved.")
        input("Press enter to exit...")

    elif choice == 3:
        exit()

main(currentchoice)