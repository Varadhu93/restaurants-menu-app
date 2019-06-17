"""
Created on Thu May 19 15:15:28 2019

@author: S.R.Varadharam-pc
"""

from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem

app = Flask(__name__)
engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

# Fake Restaurants
# restaurant = {'name': 'The CRUDdy Crab', 'id': '1'}
# restaurants = [{'name': 'The CRUDdy Crab', 'id': '1'}, {'name': 'Blue Burgers', 'id': '2'}, {'name': 'Taco Hut', 'id': '3'}]

# Fake Menu Items
# items = [{'name': 'Cheese Pizza', 'description': 'made with fresh cheese', 'price': '$5.99', 'course' : 'Entree', 'id': '1'}, {'name': 'Chocolate Cake', 'description': 'made with Dutch Chocolate', 'price': '$3.99', 'course': 'Dessert', 'id': '2'}, {'name': 'Caesar Salad', 'description': 'with fresh organic vegetables', 'price': '$5.99', 'course': 'Entree', 'id': '3'}, {'name': 'Iced Tea', 'description': 'with lemon', 'price': '$.99', 'course': 'Beverage', 'id': '4'}, {'name': 'Spinach Dip', 'description': 'creamy dip with fresh spinach', 'price': '$1.99', 'course': 'Appetizer', 'id': '5'} ]
# item = {'name': 'Cheese Pizza', 'description': 'made with fresh cheese', 'price': '$5.99', 'course' : 'Entree'}


# CODE TO SHOW RESTAURANTS HOME PAGE
@app.route('/', methods=['GET', 'POST'])
@app.route('/restaurants', methods=['GET', 'POST'])
@app.route('/restaurants/', methods=['GET', 'POST'])
def showRestaurants():
    if request.method == 'GET':
        restaurants = session.query(Restaurant).all()
        return render_template('restaurants.html', restaurants=restaurants)


# CODE TO ADD NEW RESTAURANT
@app.route('/restaurants/new', methods=['GET', 'POST'])
def newRestaurant():
    if request.method == 'POST':
        newRestaurant = Restaurant(name=request.form['name'])
        session.add(newRestaurant)
        session.commit()
        flash("New Restaurant created!")
        return redirect(url_for('showRestaurants'))
    else:
        return render_template('newRestaurant.html', methods=['GET', 'POST'])


# CODE TO EDIT A RESTAURANT
@app.route('/restaurants/<int:restaurant_id>/edit', methods=['GET', 'POST'])
def editRestaurant(restaurant_id):
    editedRestaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
    if request.method == 'POST':
        if request.form['name']:
            editedRestaurant.name = request.form['name']
        session.add(editedRestaurant)
        session.commit()
        flash("Restaurant successfully edited!")
        return redirect(url_for('showRestaurants'))
    else:
        return render_template('editRestaurant.html', restaurant_id=restaurant_id, item=editedRestaurant)


# CODE TO DELETE A RESTAURANT
@app.route('/restaurants/<int:restaurant_id>/delete', methods=['GET', 'POST'])
def deleteRestaurant(restaurant_id):
    deleteRestaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
    if request.method == 'POST':
        session.delete(deleteRestaurant)
        session.commit()
        flash("Restaurant has been deleted!")
        return redirect(url_for('showRestaurants'))
    else:
        return render_template('deleteRestaurant.html', restaurant_id=restaurant_id, item=deleteRestaurant)


# CODE TO SHOW MENU OF RESTAURANT
@app.route('/restaurants/<int:restaurant_id>/menu')
def showMenu(restaurant_id):
    restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
    menuItems = session.query(MenuItem).filter_by(restaurant_id=restaurant_id).all()
    return render_template('menu.html', restaurant_id=restaurant_id, items=menuItems)


# CODE TO ADD NEW MENU
@app.route('/restaurants/<int:restaurant_id>/menu/new', methods=['GET','POST'])
def newMenu(restaurant_id):
    if request.method == 'POST':
        newItem = MenuItem(name=request.form['name'], description=request.form['description'], price=request.form['price'], restaurant_id=restaurant_id)
        session.add(newItem)
        session.commit()
        flash("New Menu Item added")
        return redirect(url_for('showMenu', restaurant_id=restaurant_id))
    else:
        return render_template('newmenuitem.html', restaurant_id=restaurant_id)


# CODE TO EDIT A MENU OF RESTAURANT
@app.route('/restaurants/<int:restaurant_id>/menu/<int:menu_id>/edit', methods=['GET', 'POST'])
def editMenu(restaurant_id, menu_id):
    editedMenuItem = session.query(MenuItem).filter_by(id=menu_id).one()
    if request.method == 'POST':
        if request.form['name']:
            editedMenuItem.name = request.form['name']
        if request.form['description']:
            editedMenuItem.description = request.form['description']
        if request.form['price']:
            editedMenuItem.price = request.form['price']
        session.add(editedMenuItem)
        session.commit()
        flash("Menu Item edited!")
        return redirect(url_for('showMenu', restaurant_id=restaurant_id))
    else:
        return render_template('editmenuitem.html', item=editedMenuItem, restaurant_id=restaurant_id, menu_id=menu_id)


# CODE TO DEELTE A MENU
@app.route('/restaurants/<int:restaurant_id>/menu/<int:menu_id>/delete', methods=['GET', 'POST'])
def deleteMenu(restaurant_id, menu_id):
    deleteMenuItem = session.query(MenuItem).filter_by(id=menu_id).one()
    if request.method == 'POST':
        session.delete(deleteMenuItem)
        session.commit()
        flash("Menu Item has been deleted!")
        return redirect(url_for('showMenu', restaurant_id=restaurant_id))
    else:
        return render_template('deletemenuitem.html', restaurant_id=restaurant_id, menu_id=menu_id, item=deleteMenuItem)


# CODE TO ADD JSON TO RESTAURANTS
@app.route('/restaurants/JSON')
def restaurantJSON():
    restaurantsJSON = session.query(Restaurant).all()
    return jsonify(Restaurant=[i.serialize for i in restaurantsJSON])


# CODE TO ADD JSON TO MENU
@app.route('/restaurants/<int:restaurant_id>/menu/JSON')
def menuJSON(restaurant_id):
    restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
    items = session.query(MenuItem).filter_by(restaurant_id=restaurant.id).all()
    return jsonify(MenuItem=[i.serialize for i in items])


if __name__ == '__main__':
    app.secret_key = 'super_secretkey'
    app.run(debug=True, use_reloader=False, host='0.0.0.0', port=5000)
