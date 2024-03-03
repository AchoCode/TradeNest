from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func
#TODO: create a post schema, TITLE, MESSAGE, DATE and ID for admin post

class Admin(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    Email = db.Column(db.String(100), unique=True) 
    Password = db.Column(db.String(100))
    
#TODO: add earnings column and a pin
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    First_name = db.Column(db.String(100))    
    Last_name = db.Column(db.String(100))   
    Email = db.Column(db.String(100), unique=True) 
    Phone_number = db.Column(db.String(100))
    Password = db.Column(db.String(100))
    Balance = db.Column(db.Float, default=0.00)
    Total_balance = db.Column(db.Float, default=0.00)
    Available_balance = db.Column(db.Float, default=0.00)
    Subscription_plan = db.Column(db.String(100))
    Date_joined = db.Column(db.DateTime(timezone=True), default=func.now())
    transactions = db.relationship('Transactions')
    notifications = db.relationship('Notifications')

#this model holds deposit, trade, withdrawal transactions
#TODO: add a date column and  fee column
class Transactions(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    Title = db.Column(db.String(100), nullable=False)
    Amount = db.Column(db.String(100), nullable=False)
    Profit = db.Column(db.String(100), nullable=True)    
    Status = db.Column(db.String(100), nullable=False)
    Wallet = db.Column(db.String(150), nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

#this model holds deposit, trade, withdrawal transactions info for notification purposes
#TODO: remove the message column. it will be in posts, edit the html template as well.
class Notifications(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    Title = db.Column(db.String(100), nullable=False)
    Amount = db.Column(db.String(100), nullable=False)
    Status = db.Column(db.String(100), nullable=False)
    Date = db.Column(db.DateTime(timezone=True), default=func.now())
    Message = db.Column(db.String(300), nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

# TODO: add a date column
class Comments(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    User_name = db.Column(db.String(100))   
    Email = db.Column(db.String(100))
    Comment = db.Column(db.String(200))





