## Title
Articles for cryptocurrency

##
Installation


Flask

Flask_sqlalchemy

JWT

flaskweb

pip install -U selenium

pip install bs4

##
Usage

Import those libraries


Open a new Firefox browser


Load the page at the given URL


Generate and set SECRET_KEY


Set SQLALCHEMY_DATABASE_URI as postgreSQL or sqlite
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://user:password@localhost:port/database_name'



##
Example

from bs4 import BeautifulSoup as soup
from selenium import webdriver

from flaskblog import db
from flaskblog.models import Users
db.create_all()

url = 'https://coinmarketcap.com/currencies/' + cryptoName + '/news/'
driver = webdriver.Firefox()
driver.get(url)



##
Output
Enter the cryptocurrency name and press button check. If coingecko have information about 
this cryptocurrency , output will new or blogs about cryptocurrency.