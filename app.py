import hashlib
import os
from tempfile import mkdtemp
import os
import psycopg2
from flask_sqlalchemy import SQLAlchemy
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from flask import (Flask, flash, redirect, render_template, request, session,url_for, jsonify)
from book import detail
from helpers import login_required

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///BOOK.sqlite3'
'''
DATABASE_URL = os.environ['DATABASE_URL']
conn = psycopg2.connect(DATABASE_URL, sslmode='require')
cur = conn.cursor()
'''
'''SQLALCHEMY_DATABASE_URI = "mysql+mysqlconnector://{username}:{password}@{hostname}/{databasename}".format(
    username="utk_mish",
    password="Ashu@123",
    hostname="utkmish.mysql.pythonanywhere-services.com",
    databasename="utkmish$book",
)
app.config["SQLALCHEMY_DATABASE_URI"] = SQLALCHEMY_DATABASE_URI
app.config["SQLALCHEMY_POOL_RECYCLE"] = 299
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False'''

db = SQLAlchemy(app)

class book(db.Model):

    __tablename__ = "BOOK"

    username = db.Column(db.String(40), primary_key=True)
    password = db.Column(db.String(40))

class api(db.Model):

    __tablename__ = "API"

    username = db.Column(db.String(40), primary_key=True)
    password = db.Column(db.String(40))
    count = db.Column(db.Integer)

class Review(db.Model):

    __tablename__ = "REVIEW"

    username = db.Column(db.String(40))
    isbn = db.Column(db.String(40), primary_key=True)
    review = db.Column(db.Text(200))
    ratings = db.Column(db.Integer)

db.create_all()

@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

@app.route("/")
@login_required
def index():
    return render_template("index.html")

@app.route("/login", methods=["GET", "POST"])
def login():

    session.clear()

    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        if username == "":
            return render_template("error.html", message="Username field is empty")
        elif password == "":
            return render_template("error.html", message="Password field is empty")
        try:
            #cur.execute("SELECT password from BOOK WHERE username = username")
            #password_db = cur.fetchone()[0]
            password_db = book.query.filter_by(username=username).first().password
            #password_db = db.execute("SELECT password from BOOK WHERE username = :username", {"username": username}).fetchall()[0][0]
        except:
            return render_template("error.html", message="Invaild User")
        if password_db is None:
            return render_template("error.html", message="Invalid username")
        encrypted_password = hashlib.sha256(password.encode('utf-8')).hexdigest()
        if password_db != encrypted_password:
            return render_template("error.html", message="Invalid password")
        flash('You were successfully logged in')
        session["username"] = username
        return redirect(url_for("index"))
    else:
        return render_template("login.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        confirmpassword = request.form.get("confirmpassword")
        if username == "":
            return render_template("error.html", message="Username field is empty")
        elif password == "":
            return render_template("error.html", message="Password field is empty")
        elif confirmpassword == "":
            return render_template("error.html", message="Confirmpassword field is empty")
        elif confirmpassword != password:
            return render_template("error.html", message="Password does not match")
        else:

            encrypted_password = hashlib.sha256(password.encode('utf-8')).hexdigest()
            try:
                user = book(username=username, password =encrypted_password)
                db.session.add(user)
                db.session.commit()
                '''password_db = User.query.filter_by(username=username).first().password
                cur.execute("INSERT INTO BOOK(username, password) VALUES(%s, %s)", (username, encrypted_password))
                conn.commit()'''
            except:
                return render_template("error.html", message="Error username already exists choose another and try again")
                #raise Exception("Error username already exists choose another and try again")
            flash("Successfully Registered!")
            return redirect(url_for("index"))
    else:
        return render_template("register.html")

@app.route("/logout")
def logout():
     # Forget any user_id
    session.clear()
    flash('Successfully Logged Out')
    # Redirect user to login form
    return redirect(url_for("index"))

@app.route("/search", methods=["GET", "POST"])
@login_required
def search():
    if request.method == "POST":
        isbn = request.form.get('isbn')
        title = request.form.get('title')
        author = request.form.get('author')
        obj = detail(isbn=isbn, title=title, author=author)
        res = obj.search(isbn=isbn, title=title, author=author)
        if res:
            flash("Found!")
            return render_template("search.html", list=res)
        else:
            return render_template("error.html", message="No match found")
    else:
        return render_template("search.html")

@app.route("/get_info", methods=["GET", "POST"])
@login_required
def get_info():
    if request.method == "POST":
        isbn = request.form.get("isbn")
        #print(isbn)
        obj = detail(isbn=isbn)
        res = obj.search(isbn=isbn)
        result = obj.get_info(isbn=isbn)
        '''cur.execute("SELECT username FROM REVIEW WHERE isbn=isbn")
        unique_username = cur.fetchone()'''
        #print(unique_username)
        new_username = []
        reviews = Review.query.filter_by(isbn=isbn).all()
        unique_username = []
        if reviews:
            unique_username = reviews.username
        print(unique_username)
        for i in unique_username:
            new_username.append(i)

        if session['username'] not in new_username:
            reviews = Review.query.filter_by(isbn=isbn).all()
            #print(review1.reviews)
            '''cur.execute("SELECT review, ratings, username FROM REVIEW WHERE isbn=isbn")
            reviews = list(cur.fetchone())'''
            return render_template("get_info.html", isbn = res[0][0], title = res[0][1], author = res[0][2], year = res[0][3], review=reviews, check="1", review_count=result["review_count"], average_rating=result["average_score"])
        else:
            reviews = Review.query.filter_by(isbn=isbn).all()
            return render_template("get_info.html", isbn = res[0][0], title = res[0][1], author = res[0][2], year = res[0][3], review=reviews, check="", review_count=result["review_count"], average_rating=result["average_score"])
    else:
        return render_template("get_info.html")

@app.route("/review_insert/<isbn>", methods=["GET", "POST"])
@login_required
def review_insert(isbn):
    if request.method == "POST":
        review = request.form.get("review")
        ratings = request.form.get("Select")
        if ratings == "Ratings":
            ratings = 0
        ratings = int(ratings)
        '''cur.execute("INSERT INTO REVIEW(username, isbn, review, ratings) VALUES(%s, %s, %s, %s)", (session["username"], isbn, review, ratings))
        conn.commit()'''
        reviews = Review(username=session["username"], isbn=isbn, review=review, ratings=ratings)
        db.session.add(reviews)
        db.session.commit()
        flash('Review Inserted Successfully')
        return render_template("success.html", isbn=isbn)
    else:
        return render_template("index.html")

@app.route("/API/<api>/<isbn>")
def api1(isbn, api):
    '''cur.execute("SELECT username FROM API WHERE api=api")
    test_api = cur.fetchone()'''
    test_api = api.query.filter_by(api=api).first().username

    if test_api:
        '''cur.execute("SELECT count FROM API WHERE api=api")
        count = cur.fetchone()'''
        count = api.query.filter_by(api=api).first().count
        c = 0
        if count >= 100:
            return render_template("error.html", message="You have reached your access limit")
        else:
            c = count + 1
        '''cur.execute("UPDATE API SET count = c WHERE api = api")
        conn.commit()'''
        count = api.query.filter_by(api=api).update(dict(count=c))
        db.session.commit()
        obj = detail(isbn=isbn)
        res = obj.get_info(isbn=isbn)
        result = obj.search(isbn=isbn)
        res["title"] = result[0][1]
        res["author"] = result[0][2]
        res["year"] = result[0][3]
        return jsonify(res)
    else:
        return render_template("error.html", message="API key is invalid")

@app.route("/api", methods=["GET", "POST"])
@login_required
def api():
    if request.method == "POST":
        username = session["username"]
        '''cur.execute("SELECT api FROM API WHERE username=username")
        api = cur.fetchone()'''
        api = api.query.filter_by(api=api).first().username
        if api:
            return render_template('api.html', api=api[0][0])
        api = hashlib.sha256(session['username'].encode('utf-8')).hexdigest()
        '''cur.execute("INSERT INTO API(username, api, count) VALUES(%s, %s, %s)", (session["username"], api, 0))
        conn.commit()'''
        api = api(username=session["username"], api=api, count = 0)
        db.session.add(api)
        db.session.commit()
        return render_template('api.html', api=api)
    else:
        flash('Welcome To API Key registration')
        return render_template("api.html")
if __name__ == '__main__':
    app.run()
