from flask import Flask, render_template, redirect 
from flask_pymongo import PyMongo
import scrape_mars
import os

# Create an instance of Flask
app = Flask(__name__)

# Use PyMongo to establish Mongo connection
mongo = PyMongo(app, uri="mongodb://localhost:27017/mars_app")

# Route to render index.html template using data from Mongo
@app.route("/")
def home():

    # Find one record of data from the mongo database
    mars_dict = mongo.db.mars_dict.find_one()

    # Return template and data
    return render_template("index.html", mars_dict=mars_dict)

 # Route that will trigger the scrape function
@app.route("/scrape")
def scrape():

    # Run the scrape function
    mars_dict = mongo.db.mars_dict {
    "s_mars_news" : scrape_mars.latest_news_title(),
    "s_mars_image" : scrape_mars.featured_image_url(),
    "s_mars_fact" : scrape_mars.mars_fact_dictionary(),
    "s_mars_weather" : scrape_mars.mars_weather(),
    "s_mars_hemispheres" : scrape_mars.hemisphere_image_urls(),
    "s_mars_paragraph": scrape_mars.paragraph_text() }
    mars_dict.update({}, mars_scraped, upsert=True)

    # Redirect back to home page
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)