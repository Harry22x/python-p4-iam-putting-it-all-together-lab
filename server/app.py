#!/usr/bin/env python3

from flask import request, session
from flask_restful import Resource
from sqlalchemy.exc import IntegrityError

from config import app, db, api
from models import User, Recipe

class Signup(Resource):
    pass
    def post(self):
        data = request.get_json()
        
        
        errors = {}
        
       
        if not data.get('username'):
            errors['username'] = 'Username is required'
        
        
        if not data.get('password'):
            errors['password'] = 'Password is required'
        elif len(data['password']) < 6:
            errors['password'] = 'Password must be at least 6 characters'
        
       
        if errors:
            return {'errors': errors}, 422
        
        try:
            new_user = User(
                username=data['username'],
                image_url=data.get('image_url'),
                bio=data.get('bio')
            )
           
            new_user.password_hash = data['password']
            
           
            db.session.add(new_user)
            db.session.commit()
        except ValueError as e:
            
            return {'errors': {'username': str(e)}}, 422
        except Exception as e:
            db.session.rollback()
            return {'errors': {'database': 'Error saving user'}}, 422
        
      
        session['user_id'] = new_user.id
        
       
        return new_user.to_dict(), 201

class CheckSession(Resource):
    pass
    def get(self):
      
        user_id = session.get('user_id')
        
        if not user_id:
            return {'error': 'Unauthorized'}, 401
        
       
        user = User.query.filter_by(id=user_id).first()
              
     
        return user.to_dict(), 200
class Login(Resource):
    def post(self):
        data = request.get_json()
        
       
        user = User.query.filter_by(username=data.get('username')).first()
        
      
        if user and user.authenticate(data.get('password', '')):
            
            session['user_id'] = user.id
            
           
            return user.to_dict(), 200
        
       
        return {'error': 'Invalid username or password'}, 401

class Logout(Resource):
    pass
    def delete(self):
       
        if not session['user_id'] :
            return {'error': 'Unauthorized'}, 401
        
       
        session.pop('user_id', None)
        
       
        return '', 204

class RecipeIndex(Resource):
    pass
    def get(self):
           
            if not session['user_id']:
                return {'error': 'Unauthorized'}, 401
            
          
            recipes = Recipe.query.all()
            
           
            recipes_data = [recipe.to_dict()for recipe in recipes]
            
            return recipes_data, 200
    def post(self):
        if not session['user_id']:
            return {'error': 'Unauthorized'}, 401
        
        data = request.get_json()
        
     
        errors = {}
        if not data.get('title'):
            errors['title'] = 'Title is required'
        if not data.get('instructions'):
            errors['instructions'] = 'Instructions are required'
        if not data.get('minutes_to_complete'):
            errors['minutes_to_complete'] = 'Minutes to complete is required'
        
        if errors:
            return {'errors': errors}, 422
        
        try:
            new_recipe = Recipe(
                title=data['title'],
                instructions=data['instructions'],
                minutes_to_complete=data['minutes_to_complete'],
                user_id=session['user_id']
            )
            
            db.session.add(new_recipe)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            return {'errors': {'database': 'Error saving recipe'}}, 422
        
        return new_recipe.to_dict(), 201

api.add_resource(Signup, '/signup', endpoint='signup')
api.add_resource(CheckSession, '/check_session', endpoint='check_session')
api.add_resource(Login, '/login', endpoint='login')
api.add_resource(Logout, '/logout', endpoint='logout')
api.add_resource(RecipeIndex, '/recipes', endpoint='recipes')


if __name__ == '__main__':
    app.run(port=5555, debug=True)