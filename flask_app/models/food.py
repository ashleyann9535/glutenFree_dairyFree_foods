from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import user
from flask_app import app
from flask import flash, session


# make class, class methods with SQL, and logic
class Food:
    db = 'gf_df_foods'

    def __init__(self, data):
        self.id = data['id']
        self.name = data['name']
        self.description = data['description']
        self.location = data['location']
        self.gluten_free = data['gluten_free']
        self.dairy_free = data['dairy_free']
        self.user_id = data['user_id']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.creator = None


#Create 
    @classmethod
    def create_food(cls, data):
        if not cls.validate_food(data):
            return False
        query = """
        INSERT INTO foods(name, description, location, gluten_free, dairy_free, user_id)
        VALUES (%(name)s, %(description)s, %(location)s, %(gluten_free)s, %(dairy_free)s, %(user_id)s)
        ;"""

        food_id = connectToMySQL(cls.db).query_db(query, data)

        return food_id

#Read 
    @classmethod
    def view_all_foods(cls):
        query = """
        SELECT * FROM foods
        JOIN users
        ON foods.user_id = users.id
        ;"""

        result = connectToMySQL(cls.db).query_db(query)
        all_foods = []

        if not result:
            return result
        for one_food in result:
            new_food = cls(one_food)
            this_food = {
                'id' : one_food['users.id'],
                'first_name' : one_food['first_name'],
                'last_name' : one_food['last_name'],
                'email' : one_food['email'],
                'password' : one_food['password'],
                'created_at' : one_food['users.created_at'],
                'updated_at' : one_food['users.updated_at']
            }

            new_food.creator = user.User(this_food)
            all_foods.append(new_food)

        return all_foods


#Update 


#Delete 

#Validate 
    @staticmethod
    def validate_food(data):
        is_valid = True
        if not data['name']:
            flash('Please give a name to the food', 'create_food')
            is_valid = False
        if not data['location']:
            flash('Please add the place the food can be found', 'create_food')
            is_valid = False
        if not data['description']:
            flash('Please let us about the food', 'create_food')
            is_valid = False
        if not data['gluten_free']:
            flash('Is the food gluten free?', 'create_food')
            is_valid = False
        if not data['dairy_free']:
            flash('Is the food dairy free?', 'create_food')
            is_valid = False
        return is_valid