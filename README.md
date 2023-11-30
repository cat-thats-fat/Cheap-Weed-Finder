# Kingston-Cheap-Weed
i think adding support for other items than just flower wouldn't be much work but i dont think ill get around to it
to add more stores simply add their store IDS to their respective lists(ln 196,197)
how to find storeID:

  iheartjane: 
    inspect the dispensarie's website and then Ctrl + F search for "storeID" in the html, it should be 4 digits

  dutchie: 
    inspect the dispensarie's website and go to the network tab
    with the network tab open, refresh the page and filter for Fetch/XHR
    look for names that start with "graphql?operationName=" and click on it there should be multiple, it doesnt matter which you click
    then press the payload tab and press view decoded
    in the variable row you should see "dispensaryId":"XXXXXXXXXXXXXXXXXXXXXXXX" (example: "dispensaryId":"5fefa138b2782100c5acd671")
