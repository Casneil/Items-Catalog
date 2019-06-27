#!/usr/bin/env python3

from flask import Flask, render_template, url_for, flash,\
    redirect, jsonify, request
from datetime import datetime
from flask_bcrypt import Bcrypt
from forms import RegistrationForm, LoginForm
from sqlalchemy import create_engine, asc
from sqlalchemy.orm import sessionmaker
from flask import session as login_session
from catalog_setup import Base, User, Mall, Items
import random
import string
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import httplib2
import json
from flask import make_response
import requests
from googleapiclient import discovery
import httplib2
from oauth2client import client
import google.oauth2.credentials
from authlib.client import OAuth2Session
import functools
import os


CLIENT_ID = json.loads(
    open('client_secrets.json', 'r').read())['web']['client_id']
APPLICATION_NAME = "Catalog"


app = Flask(__name__)
app.secret_key = '4580bfba153d29c6159ac8708425cc06'
engine = create_engine('sqlite:///catalog.db',
                       connect_args={'check_same_thread': False})

bcrypt = Bcrypt(app)


Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()


# Create anti-forgery state token
@app.route('/glogin')
def showLogin():
    if 'username' in login_session:
        return redirect(url_for('showShops'))
    state = ''.join(random.choice(string.ascii_uppercase + string.digits)
                    for x in range(32))
    login_session['state'] = state
    # return "The current session state is %s" % login_session['state']
    return render_template('g_login.html', STATE=state)


# Creating Google Sign-in #
@app.route('/gconnect', methods=['POST', 'GET'])
def gconnect():
    # Validate state token
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    # Obtain authorization code
    code = request.data

    try:
        # Upgrade the authorization code into a credentials object
        oauth_flow = flow_from_clientsecrets('client_secrets.json', scope='')
        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(code)
    except FlowExchangeError:
        response = make_response(
            json.dumps('Failed to upgrade the authorization code.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Check that the access token is valid.
    access_token = credentials.access_token
    url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s'
           % access_token)
    h = httplib2.Http()
    result = json.loads(h.request(url, 'GET')[1])
    # If there was an error in the access token info, abort.
    if result.get('error') is not None:
        response = make_response(json.dumps(result.get('error')), 500)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is used for the intended user.
    gplus_id = credentials.id_token['sub']
    if result['user_id'] != gplus_id:
        response = make_response(
            json.dumps("Token's user ID doesn't match given user ID."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is valid for this app.
    if result['issued_to'] != CLIENT_ID:
        response = make_response(
            json.dumps("Token's client ID does not match app's."), 401)
        print ("Token's client ID does not match app's.")
        response.headers['Content-Type'] = 'application/json'
        return response

    stored_access_token = login_session.get('access_token')
    stored_gplus_id = login_session.get('gplus_id')
    if stored_access_token is not None and gplus_id == stored_gplus_id:
        response = make_response(json.dumps(
            'Current user isalready connected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Store the access token in the session for later use.
    login_session['access_token'] = credentials.access_token
    login_session['gplus_id'] = gplus_id

    # Get user info
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': credentials.access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)

    data = answer.json()

    login_session['username'] = data['name']
    login_session['picture'] = data['picture']
    login_session['email'] = data['email']

    output = ''
    output += '<h1>Welcome, '
    output += login_session['username']
    output += '!</h1>'
    output += '<img src="'
    output += login_session['picture']
    output += ' " style = "width: 300px; height: 300px;border-radius:\
     150px;-webkit-border-radius: 150px;-moz-border-radius: 150px;"> '
    flash("you are now logged in as %s" % login_session['username'])
    print ("Welcome")
    next_page = request.args.get('next')
    return output


# Creating a User  Maybe need to delete #
def newUser(login_session):
    newUser = User(name=login_session['username'], email=login_session[
        'email'], picture=login_session['picture'])
    session.add(newUser)
    session.commit()
    user = session.query(User).filter_by(email=login_session['email']).one()
    return user.id


def getUserInfo(user_id):
    user = session.query(User).filter_by(id=user_id).one()
    return user


def getUserID(email):
    try:
        user = session.query(User).filter_by(email=email).one()
        return user.id
    except:
        return None


# JSON APIs to view Shop Information
@app.route('/shop/all/JSON')
def allShopsJSON():
    shops = session.query(Mall).all()
    return jsonify(shops=[s.serialize for s in shops])


@app.route('/shop/items/all/JSON')
def allItemsJSON():
    items = session.query(Items).all()
    return jsonify(items=[i.serialize for i in items])


@app.route('/shop/<int:mall_id>/item/JSON')
def shopItemsJSON(mall_id):
    mall = session.query(Mall).filter_by(id=mall_id).one()
    items = session.query(Items).filter_by(
        mall_id=mall_id).all()
    return jsonify(Items=[i.serialize for i in items])


# Displayes Shops #
@app.route('/')
@app.route('/home')
def showShops():
    shops = session.query(Mall).order_by(asc(Mall.department))
    if 'username' not in login_session:
        return render_template('publicMall.html', shops=shops)
    else:
        return render_template('home.html', shops=shops)


# Displays Items within a shop #
@app.route('/item/<int:mall_id>/')
@app.route('/item/<int:mall_id>/items/')
def showItems(mall_id):
    shops = session.query(Mall).filter_by(id=mall_id).all()
    items = session.query(Items).filter_by(mall_id=mall_id).all()
    return render_template('items.html', title='All Items',
                           items=items, shops=shops,)


# Show links to edit/delete or create a new Mall #
@app.route('/home/new/', methods=['GET', 'POST'])
def newMall():
    if 'username' not in login_session:
        return redirect('/glogin')
    if request.method == 'POST':
        global newMall
        newMall = Mall(department=request.form
                       ['department'], description=request.form['description'],
                       user_id=login_session['username'])
        session.add(newMall)
        session.commit()
        flash('Shop %s Successfully Created' % newMall.department)
        return redirect(url_for('showShops'))
    else:
        return render_template('newMall.html', newMall=newMall)


# Edit a Shop #
@app.route('/home/<int:mall_id>/edit/', methods=['GET', 'POST'])
def editedMall(mall_id):
    if 'username' not in login_session:
        return redirect('/glogin')
    editedMall = session.query(Mall).filter_by(id=mall_id).one()
    if editedMall.user_id != login_session['username']:
        return "<script>function myFunction()\
        {alert('Error!. Please create your own Shop in order to edit.')\
        ;}</script><body onload='myFunction()'>"
    if request.method == 'POST':
        if request.form['department']:
            editedMall.department = request.form['department']
        if request.form['description']:
            editedMall.description = request.form['description']
        session.add(editedMall)
        session.commit()
        flash('Successfully Edited!: %s' % editedMall.department)
        return redirect(url_for('showShops'))
    else:
        return render_template('editMall.html', mall_id=mall_id,
                               mall=editedMall)


@app.route('/home/<int:mall_id>/delete/', methods=['GET', 'POST'])
def deleteMall(mall_id):
    if 'username' not in login_session:
        return redirect('/glogin')
    mallToDelete = session.query(Mall).filter_by(id=mall_id).one()
    if mallToDelete.user_id != login_session['username']:
        return "<script>function myFunction() {alert('Error!.\
            Please create your own Shopin order to delete.');}\
            </script><body onload='myFunction()'>"
    if request.method == 'POST':
        session.delete(mallToDelete)
        session.commit()
        return redirect(url_for('showItems', mall_id=mall_id))
    else:
        return render_template('deleteMall.html', mall_id=mall_id,
                               mall=mallToDelete)


# Show links to create/edit/delete or create a new Item
@app.route('/item/<int:mall_id>/item/new', methods=['GET', 'POST'])
def newItem(mall_id):
    if 'username' not in login_session:
        return redirect('/glogin')
    newItem = session.query(Mall).filter_by(id=mall_id).one()
    if newItem.user_id != login_session['username']:
        return "<script>function myFunction() {alert('Error!. Please\
        create your own Shop in order to add\
        items.');}</script><body onload='myFunction()'>"
    # global newItem
    if request.method == 'POST':
        newItem = Items(name=request.form['name'], description=request.form
                        ['description'], price=request.form['price'],
                        mall_id=mall_id, user_id=newItem.user_id)
        session.add(newItem)
        session.commit()
        flash('New Item %s Item added!' % (newItem.name))
        return redirect(url_for('showItems', mall_id=mall_id))
    else:
        return render_template('createNewItem.html',
                               newItem=newItem, mall_id=mall_id)


@app.route('/item/<int:mall_id>/item/<int:item_id>/edit',
           methods=['GET', 'POST'])
def editedItem(mall_id, item_id):
    if 'username' not in login_session:
        return redirect('/glogin')
    editedItem = session.query(Items).filter_by(id=item_id).one()
    shops = session.query(Mall).filter_by(id=mall_id).all()
    if editedItem.user_id != login_session['username']:
        return "<script>function myFunction() {alert('You are not authorized to\
        edit this item. Please create your own Shop in order to edit items.\
        ');}</script><body onload='myFunction()'>"
    if request.method == 'POST':
        if request.form['name']:
            editedItem.name = request.form['name']
        if request.form['description']:
            editedMall.description = request.form['description']
        if request.form['price']:
            editedItem.name = request.form['price']
        session.add(editedItem)
        session.commit()
        flash('Successfully Edited!: %s' % editedItem.name)
        return redirect(url_for('showItems', mall_id=mall_id))
    else:
        return render_template('editItem.html', item=editedItem,
                               item_id=item_id, mall_id=mall_id)


@app.route('/item/<int:mall_id>/item/<int:item_id>/delete',
           methods=['GET', 'POST'])
def deleteItem(mall_id, item_id):
    if 'username' not in login_session:
        return redirect('/glogin')
        editedItem = session.query(Items).filter_by(id=item_id).all()
    shops = session.query(Mall).filter_by(id=mall_id).all()
    itemToDelete = session.query(Items).filter_by(id=item_id).one()
    if itemToDelete.user_id != login_session['username']:
        return "<script>function myFunction() {alert('You are not authorized to delete\
        this item. Please create your own Shop in order to delete items.\
        ');}</script><body onload='myFunction()'>"
    if request.method == 'POST':
        session.delete(itemToDelete)
        session.commit()
        flash('Item %s Item Deleted!' % (itemToDelete.name))
        return redirect(url_for('showItems', mall_id=mall_id))
    else:
        return render_template('deleteItem.html', title='Delete Item',
                               itemToDelete=itemToDelete, mall_id=mall_id,
                               item_id=item_id)


# About Page #
@app.route('/about/')
def about():
    return render_template('about.html', title='About Page')


# Account Page #
@app.route('/account')
def account():
    if 'username' in login_session:
        user = session.query(User).filter_by().all()
        picture = login_session['picture']
        return render_template('account.html', title='Account', user=user,
                               picture=picture)
    else:
        flash('Youre not authorized to view this page. Please\
            login to do so')
        return redirect(url_for('showLogin'))


# Logout #
@app.route('/logout')
def logout():
        # Only disconnect a connected user.
    access_token = login_session.get('access_token')
    if access_token is None:
        response = make_response(
            json.dumps('Current user not connected.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    url = 'https://accounts.google.com/o/oauth2/revoke?token=%s' % access_token
    h = httplib2.Http()
    result = h.request(url, 'GET')[0]

    if result['status'] == '200':
        # Reset the user's sesson.
        del login_session['access_token']
        del login_session['gplus_id']
        del login_session['username']
        del login_session['email']
        del login_session['picture']
        response = make_response(json.dumps('Successfully disconnected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        return response
    else:
        # For whatever reason, the given token was invalid.
        response = make_response(
            json.dumps('Failed to revoke token for given user.', 400))
        response.headers['Content-Type'] = 'application/json'
        return response


if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
