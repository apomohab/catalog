import sys
import os
import requests
from flask import make_response
import json
import httplib2
from google.auth.transport import requests as google_requests
from google.oauth2 import id_token
from oauth2client.client import FlowExchangeError
from oauth2client.client import flow_from_clientsecrets
from flask import (
    Flask, render_template,
    request, redirect,
    jsonify, url_for,
    flash, make_response
)
from sqlalchemy import create_engine, asc
from sqlalchemy.orm import sessionmaker
from setup import Base, Catalog, Items, User
from flask import session as login_session
import random
import string
app = Flask(__name__)


# ADD JSON API HERE
@app.route('/catalouges/<int:catalog_id>/menu/JSON')
def CatalogMenuJSON(catalog_id):
    catalog = session.query(Catalog).filter_by(id=catalog_id).one()
    items = session.query(Items).filter_by(
        catalog_id=catalog_id).all()
    return jsonify(Items=[i.serialize for i in items])
# menu and menu_id json


@app.route('/catalouges/<int:catalog_id>/menu/<int:menu_id>/JSON')
def CatalogMenu_id_JSON(catalog_id, menu_id):
    catalog = session.query(Catalog).filter_by(id=catalog_id).one()
    items = session.query(Items).filter_by(
        catalog_id=catalog_id).all()
    return jsonify(Items=[i.serialize for i in items])


# routing for json index
@app.route('/index/JSON/')
def IndexJson():
    catalouges = session.query(Catalog).order_by(asc(Catalog.name))
    return jsonify(Catalog=[catalog.serialize for catalog in catalouges])

# End Point Json here

# Get google client_id for this app from json file


CLIENT_ID = json.loads(

    open('client_secrets.json', 'r').read())['web']['client_id']

engine = create_engine('sqlite:///database.db')
Base.metadata.bind = engine


DBSession = sessionmaker(bind=engine)
session = DBSession()


# login secion
@app.route('/login', methods=['GET', 'POST'])
def showLogin():
    if request.method == 'GET':
        state = ''.join(
            random.choice(
                string.ascii_uppercase +
                string.digits) for x in range(32))
        login_session['state'] = state
        return render_template('login.html', STATE=state)
    if request.method == 'POST':
        try:
            # Check the state variable for extra security
            if login_session['state'] != request.args.get('state'):
                response = make_response(
                    json.dumps('Invalid state parameter.'), 401)
                response.headers['Content-Type'] = 'application/json'
                return response
            # Retrieve the token sent by the client
            token = request.data.decode('utf-8')
            # Request an access tocken from the google api
            idinfo = id_token.verify_oauth2_token(
                token, google_requests.Request(), CLIENT_ID)
            url = (
                'https://oauth2.googleapis.com/tokeninfo?id_token=%s'
                % token)
            h = httplib2.Http()
            result = json.loads(h.request(url, 'GET')[1].decode("utf-8"))
            print(result['aud'])
            # If there was an error in the access token info, abort.
            if result.get('error') is not None:
                response = make_response(json.dumps(result.get('error')), 500)
                response.headers['Content-Type'] = 'application/json'
                return response
            # Verify that the access token is used for the intended user.
            user_google_id = idinfo['sub']
            if result['sub'] != user_google_id:
                response = make_response(
                    json.dumps("Token's user ID doesn't match given user ID."),
                    401)
                response.headers['Content-Type'] = 'application/json'
                return response
            print(result['sub'])
            # Verify that the access token is valid for this app.
            if result['aud'] != CLIENT_ID:
                response = make_response(
                    json.dumps("Token's client ID does not match app's."), 401)
                print("Token's client ID does not match app's.")
                response.headers['Content-Type'] = 'application/json'
                return response
            # Check if the user is already logged in
            stored_access_token = login_session.get('access_token')
            stored_user_google_id = login_session.get('user_google_id')
            if stored_access_token is not None and\
                    user_google_id == stored_user_google_id:
                response = make_response(
                    json.dumps('Current user is already connected.'), 200)
                response.headers['Content-Type'] = 'application/json'
                return response
            # Store the access token in the session for later use.
            login_session['access_token'] = idinfo
            login_session['user_google_id'] = user_google_id
            # Get user info
            login_session['username'] = idinfo['name']
            login_session['picture'] = idinfo['picture']
            login_session['email'] = idinfo['email']
            user_logging_in = session.query(User).filter_by(
                email=login_session['email']).first()
            if user_logging_in:
                login_session['user_id'] = user_logging_in.id
            else:
                login_session['user_id'] = createUser(login_session)
            output = ''
            output += '<h1>Welcome, '
            output += login_session['username']
            output += '!</h1>'
            output += '<img src="'
            output += login_session['picture']
            output += ' " style = "width: 300px; height: 300px;\
                        border-radius:150px;\
                        -webkit-border-radius: 150px;\
                        -moz-border-radius: 150px;"> '
            flash("you are now logged in as %s" % login_session['username'])
            print("done!")
            return output

            return 'Successful'
        except ValueError:
            # Invalid token
            pass

# Logout


@app.route('/logout')
def Logout():
    login_session.clear()
    return redirect('/')


# im add this code
def createUser(login_session):
    newUser = User(
        name=login_session['username'],
        email=login_session['email'],
        picture=login_session['picture'])
    session.add(newUser)
    session.commit()
    user = session.query(User).filter_by(email=login_session['email']).one()
    return user.id

# im add this code


def getUserInfo(user_id):
    user = session.query(User).filter_by(id=user_id).one()
    return user

# im add this code


def getUserID(email):
    try:
        user = session.query(User).filter_by(email=email).one()
        return user.id
    except BaseException:
        return None


# home page
@app.route('/')
@app.route('/index/')
def ShowCatalouges():

    catalouges = session.query(Catalog).order_by(asc(Catalog.name))
    return render_template('index.html', catalouges=catalouges)


# Catalouges items
# Catalouges items
@app.route('/catalouges/<int:catalog_id>/')
@app.route('/catalouges/<int:catalog_id>/menu/')
def CatalogMenu(catalog_id):
    catalog = session.query(Catalog).filter_by(id=catalog_id).one()
    creator = getUserInfo(catalog.user_id)
    items = session.query(Items).filter_by(catalog_id=catalog_id).all()
    if 'username' not in login_session:
        return render_template(
            'publicmenu.html',
            items=items,
            catalog=catalog,
            creator=creator)
    else:
        return render_template(
            'menu.html',
            catalog=catalog,
            items=items,
            creator=creator)


# create new item
@app.route('/catalouges/<int:catalog_id>/new', methods=['GET', 'POST'])
def NewItem(catalog_id):
    if 'username' not in login_session and 'user_id' not in login_session:
        return redirect('/login')
    else:
        if request.method == 'POST':
            addItem = Items(
                title=request.form['title'],
                details=request.form['details'],
                category=request.form['category'],
                catalog_id=catalog_id,
                user_id=login_session['user_id'])
            session.add(addItem)
            session.commit()
            return redirect(url_for('CatalogMenu', catalog_id=catalog_id))
        else:
            return render_template('newcatalog.html', catalog_id=catalog_id)

# edit catalouges


@app.route(
    '/catalouges/<int:catalog_id>/<int:menu_id>/edit',
    methods=[
        'GET',
        'POST'])
def EditCatalouges(catalog_id, menu_id):
    editItem = session.query(Items).filter_by(id=menu_id).one()
    if 'username' not in login_session:
        return redirect('/login')
    if editItem.user_id != login_session['user_id']:
        return "<script>function myFunction() {alert('You\
        are not authorized to edit this item.\
        Please create your own item in order\
        to edit.');}</script><body onload='myFunction()'>"
    if request.method == 'POST':
        if request.form['title']:
            editItem.title = request.form['title']
        if request.form['details']:
            editItem.details = request.form['details']
        if request.form['category']:
            editItem.category = request.form['category']
            session.add(editItem)
            session.commit()
        return redirect(url_for('CatalogMenu', catalog_id=catalog_id))
    else:
        return render_template(
            'edititems.html',
            catalog_id=catalog_id,
            menu_id=menu_id,
            i=editItem)

# delete items


@app.route(
    '/catalouges/<int:catalog_id>/<int:menu_id>/delete',
    methods=[
        'GET',
        'POST'])
def DeleteItems(catalog_id, menu_id):
    itemToDelete = session.query(Items).filter_by(id=menu_id).one()
    if 'username' not in login_session:
        return redirect('/login')
    if itemToDelete.user_id != login_session['user_id']:
        return "<script>function myFunction() {alert('You\
        are not authorized to edit this item.\
        Please create your own item in order\
        to edit.');}</script><body onload='myFunction()'>"
    if request.method == 'POST':
        session.delete(itemToDelete)
        session.commit()
        return redirect(url_for('CatalogMenu', catalog_id=catalog_id))
    else:
        return render_template('delete.html', item=itemToDelete)


if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
app.debug = True
app.run(host='0.0.0.0', port=5000, threaded=False)
