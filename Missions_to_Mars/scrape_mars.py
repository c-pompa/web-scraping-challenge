# Dependencies
from bs4 import BeautifulSoup
import requests
import pymongo
from pprint import pprint
from splinter import Browser
from splinter.exceptions import ElementDoesNotExist
import pandas as pd
import time


def init_browser():
    # @NOTE: Replace the path with your actual path to the chromedriver
    executable_path = {
        # "executable_path": "/usr/local/bin/chromedriver"      # MACOS
        "executable_path": "chromedriver.exe"  # WINDOWS: Remember to manually paste the `chromedriver.exe` into the same folder
    }
    return Browser("chrome", **executable_path, headless=False)


def scrape():
    browser = init_browser()

    # Initialize PyMongo to work with MongoDBs
    # Connection string should reference mongodb, localhost, and port 27017
    conn = 'mongodb://localhost:27017'
    # Instantiate at `pymongo.MongoClient()` object with your `conn`
    client = pymongo.MongoClient(conn)

    # Define database and collection
    db = client.missiontomars
    collection = db.articles

    # URL of page to be scraped
    url = 'https://mars.nasa.gov/news/'

    # Retrieve page with the requests module .get() method
    response = requests.get(url)

    # Create BeautifulSoup object; parse the `response.text` with 'lxml'
    soup = BeautifulSoup(response.text, 'lxml')

    ############################
    #### Latest News and Title
    ############################
    # Collect the latest News Title and Paragraph Text. Assign the text to variables that you can reference later.
    # Latest News Title
    news_title = soup.find('div', class_='content_title').a.text.strip()
    # Latest News Title Paragraph
    news_p = soup.find('div', class_='rollover_description_inner').text.strip()
    
    # Quit the browser after scraping
    browser.quit()

    ############################
    #### Featured Image
    ############################
    # Using Splinter, I will grab the features Mars space image from https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars
    executable_path = {'executable_path': 'chromedriver.exe'}
    browser = Browser('chrome', **executable_path, headless=False)

    url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url)

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
                # print('-----------')
                # print(featured_image_url)
                # print('-----------')
                # break

        except:
            print("No image link")
    # Quit the browser after scraping
    browser.quit()

    ############################
    ### Mars Weather
    ############################
    # Get the latest weather data from Mars Weather latest twitter post.
    executable_path = {'executable_path': 'chromedriver.exe'}
    browser = Browser('chrome', **executable_path, headless=False)
    url = 'https://twitter.com/marswxreport?lang=en'
    browser.visit(url)
    time.sleep(5)

    # HTML object
    html = browser.html
    # Instantiate a BeautifulSoup() object with our `html` and the `html5lib` parser
    soup = BeautifulSoup(html, 'html5lib')
    
    # Article holding pic
    article = soup.find('article')

    mars_weather = article.find('div', class_='css-901oao r-hkyrab r-1qd0xha r-a023e6 r-16dba41 r-ad9z0x r-bcqeeo r-bnwqim r-qvutc0').text
    
    # Quit the browser after scraping
    browser.quit()

    ############################
    # ### Mars Facts
    ############################
    # Scrape the table containing facts about the planet including Diameter, Mass, etc.
    url = 'https://space-facts.com/mars/'

    # Use Panda's `read_html` to parse the url
    tables = pd.read_html(url)
    mars_table_df = tables[1]

    # Convert table to HTML in notebooks
    # mars_table_html = mars_table_df.to_html(classes='mars_table')
    mars_table_html = tables[1].to_html().replace('  ', ' ').replace('border="1"','border="0"')

 
    # Save Mars table to an HTML file
    mars_table_df.to_html('mars_table.html')

    ############################
    #### Mars Hemispheres
    ############################
    executable_path = {'executable_path': 'chromedriver.exe'}
    browser = Browser('chrome', **executable_path, headless=False)
    # URL to scrape
    url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url)
    # Assign html to brownser
    html = browser.html
    

    # Instantiate a BeautifulSoup() object with our `html` and the `html5lib` parser
    soup = BeautifulSoup(html, 'html5lib')
    # Find the 'div' containing the 4 hemisphere selections
    hemis = soup.find('div', class_='collapsible results')

    # Find all(each) the 'div' with title descriptions
    hemis_single = hemis.find_all('div', class_='description')

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

    # Complete the full url for each hemisphere webpage
    hemis_url_list = ['https://astrogeology.usgs.gov' + url for url in url_list]

    # Combine both lists for looping
    hemis_and_urls = zip(hemis_list, hemis_url_list)


    # Add data found to hemisphere_image_urls
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

    # Store data in a dictionary
    mars_data = {
        "news_title": news_title,
        "news_p": news_p,
        "featured_image_url": featured_image_url,
        "mars_weather": mars_weather,
        "mars_table_html": mars_table_html, 
        "hemisphere_image_urls": hemisphere_image_urls
        }

    # Quit the browser after scraping
    browser.quit()
    
    # Return results
    return mars_data