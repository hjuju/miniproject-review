from django.db import models

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import pandas as pd
from icecream import ic
import re
from tqdm import tqdm
import googlemaps
import numpy as np
import folium

class Chicago():
    rank = []
    cafe_name = []
    food = []
    price = []
    address = []

    cafe_add = []
    url_add = []
    url_fix = []
    df = None
    url = 'https://www.chicagomag.com/Chicago-Magazine/November-2012/Best-Sandwiches-Chicago/'
    driver_path = 'C:\Program Files\Google\Chrome\chromedriver'


    def scrap(self):
        driver =webdriver.Chrome(self.driver_path)
        driver.get(self.url)
        soup = BeautifulSoup(driver.page_source, 'lxml')
        all_td = soup.find_all('div','sammy')
        for item in all_td:
            self.rank.append(item.find(class_='sammyRank').text)
            temp =item.find(class_='sammyListing').text
            self.cafe_name.append(re.split(('\n'), temp)[1])
            self.food.append(re.split(('\n'), temp)[0])
            self.url_add.append(item.find('a')['href'])

        # ic(self.url_add)

        for acc in self.url_add:
            self.url_fix.append(acc.split('November-2012')[1])

        # ic(self.url_fix)
        for i in self.url_fix:
            driver.get('https://www.chicagomag.com/Chicago-Magazine/November-2012'+i)
            soup = BeautifulSoup(driver.page_source, 'lxml')
            all_tdd = soup.find_all(class_='addy')
            for item in all_tdd:
                all_tddd = item.find('em').text
                self.price.append(all_tddd.split()[0][:-1])
                self.address.append(' '.join(all_tddd.split()[1:-2]))

                # ic(self.price)

        driver.close()

    def insert_DataFrame(self):

        data = {"rank":self.rank,
                                "cafe":self.cafe_name,
                                "food":self.food,
                                "price":self.price,
                                "address":self.address}

        self.df = pd.DataFrame(data,
                               columns=['rank','cafe','food','price','address']
                               )
        ic(self.df)


    def map(self):
        lat = []
        lng = []
        gmaps=googlemaps.Client(key='AIzaSyD7gUbdCzIhR-J_Gr5m3JdDvki9Z_T6bTI')

        for i in tqdm(self.df.index):  # 진행상태 표시위함
            if self.df['address'][i] != 'Multiple':
                target_name = self.df['address'][i] + ', ' + 'Chicago'
                gmaps_output = gmaps.geocode(target_name)
                location_output = gmaps_output[0].get('geometry')
                lat.append(location_output['location']['lat'])
                lng.append(location_output['location']['lng'])

                ic(gmaps_output)

            else:
                lat.append(np.nan)
                lng.append(np.nan)

        self.df['lat'] = lat
        self.df['lng'] = lng
        self.df.head()

        mapping = folium.Map(location=[self.df['lat'].mean(),self.df['lng'].mean()]
                             ,Zoom_start=11)
        for n in self.df.index:
            if self.df['address'][n] != 'Multiple':
                folium.Marker([self.df['lat'][n], self.df['lng'][n]],
                              popup=self.df['cafe'][n]).add_to(mapping)

        folium.LayerControl().add_to(mapping)

        mapping.save('./saved_data/chicago_sandwiches.html')


if __name__ == '__main__':
    c = Chicago()
    c.scrap()
    c.insert_DataFrame()
    c.map()


