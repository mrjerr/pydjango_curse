#!/usr/bin/env python
# -*- coding: utf-8
import json
from time import time
from lxml.html import fromstring
from urllib.request import urlopen
from selection import XpathSelector

START_URL = 'http://hotline.ua/mobile/mobilnye-telefony-i-smartfony/?p={}'
PAG_RANGE = [0,93]
XPATH_ITEM = './/ul[@class="catalog  clearfix"]/li'
XPATH_ITEM_AVGPRICE = './/div[@class="price"]/span/node()'
XPATH_ITEM_NAMEURL = './/div[@class="ttle"]/a'
XPATH_ITEM_FEATR = 'div/p[@class="tech-char"]'

def get_urls(start_url, pag_range, save_json=''):
    """
    {   
        "name": str_value,
        "avgPrice": int_value,
        "url": str_url,
        "features":  str_value
    }
    
    """
    t = time()
    data = []
    for i in range(*pag_range):
        print(i, time()-t,'sec')
        http_resp = urlopen(start_url.format(i))
        
        if http_resp.code != 200:
            print('Problem ulr {}, Code - {}'.format(start_url.format(i),http_resp.code))
            return False
            
        html = http_resp.read()
        sel = XpathSelector(fromstring(html))
        
        for item in sel.select(XPATH_ITEM):
            name = item.select(XPATH_ITEM_NAMEURL).text()
            url = item.select(XPATH_ITEM_NAMEURL).attr('href')
            try:
                avg_price =  int(item.select(XPATH_ITEM_AVGPRICE).text()[:-4].replace(' ',''))
            except:
                print(name, url, 'Error price')
                avg_price = 'nd'
            try:
                features = item.select(XPATH_ITEM_FEATR).text()
            except:
                print(name, url, 'Error features')
                features = 'None'
            
            data.append( {
                "name": name,
                "avgPrice": avg_price,
                "url": url,
                "features": features
            })
    if save_json:
        with open(save_json, 'w') as fp:
            json.dump(data, fp, indent=2, sort_keys=True, ensure_ascii=False)
        return True
    return data

def main():
    get_urls(start_url=START_URL, pag_range=PAG_RANGE, save_json='hotline_smartphones.json')


if __name__ == "__main__":
    main()
