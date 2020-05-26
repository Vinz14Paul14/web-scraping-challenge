from bs4 import BeautifulSoup as bs
from splinter import Browser
import requests
import pymongo
import pandas as pd
import time

def init_browser():
    executable_path = {"executable_path": "/usr/local/bin/chromedriver"}
    return Browser("chrome", **executable_path, headless=False)

    # important_mars_data = {"Mars News Title" : clean_news_title,
    #                     "Mars Title Paragraph" : clean_news_p,
    #                      "Featured Image" : featured_image_url,
    #                       "Mars Facts" : html_facts,
    #                       "Mars Images" : hemisphere_image_urls}
def news_title():
    browser = init_browser()
# URL of page to be scraped
    url = 'https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest'
    browser.visit(url)

    html = browser.html
    soup = bs(html, "html.parser")
# # Retrieve page with the requests module
# response = requests.get(url)
# # Create BeautifulSoup object; parse with 'lxml'
# soup = BeautifulSoup(response.text, 'lxml')
# ### NASA Mars News
    news_title = soup.find('div', class_='content_title')
    clean_news_title = news_title.text.strip()

# issue here
    news_p = soup.find('div', class_='rollover_description_inner')
    clean_news_p = news_p.text.strip()

    browser.quit()
    print(clean_news_title, clean_news_p)
    return clean_news_title, clean_news_p 

def mars_image():
    browser = init_browser()

    url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url) 

    html = browser.html
    soup = bs(html, 'html.parser')


    main_image = soup.find('div', class_='carousel_container').find('div', class_='carousel_items').article['style']
    main_image


    featured_image = main_image.split("('")[1]
    featured_image = featured_image.strip("');")
    featured_image


# issue here with containing code
    base_image_url = 'http://www.jpl.nasa.gov'
    featured_image_url = base_image_url + featured_image

    browser.quit()
    return featured_image_url

def mars_weather():
    browser = init_browser()
    url = 'https://twitter.com/marswxreport?lang=en'
    browser.visit(url)
    time.sleep(5)
    html = browser.html
    soup = bs(html, "html.parser")
    soup.find("article", {"role":"article"})
    
    mars_weather_facts = browser.find_by_xpath('//span[starts-with(text(),"InSight sol")]').first.text.replace('\n', ',')
    browser.quit()
    return mars_weather_facts

def mars_facts():
    browser = init_browser()
# URL of page to be scraped
    url = 'https://space-facts.com/mars/'
    browser.visit(url)
    html = browser.html
# Create BeautifulSoup object; parse with 'lxml'
    soup = bs(html, "html.parser")

    mars_facts = soup.find('table', class_='tablepress tablepress-id-p-mars')

    mars_facts.text

    mars_facts.text

##how to parse into a html string
    tables = pd.read_html(url)
    tables

    df =tables[0]
    df.columns = ['', 'Value']
    df.set_index('', inplace=True)
    df.head(10)

#turn into an html string
    html_facts = df.to_html()
    html_facts.replace('\n', '')
    html_facts

    browser.quit()
    return html_facts 

def mars_hems():
    browser = init_browser()
# first image
    image_url_1 = 'https://astrogeology.usgs.gov/cache/images/f5e372a36edfa389625da6d0cc25d905_cerberus_enhanced.tif_full.jpg'
#first image title
    url = 'https://astrogeology.usgs.gov/search/map/Mars/Viking/cerberus_enhanced'
    browser.visit(url)
    html = browser.html
# Retrieve page with the requests module
    soup = bs(html, "html.parser")
# Create BeautifulSoup object; parse with 'lxml'

    image_title_1 = soup.find('h2', class_='title')
    image_title_1.text


# second image
    image_url_2 = 'https://astrogeology.usgs.gov/cache/images/3778f7b43bbbc89d6e3cfabb3613ba93_schiaparelli_enhanced.tif_full.jpg'
#first image title
    url2 = 'https://astrogeology.usgs.gov/search/map/Mars/Viking/schiaparelli_enhanced'
    browser.visit(url2)
    html2 = browser.html
# Retrieve page with the requests module
    soup = bs(html2, "html.parser")
# Create BeautifulSoup object; parse with 'lxml'

    image_title_2 = soup.find('h2', class_='title')
    image_title_2.text


# third image
    image_url_3 = 'https://astrogeology.usgs.gov/cache/images/555e6403a6ddd7ba16ddb0e471cadcf7_syrtis_major_enhanced.tif_full.jpg'
#first image title
    url3 = 'https://astrogeology.usgs.gov/search/map/Mars/Viking/syrtis_major_enhanced'
    browser.visit(url3)
    html3 = browser.html
# Retrieve page with the requests module
    soup = bs(html3, "html.parser")
# Create BeautifulSoup object; parse with 'lxml

    image_title_3 = soup.find('h2', class_='title')
    image_title_3.text


# fourth image
    image_url_4 = 'https://astrogeology.usgs.gov/cache/images/b3c7c6c9138f57b4756be9b9c43e3a48_valles_marineris_enhanced.tif_full.jpg'
#first image title
    url4 = 'https://astrogeology.usgs.gov/search/map/Mars/Viking/valles_marineris_enhanced'
    browser.visit(url4)
    html4 = browser.html
# Retrieve page with the requests module
    soup = bs(html4, "html.parser")
# Create BeautifulSoup object; parse with 'lxml'

    image_title_4 = soup.find('h2', class_='title')
    image_title_4.text

## need to append all this into a dictionary??
    hemisphere_image_urls = [
        {"title": image_title_1.text, "img_url": image_url_1},  
        {"title": image_title_2.text, "img_url": image_url_2},
        {"title": image_title_3.text, "img_url": image_url_3},
        {"title": image_title_4.text, "img_url": image_url_4},
    ]

    browser.quit()
    return hemisphere_image_urls

def scrape_info():

    important_mars_data = {}
    mars_title, mars_paragraph = news_title()
    important_mars_data["mars_title"] = mars_title
    important_mars_data["mars_paragraph"] = mars_paragraph
    important_mars_data["featured_image_url"] = mars_image()
    important_mars_data["mars_weather_facts"] = mars_weather()
    important_mars_data["mars_facts"] = mars_facts()
    important_mars_data["mars_hems"] = mars_hems()
    return important_mars_data

if __name__ == "__main__":
    print(scrape_info())





# # ### JPL Mars Space Images - Featured Image
# # executable_path = {'executable_path': '/usr/local/bin/chromedriver'}
# # browser = Browser('chrome', **executable_path, headless=False)
#     browser = init_browser()

#     url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
#     browser.visit(url) 

#     html = browser.html
#     soup = bs(html, 'html.parser')


#     main_image = soup.find('div', class_='carousel_container').find('div', class_='carousel_items').article['style']
#     main_image


#     featured_image = main_image.split("('")[1]
#     featured_image = featured_image.strip("');")
#     featured_image


# # issue here with containing code
#     base_image_url = 'http://www.jpl.nasa.gov'
#     featured_image_url = base_image_url + featured_image
#     featured_image_url

#     browser.quit()













# # ### Mars Weather 

# # executable_path = {'executable_path': '/usr/local/bin/chromedriver'}
# # browser = Browser('chrome', **executable_path, headless=False)


# # url = 'https://twitter.com/marswxreport?lang=en'
# # browser.visit(url) 

# # html = browser.html
# # soup = BeautifulSoup(html, 'html.parser')

# # mars_weather = soup.find('p', class_="js-tweet-text")

# # mars_weather.text












# # ### Mars Facts
#     browser = init_browser()
# # URL of page to be scraped
#     url = 'https://space-facts.com/mars/'
#     browser.visit(url)
#     html = browser.html
# # Create BeautifulSoup object; parse with 'lxml'
#     soup = bs(html, "html.parser")

#     mars_facts = soup.find('table', class_='tablepress tablepress-id-p-mars')

#     mars_facts.text

#     mars_facts.text

# ##how to parse into a html string
#     tables = pd.read_html(url)
#     tables

#     df =tables[0]
#     df.columns = ['', 'Value']
#     df.set_index('', inplace=True)
#     df.head(10)

# #turn into an html string
#     html_facts = df.to_html()
#     html_facts.replace('\n', '')
#     html_facts

#     browser.quit()









# # ### Mars Hemispheres

#     browser = init_browser()
# # first image
#     image_url_1 = 'https://astrogeology.usgs.gov/cache/images/f5e372a36edfa389625da6d0cc25d905_cerberus_enhanced.tif_full.jpg'
# #first image title
#     url = 'https://astrogeology.usgs.gov/search/map/Mars/Viking/cerberus_enhanced'
#     browser.visit(url)
#     html = browser.html
# # Retrieve page with the requests module
#     soup = bs(html, "html.parser")
# # Create BeautifulSoup object; parse with 'lxml'

#     image_title_1 = soup.find('h2', class_='title')
#     image_title_1.text


# # second image
#     image_url_2 = 'https://astrogeology.usgs.gov/cache/images/3778f7b43bbbc89d6e3cfabb3613ba93_schiaparelli_enhanced.tif_full.jpg'
# #first image title
#     url2 = 'https://astrogeology.usgs.gov/search/map/Mars/Viking/schiaparelli_enhanced'
#     browser.visit(url2)
#     html2 = browser.html
# # Retrieve page with the requests module
#     soup = bs(html2, "html.parser")
# # Create BeautifulSoup object; parse with 'lxml'

#     image_title_2 = soup.find('h2', class_='title')
#     image_title_2.text


# # third image
#     image_url_3 = 'https://astrogeology.usgs.gov/cache/images/555e6403a6ddd7ba16ddb0e471cadcf7_syrtis_major_enhanced.tif_full.jpg'
# #first image title
#     url3 = 'https://astrogeology.usgs.gov/search/map/Mars/Viking/syrtis_major_enhanced'
#     browser.visit(url3)
#     html3 = browser.html
# # Retrieve page with the requests module
#     soup = bs(html3, "html.parser")
# # Create BeautifulSoup object; parse with 'lxml

#     image_title_3 = soup.find('h2', class_='title')
#     image_title_3.text


# # fourth image
#     image_url_4 = 'https://astrogeology.usgs.gov/cache/images/b3c7c6c9138f57b4756be9b9c43e3a48_valles_marineris_enhanced.tif_full.jpg'
# #first image title
#     url4 = 'https://astrogeology.usgs.gov/search/map/Mars/Viking/valles_marineris_enhanced'
#     browser.visit(url4)
#     html4 = browser.html
# # Retrieve page with the requests module
#     soup = bs(html4, "html.parser")
# # Create BeautifulSoup object; parse with 'lxml'

#     image_title_4 = soup.find('h2', class_='title')
#     image_title_4.text

# ## need to append all this into a dictionary??
#     hemisphere_image_urls = [
#         {"title": image_title_1.text, "img_url": image_url_1},  
#         {"title": image_title_2.text, "img_url": image_url_2},
#         {"title": image_title_3.text, "img_url": image_url_3},
#         {"title": image_title_4.text, "img_url": image_url_4},
#     ]
#     hemisphere_image_urls


#     important_mars_data = {"Mars News Title" : clean_news_title,
#                         "Mars Title Paragraph" : clean_news_p,
#                          "Featured Image" : featured_image_url,
#                           "Mars Facts" : html_facts,
#                           "Mars Images" : hemisphere_image_urls}

#     browser.quit()

#     return important_mars_data
