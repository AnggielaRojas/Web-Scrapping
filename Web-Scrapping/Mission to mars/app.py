from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars
app = Flask(__name__)

app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_db"
mongo = PyMongo(app)

@app.route("/")
def index():

    mars_data_dict = mongo.db.mars_data_dict.find_one()
    return render_template("index.html", mars_info=mars_data_dict)

@app.route("/scrape")
def scraper():

    mars_data = scrape_mars.scrape_info()

    mars_data_dict = mongo.db.mars_data_dict
    mars_data_dict.update({}, mars_data, upsert=True)
    return redirect("/", code=302)


if __name__ == "__main__":
    app.run(debug=True)
