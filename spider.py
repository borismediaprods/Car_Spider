import requests
from bs4 import BeautifulSoup
import re

# Really basic Kijiji Spider, this one looks for cars
# I made it because I need to buy a car, and many ads are just spare car parts
# Which is super annoying to browse through, also *Educational Purposes Only* stuff
# Written by Boris Skurikhin (Boris MediaProds)

# Does this even need a license? No, but I'll throw in MIT just for the lolz.

pages_to_search = 1

def car_spider(max_pages):
    region = 'markham-york-region'
    current_page = 1
    while current_page <= max_pages:
        url = 'http://www.kijiji.ca/b-cars-vehicles/' + region + '/page-' + str(current_page) + '/c27l1700274'
        source_code = requests.get(url)
        plain_text = source_code.text
        soup = BeautifulSoup(plain_text, 'html.parser')
        for link in soup.find_all('a', {'class': 'title'}):
            href = 'http://www.kijiji.ca' + link.get('href')
            get_single_item_data(href)
        current_page += 1

def get_attrib(soup, type, tag, attrib):
    temp = soup.find(type, {tag: attrib})
    return 'undefined' if temp is None else temp.string

def get_single_item_data(item_url):
    source_code = requests.get(item_url)
    plain_text = source_code.text
    soup = BeautifulSoup(plain_text, 'html.parser')

    title = soup.find('h1').string.split()
    for string in title:
        if string.isdigit() and 2000 <= int(string) <= 2012:
            # So we found what it looks to be vehicle (not 100% a car, could be a motorbike)
            # Simple regex to find the price attribute, and remove the extra bullshit.
            raw_price = re.sub('[$,]', '', str(soup.find('span', {'itemprop': 'price'}).string))
            if not re.match('[^0-9]', raw_price):
                price = float(raw_price)
            else:
                price = -1
            year = int(string)
            # Let's get all the important attributes
            make = get_attrib(soup, 'span', 'itemprop', 'brand')
            color = get_attrib(soup, 'span', 'itemprop', 'color')
            model = get_attrib(soup, 'span', 'itemprop', 'model')
            km = -1
            # A terrible way to find the KM count, but it's the first I thoguht of.
            for possible_km in soup.find_all('td'):
                __temp__ = possible_km.string
                if __temp__ is not None:
                    __temp__ = re.sub('[\n ]', '', __temp__)
                    if __temp__.replace(' ', '').isdigit():
                        km = max(km, int(__temp__.replace(' ', '')))
            # Dumb logic, making sure that the car is not *too used* and also within budget.
            # And we don't wanna buy really cheap cars either, they break too often.
            if price >= 30000 or price <= 2000 or km >= 500000:
                return
            print '================================================'
            print 'Price:', 'Contact Owner' if price < 0 else '$' + str(price)
            print 'Year', str(year)
            print 'Make :', make
            print 'Model:', model
            print 'Has', ('an unknown number of' if km < 0 else str(km)) + ' kilometers on it.'
            print 'Color:', color
            print 'Link:', item_url
            # Finished printing the info, now we can move on to other vehicles.

# The actual starting point is here!
car_spider(pages_to_search)
print '============ End of Browsing ============'