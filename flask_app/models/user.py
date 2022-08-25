# ---------------------IMPORTS---------------------------------------------------------------------
from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import flash
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 

# from flask_app.models import                   # MAKE SURE TO IMPORT OTHER MODELS

# -------------------------------------------------------------------------------------------------
DATABASE = 'gwei-check-users'                                        # MAKE SURE TO REPLACE WITH DATABASE NAME
# -------------------------------------------------------------------------------------------------

class User:
    def __init__( self , data ):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.email_alert = data['email_alert']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

# SAVE ALERT STATUS ON USER CHANGE
    @classmethod
    def set_alert(cls, data):
        query = "UPDATE users SET email_alert = %(email_alert)s WHERE id = %(id)s;"
        return connectToMySQL(DATABASE).query_db(query, data)

# GET USERS WHERE SET_ALERT = TRUE
    @classmethod
    def get_users_with_alerts(cls):
        query = "SELECT email FROM users WHERE email_alert = 1"
        results = connectToMySQL(DATABASE).query_db(query)
        print(results)
        return results

# SET EMAIL ALERT TO FALSE POST EMAIL BEING SENT
    @classmethod
    def set_alert_to_false(cls, data):
        query = "UPDATE users SET email_alert = 0 WHERE email = %(email)s;"
        return connectToMySQL(DATABASE).query_db(query, data)

# -------------------------------------------------------------------------------------------------
# GENERAL SQL QUERIES
# -------------------------------------------------------------------------------------------------
    # ! GET ALL USERS FROM DB
    @classmethod
    def get_all(cls):
        query = "SELECT * FROM users;"
        results = connectToMySQL(DATABASE).query_db(query)
        users = []
        for user in results:
            users.append( cls(user) )
        return users

    # ! GET ONE USER FROM DB
    @classmethod
    def get_one(cls, data):
        query = "SELECT * FROM users WHERE id = %(id)s;"
        result = connectToMySQL(DATABASE).query_db(query, data)
        user = User(result[0])
        return user

    # ! CREATE USER IN DB                                   # MAKE SURE TO UPDATE COLUMN NAMES BELOW IN SQL STMT
    @classmethod
    def save(cls, data):
        # Set default for email_alert to 0?
        query = "INSERT INTO users (first_name, last_name, email, password) VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password)s);"
        return connectToMySQL(DATABASE).query_db(query, data)

    # ! UPDATE
    @classmethod
    def edit_user(cls, data):
        query = "UPDATE users SET first_name = %(first_name)s, last_name = %(last_name)s, email = %(email)s WHERE id = %(id)s;"
        return connectToMySQL(DATABASE).query_db(query, data)

    # ! DELETE
    @classmethod
    def delete_user(cls, data):
        query = "DELETE FROM users WHERE id = %(id)s;"
        return connectToMySQL(DATABASE).query_db(query, data)

# -------------------------------------------------------------------------------------------------
# LOGIN AND REGISTRATION
# -------------------------------------------------------------------------------------------------
    # ! GET ONE USER FROM DB BY EMAIL                       # LOGIN FUNCTION - CHECKS DB FOR EMAIL
    @classmethod
    def get_one_with_email(cls,data) -> object or bool:
        query = "SELECT * FROM users WHERE email = %(email)s;"
        result = connectToMySQL(DATABASE).query_db(query, data)
        print(result)
        if len(result) < 1:
            return False
        else:
            user = User(result[0])
        return user

    # ! VALIDATE REGISTRATION INPUT                         # REGISTRATION FUNCTION - CHECKS INPUTS
    @staticmethod
    def validate_user(user:dict) -> bool:
        is_valid = True
        if len(user['first_name']) < 3:
            is_valid = False
            flash("First name must be at least 3 characters.")
        if len(user['last_name']) < 3:
            is_valid = False
            flash("Last name must be at least 3 characters.")
        if not EMAIL_REGEX.match(user['email']): 
            flash("Invalid email address.")
            is_valid = False
        if 'password' in user:
            if len(user['password']) < 8:
                is_valid = False
                flash("Password must be at least 8 characters.")
            if user['password'] != user['password_confirmation']:
                flash("Passwords must match.")
                is_valid = False
            if len(user['password']) < 3:
                flash("Password must be at least 3 characters.")
                is_valid = False
        return is_valid