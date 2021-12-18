import pandas as pd
from bs4 import BeautifulSoup as bs
import pymongo
from webdriver_manager.chrome import ChromeDriverManager
import requests
from splinter import Browser
import time

def scrape_info():
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)

    mars_url = 'https://redplanetscience.com/'
    browser.visit(mars_url)

    time.sleep(1)

    html = browser.html
    mars_soup = bs(html, 'html.parser')

    title = mars_soup.find('div', class_='content_title').text
    teaser = mars_soup.find('div', class_='article_teaser_body').text

    jpl_url = 'https://spaceimages-mars.com/'
    browser.visit(jpl_url)

    time.sleep(1)

    html = browser.html
    jpl_soup = bs(html, 'lxml')

    image = jpl_soup.find_all('img', class_= "headerimage fade-in")[0]["src"]
    featured_image_url = jpl_url + image


    url = 'https://galaxyfacts-mars.com/'


    mars_table = pd.read_html(url)

    facts_df = mars_table[0]
    facts_df.columns = ['Description', 'Mars', 'Earth']

    mars_html_table = facts_df.to_html(border="1", justify="left")

    mars_html_table.replace('\n', '')

    hems_url = 'https://marshemispheres.com/'
    browser.visit(hems_url)

    time.sleep(1)
 
    html = browser.html
    hems_soup = bs(html, 'lxml')

    all_hemispheres = hems_soup.find('div', class_= "collapsible results")

    each_hemisphere = all_hemispheres.find_all('div', class_='item')

    hems_link = []


    for one in each_hemisphere:

        hems_title = one.find("h3").text
        hems_title = hems_title.replace("Enhanced", "")
        
        image = one.find('img', class_= "thumb")["src"]

        img_url = hems_url + image

        hems_dict = {}
        hems_dict['title'] = hems_title
        hems_dict['img_url'] = img_url
        
        hems_link.append(hems_dict)

    mars_data_dict = {
        "news_title": title,
        "news_info": teaser,
        "featured_image_url": featured_image_url,
        "fun_facts_table": str(mars_html_table),
        "hemisphere_info": hems_link
    }

    browser.quit()

    return mars_data_dict