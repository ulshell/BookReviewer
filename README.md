# BookReviewer
A web application for searching books with their isbn number, name or author of book. User can view the reviews of others for the book and can himself review the book. This app has one external feature of api which can be used by other developers to intergrate the information recieved from server in their application without any under level implementation.

## Login Page

>For login of users into web app implementing secure login with password encryption.

![alt login](https://github.com/ulshell/BookReviewer/blob/master/static/login.png)

## Register Page

>For registeration of new user into web app implementing secure login with password encryption.

![alt register](https://github.com/ulshell/BookReviewer/blob/master/static/register.png)

## User's Home Page

>Home page of user for searching different scree_names of twitter account that are not private.

![alt home](https://github.com/ulshell/BookReviewer/blob/master/static/Index.png)

## Tweet Analysis Page

>Page describing whole analysis of atmost 200 recent tweets (positive , negative or neutral)

![alt analysis](https://github.com/ulshell/BookReviewer/blob/master/static/analysis.png)

# How to run :-

>For installing all required python3 libraries

->$ pip3 install --user -r requirements.txt

>Goto your Twitter account create an app and get API_KEY and API_SECRET to run app.

-> $export API_KEY=your api key

-> $export API_SECRET=your api secret key

>Provide the FLASK_APP environment variable

-> $export FLASK_APP=application.py

>Run Flask Application

-> $python3 -m flask run

>Open http link provided in terminal. 
