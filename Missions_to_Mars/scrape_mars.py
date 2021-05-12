from splinter import Browser
from bs4 import BeautifulSoup as bs
from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import pandas as pd
from webdriver_manager.chrome import ChromeDriverManager

def scrape():
    # Set up Splinter
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)

    #URL of what we are scraping
    url = 'https://redplanetscience.com/'
    browser.visit(url)

    #HTML Object
    html = browser.html
    # Parse HTML with Beautiful Soup
    soup = BeautifulSoup(html, 'html.parser')

    #Retrieve title, class="content_title"
    news_title = soup.find_all('div', class_='content_title')[0].text

    #Retrieve paragraph, class="article_teaser_body"
    paragraph_content = soup.find_all('div', class_='article_teaser_body')[0].text
    
    #MARS IMAGE

    #URL of what we are scraping
    sim_url = 'https://spaceimages-mars.com/'
    browser.visit(sim_url)

    #HTML Object
    html = browser.html
    # Parse HTML with Beautiful Soup
    soup = BeautifulSoup(html, 'html.parser')

    # Retrieve image url
    image_url=soup.find_all('img')

    relative_image_path = soup.find_all('img')[1]["src"]
    featured_image_url = sim_url + relative_image_path

    #Use Pandas to read Mars table
    mars_df=pd.read_html('https://galaxyfacts-mars.com/')[0]

    mars_df.columns=["Description","Mars","Earth"]


    #Use Pandas to convert the data to a HTML table string
    mars_df=mars_df.to_html()
    
    mars_df.replace('\n','')

    #MARS HEMISPHERES

    #URL of what we are scraping
    mh_url = 'https://marshemispheres.com/'
    browser.visit(mh_url)
    #HTML Object
    html = browser.html
    # Parse HTML with Beautiful Soup
    soup = BeautifulSoup(html, 'html.parser')

    #Create dictionary
    hemisphere_img_urls=[]

    results = soup.find("div", class_="result-list")
    hemispheres = results.find_all("div", class_="item")

    #Iterate through list and append dictionary with URL string and hemisphere title to a list

    for hemisphere in hemispheres:
        #Find title and image URL
        title=hemisphere.find("h3").text
        trailing_link=hemisphere.find("a")["href"]
        image_link = mh_url+trailing_link
        browser.visit(image_link)
        html=browser.html
        soup = BeautifulSoup(html, 'html.parser')
        #Image specific page
        downloads=soup.find("div", class_="downloads")
        image_url=downloads.find("a")["href"]
        hemisphere_img_urls.append({"title": title, "img_url": image_url})

    #Store data in a ditionary
    mars = {
        "news_title":news_title,
        "news":paragraph_content,
        "featured_image_url":featured_image_url,
        "mars_table":mars_df,
        "hemisphere_images":hemisphere_img_urls
    }

    # Close the browser after scraping
    browser.quit()

    # Return results
    return mars
