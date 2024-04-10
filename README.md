# Cheap Weed Finder
### This is a program made to help you find the best deals on weed!

## Supported APIs:

  Dutchie
  
  Iheartjane(COMING SOON)

## Features:

  Search for Flower, Pre-rolls, Vaporizers and Concentrates.
  
  Store by store discount.
  
  Can search multiple stores.
  
### To-be-added Features:

  Maximum price.
  
  Add/remove stores without needing to change code
  
## Configuring:
To remove/add stores edit config.py

You also need to enter the output path in config.py

If you do not have a discount at a store enter the value 0

  ### iheartjane: 
    Inspect the dispensary's website and then Ctrl + F search for "storeID" in the html, it should be 4 digits.

 ### dutchie: 
    Inspect the dispensarie's website and go to the network tab.
    With the network tab open, refresh the page and filter for Fetch/XHR.
    Look for requests like graphql?operationName=FilteredProducts/MenuFilters/GetMenuSelection, it doesnt matter which you pick.
    Then press the payload tab and press view decoded.
    In the variable row you should see "dispensaryId":"XXXXXXXXXXXXXXXXXXXXXXXX". (example: "dispensaryId":"5fefa138b2782100c5acd671")
