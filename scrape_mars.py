# Import Dependecies 
from bs4 import BeautifulSoup as bs
from splinter import Browser
import pandas as pd 
import requests

# Browser initialization
def init_browser():
    executable_path = {'executable_path': 'chromedriver.exe'}
    return Browser('chrome', **executable_path, headless=False)

# Global dictionary to be imported into Mongo
mars_info = {}

# NASA Mars News function
def scrape_mars_news():
    try: 
        # Initialize browser 
        browser = init_browser()

        # Visit first NASA news website and build html to parse
        url = 'https://mars.nasa.gov/news/'
        browser.visit(url)

        html = browser.html

        soup = bs(html, 'html.parser')

        # Get last news elements, title and paragraph
        news_title = soup.find('div', class_='content_title').find('a').text
        news_p = soup.find('div', class_='article_teaser_body').text

        # Dictionary entry from MARS News
        mars_info['news_title'] = news_title
        mars_info['news_paragraph'] = news_p

        return mars_info

    finally:

        browser.quit()

# JPL Mars Space Images
def scrape_mars_image():

    try: 

        # Initialize browser 
        browser = init_browser()

        # Visit JPL images website and buil html to parse
        image_url_featured = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
        browser.visit(image_url_featured)

        html_image = browser.html

        soup_image = bs(html_image, 'html.parser')

        # Get featured image url from style tag
        featured_image_url  = soup_image.find('article')['style'].replace('background-image: url(','').replace(');', '')[1:-1]

        # Build new website with the featured image
        main_url = 'https://www.jpl.nasa.gov'
        featured_image_url = main_url + featured_image_url

        # Dictionary entry from JPL Mars Images
        mars_info['featured_image_url'] = featured_image_url 
        
        return mars_info

    finally:

        browser.quit()

#  Mars Weather
def scrape_mars_weather():

    try: 

        # Initialize browser 
        browser = init_browser()

        # Visit Mars Weather Twitter and buil html to parse
        weather_url = 'https://twitter.com/marswxreport?lang=en'
        browser.visit(weather_url)
 
        html_weather = browser.html

        soup_weather = bs(html_weather, 'html.parser')

        # Get all tags that contains tweets
        latest_tweets = soup_weather.find_all('div', class_='js-tweet-text-container')

        # Loop the tweets to find the one that contains weather info and break the loop
        for tweet in latest_tweets: 
            weather_tweet = tweet.find('p').text
            if 'Sol' and 'pressure' in weather_tweet:
                print(weather_tweet)
                break
            else: 
                pass

        # Dictionary entry from Mars Weather
        mars_info['weather_tweet'] = weather_tweet
        
        return mars_info
    finally:

        browser.quit()

# Mars Facts
def scrape_mars_facts():

    # Visit Mars facts url
    facts_url = 'http://space-facts.com/mars/'

    # Use Panda's `read_html` to parse the url
    mars_facts = pd.read_html(facts_url)

    # clean table and create data frame with column names
    mars_df = mars_facts[0]
    mars_df.columns = ['Description','Value']
    mars_df.set_index('Description', inplace=True)

    # Crate html code
    mars_df.to_html()
    # Create a dictionary to use latter
    data = mars_df.to_dict(orient='records')

    # Save html code to folder Assets
    data = mars_df.to_html()

    # Dictionary entry from MARS FACTS
    mars_info['mars_facts'] = data

    return mars_info

def scrape_mars_hemispheres():

    try: 

        # Initialize browser 
        browser = init_browser()

        # Visit hemispheres website through splinter module 
        hemispheres_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
        browser.visit(hemispheres_url)

        # HTML Object
        html_hemispheres = browser.html

        # Parse HTML with Beautiful Soup
        soup = bs(html_hemispheres, 'html.parser')

        # Retreive all items that contain mars hemispheres information
        items = soup.find_all('div', class_='item')

        # Create empty list for hemisphere urls 
        hiu = []

        # Store the main_ul 
        hemispheres_main_url = 'https://astrogeology.usgs.gov' 

        # Loop through the items previously stored
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
            
            # Append the retreived information into a list of dictionaries 
            hiu.append({"title" : title, "img_url" : img_url})

        mars_info['hiu'] = hiu

        
        # Return mars_data dictionary 

        return mars_info
    finally:

        browser.quit()
