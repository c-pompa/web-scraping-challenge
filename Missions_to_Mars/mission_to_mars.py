#!/usr/bin/env python
# coding: utf-8

# ### Dependencies

# In[1]:


# Dependencies
from bs4 import BeautifulSoup
import requests
import pymongo
from pprint import pprint
from splinter import Browser
from splinter.exceptions import ElementDoesNotExist
import pandas as pd


# ### Connection string from pymongo to mongodb

# In[2]:


# Initialize PyMongo to work with MongoDBs
# Connection string should reference mongodb, localhost, and port 27017
conn = 'mongodb://localhost:27017'
# Instantiate at `pymongo.MongoClient()` object with your `conn`
client = pymongo.MongoClient(conn)


# In[ ]:


# Define database and collection
db = client.missiontomars
collection = db.articles


# ### URL to scrape

# In[ ]:


# URL of page to be scraped
url = 'https://mars.nasa.gov/news/'


# In[ ]:


# Retrieve page with the requests module .get() method
response = requests.get(url)


# ### BeautifulSoup object to parse

# In[ ]:


# Create BeautifulSoup object; parse the `response.text` with 'lxml'
soup = BeautifulSoup(response.text, 'lxml')
pprint(soup)


# Collect the latest News Title and Paragraph Text. Assign the text to variables that you can reference later.

# In[ ]:





# In[ ]:


# Latest News Title
news_title = soup.find('div', class_='content_title').a.text.strip()
news_title


# In[ ]:


# Latest News Title Paragraph
news_p = soup.find('div', class_='rollover_description_inner').text.strip()
news_p


# In[ ]:





# ### Splinter

# Using Splinter, I will grab the features Mars space image from https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars

# In[ ]:


executable_path = {'executable_path': 'chromedriver.exe'}
browser = Browser('chrome', **executable_path, headless=False)


# In[ ]:


url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
browser.visit(url)


# In[ ]:


# Iterate through JPL space images. Find featured image full size link
for x in range(1):
    # HTML object
    html = browser.html
    # Instantiate a BeautifulSoup() object with our `html` and the `html5lib` parser
    soup = BeautifulSoup(html, 'html5lib')
    
    # Article holding pics
    articles = soup.find('article')
    # Click Featured space image, click more information and grab main image full size
    try:
        browser.click_link_by_partial_text('FULL IMAGE')
        browser.click_link_by_partial_text('more info')

        # Go in article and find image
        for article in articles: 
            # Tell beautifulsoup where we are by calling new browser URL
            url = browser.url
            # Retrieve page with the requests module .get() method
            response = requests.get(url)
            # Create BeautifulSoup object; parse the `response.text` with 'lxml'
            soup = BeautifulSoup(response.text, 'lxml')
            
            # class holding image
            pic_link = soup.find('figure', class_='lede')
            # image anchor
            anchor = pic_link.a['href']
            # create image full link. Only received half the link.
            featured_image_url = ('https://www.jpl.nasa.gov'+anchor)
            print('-----------')
            print(featured_image_url)
            print('-----------')
            break

    except:
        print("No image link")


# ### Featured image URL

# In[ ]:


featured_image_url


# In[ ]:





# ## Mars Weather

# Get the latest weather data from Mars Weather latest twitter post.

# In[ ]:


executable_path = {'executable_path': 'chromedriver.exe'}
browser = Browser('chrome', **executable_path, headless=False)


# In[ ]:


url = 'https://twitter.com/marswxreport?lang=en'
browser.visit(url)


# In[16]:


# Iterate through JPL space images. Find featured image full size link
for x in range(1):
    # HTML object
    html = browser.html
    # Instantiate a BeautifulSoup() object with our `html` and the `html5lib` parser
    soup = BeautifulSoup(html, 'html5lib')
    
    # Article holding pics
    articles = soup.find('article')
    
    
    mars_weather = articles.find_all('span', class_='css-901oao css-16my406 r-1qd0xha r-ad9z0x r-bcqeeo r-qvutc0')[4].text
    
    print(mars_weather)


# In[17]:


# Latest Mars weather data from twitter
mars_weather


# In[ ]:





# ### Mars Facts
# Scrape the table containing facts about the planet including Diameter, Mass, etc.
# 

# In[18]:


url = 'https://space-facts.com/mars/'


# In[22]:


# Use Panda's `read_html` to parse the url
### BEGIN SOLUTION
tables = pd.read_html(url)
tables
### END SOLUTION


# In[25]:


mars_table_df = tables[1]
mars_table_df


# In[ ]:





# In[28]:


# Convert table to HTML in notebooks
mars_table_html = mars_table_df.to_html()
mars_table_html


# In[29]:


# Clean table from \n values
mars_table_html = mars_table_html.replace('\n', '')
mars_table_html


# In[30]:


# Save Mars table to an HTML file
mars_table_df.to_html('mars_table.html')


# In[ ]:





# ### **Mars Hemispheres**

# In[86]:


executable_path = {'executable_path': 'chromedriver.exe'}
browser = Browser('chrome', **executable_path, headless=False)


# In[87]:


# URL to scrape
url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
browser.visit(url)


# In[88]:


# Assign html to brownser
html = browser.html


# In[89]:


# Instantiate a BeautifulSoup() object with our `html` and the `html5lib` parser
soup = BeautifulSoup(html, 'html5lib')


# In[90]:


# Find the 'div' containing the 4 hemisphere selections
hemis = soup.find('div', class_='collapsible results')

# Find all(each) the 'div' with title descriptions
hemis_single = hemis.find_all('div', class_='description')


# In[91]:


# Create empty lists. Will store titles and URL's to the specific hemisphere webpage
hemis_list = []
url_list = []

# Search current page, add hemis title to hemis_list
# Search current page, add specific hemis url to url_list to loop through
for category in hemis_single:
    title = category.h3.text
    hemis_list.append(title)
    web_url = category.find('a')['href']
    url_list.append(web_url)


# In[92]:


# Complete the full url for each hemisphere webpage
hemis_url_list = ['https://astrogeology.usgs.gov' + url for url in url_list]


# In[93]:


# Combine both lists for looping
hemis_and_urls = zip(hemis_list, hemis_url_list)


# Add data found to hemisphere_image_urls

# In[94]:


# Create empty list to fill
hemisphere_image_urls = []

# Loop through combined list, create dict for title and img_url, return list of dict
for titles, urls in hemis_and_urls:
    # Tell beautifulsoup where we are by calling new browser URL
    url = urls
    # Retrieve page with the requests module .get() method
    response = requests.get(url)
    # Create BeautifulSoup object; parse the `response.text` with 'lxml'
    soup = BeautifulSoup(response.text, 'lxml')

    # Full Size image
    hemis_image = soup.find('div', class_='downloads').a['href']

    # Fill dict with title and img_url
    hemisphere_image_urls.append({
        'title': titles, 
        'img_url': hemis_image
    })
    
    
    print('-----------')
    print(f'added {titles}')
    print('-----------')
    
    
print(f'completed')


# In[95]:


hemisphere_image_urls


# In[ ]:




