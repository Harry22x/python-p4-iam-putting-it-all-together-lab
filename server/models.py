from sqlalchemy.orm import validates
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy_serializer import SerializerMixin

from config import db, bcrypt



class User(db.Model, SerializerMixin):
    __tablename__ = 'users'
    serialize_rules = ('-recipes.user', '-_password_hash',)

    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String, unique = True, nullable = False)
    image_url = db.Column(db.String)
    bio = db.Column(db.String)
    _password_hash = db.Column(db.String, nullable = True)  

    recipes = db.relationship('Recipe', back_populates= 'user')


    @validates('username')
    def validate_user_name(self, key, user_name):
        existing_user_names = [user.username for user in User.query.all()]  
        if user_name in existing_user_names:
            raise ValueError(f"Username '{user_name}' already exists.")
        elif user_name == "":
            raise ValueError("Username cannot be empty.")
        return user_name


    @hybrid_property
    def password_hash(self):
        raise AttributeError("Password hash cannot be accessed")

    @password_hash.setter
    def password_hash(self, password):
         password_hash = bcrypt.generate_password_hash(password.encode('utf-8'))
         self._password_hash = password_hash.decode("utf-8")

    
    def authenticate(self,password):
        return bcrypt.check_password_hash(self._password_hash,password.encode('utf-8'))

    

class Recipe(db.Model, SerializerMixin):
    __tablename__ = 'recipes'
    
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String, nullable=False)
    instructions = db.Column(db.String, nullable=False)
    minutes_to_complete = db.Column(db.Integer)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable = True)  
    user = db.relationship("User", back_populates = "recipes")

    @validates('title','instructions')
    def validate_title_instructions(self, key, value):
        if key == 'title':
            if value == "":
                raise ValueError("Title cannot be empty.")
            return value
        elif key == 'instructions':
            if len(value) < 51:
                raise ValueError("Instructions must be more than 50 characters.")
            return value