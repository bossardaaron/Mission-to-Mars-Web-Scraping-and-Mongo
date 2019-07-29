# Import dependencies
from splinter import Browser
import os
from bs4 import BeautifulSoup as bs
from splinter.exceptions import ElementDoesNotExist
import pandas as pd
import requests

def init_browser(): 
# Choose the executable path to driver
	executable_path = {'executable_path': 'chromedriver.exe'}
	return Browser('chrome', headless=True, **executable_path)

mars_dict = {}

#NASA Mars News
def scrape_mars_news():
    try: 

        # Initialize browser 
        browser = init_browser()

		# Visit https://mars.nasa.gov/news/
		url1 = "https://mars.nasa.gov/news/"
		browser.visit(url1)

		# Scrape page into Soup
		html = browser.html
		soup = bs(html, "html.parser")

		# Get the latest news title
		latest_news_title = soup.find('div', class_='content_title').find('a').text

		# Get the paragraph text
		paragraph_text = soup.find('div', class_='article_teaser_body').text

		# Dictionary entry from MARS NEWS
        mars_dict['latest_news_title'] = latest_news_title
        mars_dict['paragraph_text'] = paragraph_text

        return mars_dict

    finally:

        browser.quit()

# JPL MARS SPACE IMAGES -- FEATURED IMAGE
def scrape_mars_image():

    try: 

        # Initialize browser 
        browser = init_browser()

		# Visit https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars and use splinter to navigate the site
		url2 = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
		browser.visit(url2)

		# Scrape page to soup
		html = browser.html
		soup = bs(html, "html.parser")

		# Retrieve background-image url from style tag and assign url string to 'featured_image_url'
		featured_image_url = soup.find('article')['style'].replace('background-image: url(','').replace(');', '')[1:-1]

		# Concatenate website url with scrapped route
		featured_image_url = url2 + featured_image_url

		# Display full link to featured image
		featured_image_url

		mars_dict['featured_image_url'] = featured_image_url 
        
        return mars_dict
    finally:

        browser.quit()

# MARS WEATHER
def scrape_mars_weather():

    try: 

        # Initialize browser 
        browser = init_browser()

		# Visit https://twitter.com/marswxreport?lang=en
		url3 = "https://twitter.com/marswxreport?lang=en"
		browser.visit(url3)

		# Scrape page to soup and use splinter 
		html = browser.html
		soup = bs(html, "html.parser")

		# Get the latest news title
		latest_tweets = soup.find_all('div', class_='js-tweet-text-container')

		# Save the tweet text for the weather report as a variable called `mars_weather` and output tweets based on credentials
		for tweet in latest_tweets:
    		mars_weather = tweet.find('p').text
    		if 'ºF' or 'ºC' or 'Sol' or 'pressure' in mars_weather:
        		print(mars_weather)
        		break
    		else: 
        		pass

        mars_dict['mars_weather'] = mars_weather
     return mars_dict
    finally:

        browser.quit()


# MARS FACTS
def scrape_mars_facts():
		# Visit mars facts webpage at https://space-facts.com/mars/
		url4 = 'http://space-facts.com/mars/'

		# Use panda's `read_html` to parse the url
		mars_facts = pd.read_html(url4)

		# Find the mars facts DataFrame in the list of DataFrames as assign it to `mars_df`
		mars_df = mars_facts[0]

		# Assign the columns `['Characteristics', 'Mars', 'Earth']`
		mars_df.columns = ['Characteristics', 'Mars', 'Earth']

		# Set the index to the `Characteristics` column without row indexing
		mars_df.set_index('Characteristics', inplace= True)

		#vDrop Earth column
		del mars_df['Earth']

		# Use pandas to convert the data to an html table string
		mars_fact_dictionary = mars_df.to_html()

		# Store the mars dataframe in a dictionary, orient='records' makes it list-like
		mars_dict['mars_facts'] = mars_fact_dictionary

		# Display mars_df
		return mars_dict


# MARS HEMISPHERES
def scrape_mars_hemispheres():

    try: 

        # Initialize browser 
        browser = init_browser()
		# Visit https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars to obtain high resolution images for each of Mar's hemispheres and use splinter
		url5 = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
		browser.visit(url5)

		# HTML Object
		html_hemispheres = browser.html

		# Parse HTML with soup
		soup = bs(html_hemispheres, 'html.parser')

		# Find all elements that contain mars hemispheres information
		items = soup.find_all('div', class_='item')

		# Create list for hemisphere urls 
		hemisphere_image_urls = []

		# Store the main_ul 
		hemispheres_main_url = 'https://astrogeology.usgs.gov'

		for i in items: 
    		# Store title
    		title = i.find('h3').text
    
    		# Store link that leads to full image website
    		partial_img_url = i.find('a', class_='itemLink product-item')['href']
    
    		# Visit the link that contains the full image website 
    		browser.visit(hemispheres_main_url + partial_img_url)
    
    		# HTML Object of individual hemisphere information website 
    		partial_img_html = browser.html
    
    		# Parse HTML with Beautiful Soup for every individual hemisphere information website 
    		soup = bs( partial_img_html, 'html.parser')
    
    		# Retrieve full image source 
    		img_url = hemispheres_main_url + soup.find('img', class_='wide-image')['src']
    
    		# Append information into a list of dictionaries 
    		hemisphere_image_urls.append({"title" : title, "img_url" : img_url})
    
		# Display hemisphere_image_urls
		mars_dict['hemisphere_image_urls'] = hemisphere_image_urls

		return mars_dict
    	finally:

        	browser.quit()