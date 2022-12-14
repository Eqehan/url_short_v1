#projenin calisan ilk hali

from flask import Flask, render_template, request, redirect, url_for 
from flask_sqlalchemy import SQLAlchemy
import random
import string
import os

app = Flask(__name__)
                    #db configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///urls.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
                     #db start
db = SQLAlchemy(app)
                     #defining db elements
class Urls(db.Model):
    id_ = db.Column("id_", db.Integer, primary_key=True)
    long= db.Column("long", db.String())
    short= db.Column("short", db.String(3))

    def __init__(self, long,short):
        self.long=long
        self.short=short 
                    #creating db table
@app.before_first_request
def create_tables():
    db.create_all() 
                    #short url choose and create function
def shorten_url():
    letters = string.ascii_lowercase + string.ascii_uppercase
    while True:
        rand_letters = random.choices(letters, k=3)
        rand_letters = "".join(rand_letters)
        short_url = Urls.query.filter_by(short=rand_letters).first()
        if not short_url:
            return rand_letters

@app.route('/', methods=['POST', 'GET'])
def home():
    if request.method == "POST":
        url_received = request.form["nm"]   #check if url in db
        found_url = Urls.query.filter_by(long=url_received).first()
        
        if found_url:                       #return short url, if found
            return redirect(url_for("display_short_url",url=found_url.short))
        
        else:                               #create short url, if not found
            short_url = shorten_url()
            new_url = Urls(url_received, short_url)
            db.session.add(new_url)
            db.session.commit()
            return redirect(url_for("display_short_url", url=short_url))

    else:
        return render_template("home.html")

@app.route('/display/<url>')
def display_short_url(url):
    return render_template('shorturl.html',short_url_display=url)

@app.route('/<short_url>')
def redirection(short_url):
    long_url = Urls.query.filter_by(short=short_url).first()
    if long_url:
        return redirect(long_url.long)
    else:
        return f'<h1> Url does not exist <h1>' 

@app.route('/recep')
def hello_egehan():
    return "Recep abi geç kaldim kusuruma bakma lütfen :/"

if __name__ == '__main__':
    app.run(port=5000, debug=True)

    # auth eklencek, jw token, 