from flask import Flask, render_template, redirect
from flask_table import Table, Col
from flask_pymongo import PyMongo
import scrape_mars

# Create an instance of Flask
app = Flask(__name__)

# Use PyMongo to establish Mongo connection
mongo = PyMongo(app, uri="mongodb://localhost:27017/mars_data")
information = mongo.db.information  #THIS IS OUR COLLECTION IN MONGODB

# Route to render index.html template using data from Mongo
@app.route("/")
def home():

    # `.find_one()` record of data from the `desination` collection in our mongo database 
    information_data = information.find_one()

    # Return template and data
    return render_template("index.html", info=information_data)


# Route that will trigger the scrape function
@app.route("/scrape")
def scrape():

    # Run the scrape function and save the results to a variable
    # Call the `.scrape()` function of `scrape_mars`
    mars_data = scrape_mars.scrape()

    # Update the Mongo database using update, passing in your `mars_data` and upsert=True
    information.update({}, mars_data, upsert=True)

    # Redirect back to home page
    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)
