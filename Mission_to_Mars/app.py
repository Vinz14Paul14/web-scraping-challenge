import numpy as np
import datetime as dt
import sqlalchemy
import scrape_mars
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask_pymongo import PyMongo

from flask import Flask, render_template, redirect

app = Flask(__name__)

# mongo = PyMongo(app, uri="mongodb://localhost:27017/mars_app")
# put the dictionary scrape script here
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_app"
mongo = PyMongo(app)



@app.route("/")
def home():
    # home page
    mars_info = mongo.db.mars_data.find_one()

    # Return template and data
    return render_template("index.html", mars_info=mars_info)




@app.route("/scrape")
def scrape():
    
    mars_info = mongo.db.mars_data

    mars_data = scrape_mars.scrape_info()
    
    # Update the Mongo database using update and upsert=True
    mars_info.update({}, mars_data, upsert=True)

    # Redirect back to home page
    return redirect("/", code=302)



if __name__ == '__main__':
    app.run(debug=True)