#!/usr/bin/env python
# coding: utf-8

# In[1]:


#Import dependencies
import pandas as pd
import pymongo
import requests
from splinter import Browser
from bs4 import BeautifulSoup as soup
from webdriver_manager.chrome import ChromeDriverManager


# In[2]:


# configure ChromeDriver
executable_path = {'executable_path': ChromeDriverManager().install()}
browser = Browser('chrome', **executable_path)


# In[3]:


#### NASA MARS NEWS ####


# In[4]:


def mars_news(): 
   
    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)

    html = browser.html
    new_soup = soup(html, 'html.parser')

    #article_container = new_soup.select('ul.item_list')
    article_container = new_soup.find('ul', class_ = 'item_list')


    headline_date = article_container.find('div', class_ = 'list_date').text
    news_title = article_container.find('div', class_ = 'content_title').find('a').text
    news_p = article_container.find('div', class_ = 'article_teaser_body').text

    return news_title, news_p


# # JPL MARS SPACE IMAGES

# In[5]:


def featured_image():   
   url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
   browser.visit(url)

   htlm = browser.html
   img_soup = soup(html, 'html.parser')

   #Method 1
   try:
       img_element = img_soup.find('article', class_ = 'carousel_item')['style']

       img_rel_url = img_element.replace("backround-image: url('",'')
       img_rel_url = img_rel_url.replace("');",'')

       print(img_rel_url)
   except Exception as e:
       print(e)
       #Method 2
   try:
       full_image_elem = browser.find_by_id('full_image')[0]
       full_image_elem.click()

       html = browser.html
       img_soup = soup(html, 'html.parser')
       img_rel_url = img_soup.find('img', class_ = 'fancybox-image')['scr']
       print(img_rel_url)

       featured_image_url = f'{base_url}{img_rel_url}'
       print(featured_img_url)
   except Exception as e:
       print(e)
   return featured_img_url


# #Mars Facts

# In[6]:


def mars_facts():
    
    url = 'https://space-facts.com/mars/'
    browser.visit(url)

    mars_facts_df = pd.read_html(url)
    mars_facts_df = mars_facts_df[0]
    mars_facts_df.columns = ['Description', 'Mars']
    mars_facts_df

    mars_facts_html = mars_facts_df.to_html(classes='table table-striped')
    
    return mars_facts_html


# In[7]:


html = browser.html
facts_soup =soup(html, 'html.parser')
facts_soup.find(id='tablepress-p-mars')


# # Mars 

# In[ ]:





# # Insert into Mongo DB

# In[8]:


def scrape_all():

    news_title, news_p = mars_news()
    featured_img_url = featured_image()
    mars_facts_html = mars_facts()

    #Assemble the document to insert into the database
    nasa_document = {
        'news_title': news_title,
        'news_paragraph': news_p,
        'featured_img_url': featured_img_url,
        'mars_fact_html': mars_facts_html
    }

    return nasa_document


# In[9]:


#Connect to MongoDB

conn = 'mongodb://localhost:27017'
client =pymongo.MongoClient(conn)

db = client.mars_app

mars = db.mars

data_document = scrape_all()


mars.update_one({},{'$set': data_document}, upsert=True)


# In[ ]:




