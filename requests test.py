import requests
from bs4 import BeautifulSoup

url = 'https://www.leafly.com/strains/lists/category/indica'

payload = {
    "portalId":"21108639",
    "referrer":"https://gigglescannabis.ca/",
    "currentUrl":"https://dutchie.com/embedded-menu/giggles?_ga=2.129109260.1647657376.1699254405-806277750.1699254405"
}

r = requests.get(url, params=payload)
pagesource = r.text





#<span class="mobile-product-list-item__ProductName-zxgt1n-6 hBmGOx">INFO HERE</span> <-- this is for strain/name
#<button value="3.5g" label="3.5g" class="clickable__StyledButton-uqcx8d-0 hXFoyD weight-tile__MultiTile-otzu8j-2 esCRpt"> <== for price and weight