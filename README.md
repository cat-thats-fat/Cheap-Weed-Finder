# Cheap Weed Finder
### This is a program made to help you find the best deals on weed!

## Supported APIs:

  Dutchie
  
  Iheartjane

## Features:

  Search for Flower, Pre-rolls, Vaporizers and Concentrates.
  
  Can search multiple stores.
  
  Store by store discounts
  
### To-be-added Features:

  Maximum price.
  
  Add/remove stores by pasting a link to the storefront, and the program will scrape the ID from it.
  
## Configuring:
To remove/add stores edit config.py just follow the format of the config file that is made for you, the program checks for a config every launch and will make one if not found.

If you do not have a discount at a store enter the value 0

  ### iheartjane: 
    Inspect the dispensary's website and then Ctrl + F search for "storeID" in the html, it should be 4 digits.

 ### dutchie: 
    Inspect the dispensarie's website and go to the network tab.
    With the network tab open, refresh the page and filter for Fetch/XHR.
    Look for requests like graphql?operationName=FilteredProducts/MenuFilters/GetMenuSelection, it doesnt matter which you pick.
    Then press the payload tab and press view decoded.
    In the variable row you should see "dispensaryId":"XXXXXXXXXXXXXXXXXXXXXXXX". (example: "dispensaryId":"5fefa138b2782100c5acd671")

## Disclaimer(s)

### Not an active project

I wont be working on this project for the near future, unless something breaks. Open a issue thread and I'll try and fix the problem.

### Faulty Input Data

Some dispensaries do not input data in its respective fields which will lead to the program crashing or bad output data. There is nothing that can be done about this except maybe inform a dispensary employee.