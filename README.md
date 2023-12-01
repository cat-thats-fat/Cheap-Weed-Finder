# Kingston-Cheap-Weed
This is a python script that uses iheartjane and dutchie apis to get the data about their bud offers and then calculates and displays the cheapest 5 offers from each dispensary. 

## Adding more stores:
To add more stores find its storeID(instructions below) and add it to their respective lists(ln 196,197)

  ### iheartjane: 
    Inspect the dispensary's website and then Ctrl + F search for "storeID" in the html, it should be 4 digits.

 ### dutchie: 
    Inspect the dispensarie's website and go to the network tab.
    With the network tab open, refresh the page and filter for Fetch/XHR.
    Look for names that start with "graphql?operationName=" and click on it there should be multiple, it doesnt matter which you click.
    Then press the payload tab and press view decoded.
    In the variable row you should see "dispensaryId":"XXXXXXXXXXXXXXXXXXXXXXXX". (example: "dispensaryId":"5fefa138b2782100c5acd671")
