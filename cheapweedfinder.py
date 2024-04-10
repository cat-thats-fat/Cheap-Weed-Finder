import json
import requests
from urllib.parse import quote

def dutchrequest(info , dutchfilters):

    #build the request
    
    url = "https://dutchie.com/graphql"
    
    variables = {
        "includeEnterpriseSpecials": False,
        "includeCannabinoids": True,
        "productsFilter": {
            "dispensaryId": info["id"],
            "pricingType": "rec",
            "strainTypes": [dutchfilters["strainType"][1]],
            "subcategories": [],
            "Status": "Active",
            "types": [dutchfilters["category"][0]],
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
            if discount != 0: currentoffer.append(dpg)
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

    # sort all offers by their best dpg(the first one bc its already sorted)
    sorted = []
    count = 0

    #need to create a sorted list
        

        

    #Return the response

    return sorted

def maryrequest(maryID , category):
    #Build the request
    #send the request
    #Format the response
    #Return the response
    return output

#Where the store IDS are stored
dutchIDS = {
    "Giggles":  {
        "id": "62e858e63967b40082a6aba1",
        "discount": 10
    },
    "Avenue":  {
        "id": "630693d206463800b24a8e4c",
        "discount": 10
    },
}

dutchfilters = {
    "category": ["Flower", "Vaporizers", "Pre-Rolls", "Concentrate" ],
    "strainType": ["Sativa", "Indica", "Hybrid"],
    "discount": 10
}



output = {}

if __name__ == "__main__":
    #Loop through the IDs and request the data
    loop = 0
    if len(dutchIDS) > 0:
        for name, info in dutchIDS.items():
           output[name] = dutchrequest(info, dutchfilters)
           loop += 1
           print(loop)
    
    with open("output.json", "w") as f:
        json.dump(output, f, indent=4)
        f.close

    print("done")

