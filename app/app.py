from flask import Flask, redirect, render_template
from flask_pymongo import PyMongo
import scrap_mars

app = Flask(__name__)
app.config['MONGO_URI'] = 'mongodb://localhost:27017/mars_app'
mongo = PyMongo(app)


@app.route('/')
def index():
    mars = mongo.db.mars.find_one()
    return render_template('index.html', mars=mars)


@app.route('/scrape')
def scrape():
    mars = mongo.db.mars
    mars_data = scrap_mars.scrape()
    mars.update({}, mars_data, upsert=True)
    print('Scraping successful!')
    return redirect('/', code=302)


if __name__ == '__main__':
    app.run(debug=True)


# to check in mongo
# > use mars_app
# > db.mars.find().pretty()