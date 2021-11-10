from flask import render_template
from bs4 import BeautifulSoup
from selenium import webdriver
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SECRET_KEY'] = 'thisismysecretkey'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:9666@localhost:5432/postgres2'
db = SQLAlchemy(app)


@app.route('/', methods=['GET', 'POST'])
@app.route('/coin', methods=['GET', 'POST'])
def coin():
    form = CheckCoinForm()
    name = (str(form.name.data)).lower()

    if form.validate_on_submit():
        driver = webdriver.Firefox()
        driver.get(f'https://coinmarketcap.com/currencies/{name}/news/')
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        headers = soup.findAll("h3", {"class": "sc-1q9q90x-0", "class": "gEZmSc"})
        paragraphs = soup.findAll("p", {"class": "sc-1eb5slv-0", "class": "svowul-3", "class": "ddtKCV"})
        boo = False
        for row in db.session.query(Articles).filter_by(crypto_name=name):
            if row.crypto_name == name:
                boo = True
        for i in range(0, len(headers)):
            header = headers[i].text.strip()
            paragraph = paragraphs[i].text.strip()
            if len(header) > 0 and len(paragraph) > 0 and not boo:
                db.session.add(Articles(f'{name}', f'{header}', f'{paragraph}'))
                db.session.commit()

    headArray = []
    paraArray = []
    for row in db.session.query(Articles).filter_by(crypto_name=name):
        headArray.append(row.header)
        paraArray.append(row.paragraph)

    return render_template('coin.html', form=form, header=headArray, paragraph=paraArray)


class CheckCoinForm(FlaskForm):
    name = StringField('Coin')
    check = SubmitField('Check')


class Articles(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    crypto_name = db.Column(db.String(20), nullable=False)
    header = db.Column(db.Text, nullable=False)
    paragraph = db.Column(db.Text, nullable=False)

    def __init__(self, crypto_name, header, paragraph):
        self.crypto_name = crypto_name
        self.header = header
        self.paragraph = paragraph


if __name__ == '__main__':
    app.run(debug=True)