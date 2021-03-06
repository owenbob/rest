"""/rest_api basetest.py"""
import os
import json
from flask import Flask, request
from datetime import datetime

from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash
from decouple import config
from unittest import TestCase

from recipes import app, db
from recipes.models import User, Recipe, Category
from recipes.models import save, delete


class BaseTestCase(TestCase):
    app.config['SQLALCHEMY_DATABASE_URI'] = config('TEST_DB') or os.environ['TEST_DB']
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    def setUp(self):
        self.client = app.test_client()
        db.drop_all()
        db.create_all()

        #test users for login
        self.user2={'username':'geom','password':'12345'}

        # create and add a test user        
        password = '12345'
        self.user_test={'user_id':'5xxxxx', 'name':'Geofrey', 'username':'geom', 'email':'geom2@gmail.com', 'password':password}
        password_hash = generate_password_hash(password, method='sha256')
        test_user = User(user_id='5xxxxx', name='Geofrey', username='geof', email='geom@gmail.com', password=password_hash)
        save(test_user)
        
        # create and add test category
        self.cat_test={'cat_id':'5xxxxxx','cat_name':'Generall','cat_desc':'General recipes','created_by':'geom'}
        test_category = Category(cat_id='5xxxxx', cat_name='General', cat_desc='General recpes', create_date=datetime.now(), created_by='geof', modified_date=datetime.now())
        save(test_category)

        # create and add test recipe
        self.recipe_test={'recipe_id':'5xxxxx','title':'Recipe One and two','category':'General','ingredients':'Ingredient one and two','steps':'step 1','created_by':'geom', 'status':'public', 'upvotes':0}
        test_recipe = Recipe(recipe_id='5xxxxx', title='Recipe One', category='General', ingredients='Ingredient one and two', steps='step 1', create_date=datetime.now(), created_by='geof', modified_date=datetime.now(), status='public', upvotes=0)
        save(test_recipe)

        """ Generate authentication token"""
        self.user = {"username": "geof", "password": password}
        response = self.client.post(
            '/auth/login', data=json.dumps(self.user),
            headers={'Content-Type': 'application/json'})
        
        response_data = json.loads(response.data)
        token = response_data['token']

        self.headers = {'x-access-token': token,
                        'Content-Type': 'application/json',
                        }

    def tearDown(self):
        db.session.remove()
        db.drop_all()

if __name__ == "__main__":
    unittest.main()