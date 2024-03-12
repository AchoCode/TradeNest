from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func

class NewPost(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    Title = db.Column(db.String(100), nullable=False)
    Message = db.Column(db.String(300), nullable=False)
    Date = db.Column(db.DateTime(timezone=True), default=func.now())

class NewAdmin(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    Email = db.Column(db.String(100), unique=True)
    Wallet = db.Column(db.String(150), nullable=True)
    Password = db.Column(db.String(100))
    
class NewUser(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    First_name = db.Column(db.String(100))    
    Last_name = db.Column(db.String(100))   
    Email = db.Column(db.String(100), unique=True) 
    Phone_number = db.Column(db.String(100))
    Password = db.Column(db.String(100))
    Pin = db.Column(db.String(100), default='0000')
    Balance = db.Column(db.Float, default=0.00)
    Total_balance = db.Column(db.Float, default=0.00)
    Earnings = db.Column(db.Float, default=0.00)
    Available_balance = db.Column(db.Float, default=0.00)
    Subscription_plan = db.Column(db.String(100))
    is_active = db.Column(db.Boolean, default=True)
    Date_joined = db.Column(db.DateTime(timezone=True), default=func.now())
    transactions = db.relationship('NewTransactions')
    notifications = db.relationship('NewNotifications')

#this model holds deposit, trade, withdrawal transactions
class NewTransactions(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    Title = db.Column(db.String(100), nullable=False)
    Amount = db.Column(db.String(100), nullable=False)
    Profit = db.Column(db.String(100), nullable=True)    
    Status = db.Column(db.String(100), nullable=False)
    Wallet = db.Column(db.String(150), nullable=True)
    Date = db.Column(db.DateTime(timezone=True), default=func.now())
    Fee = db.Column(db.Float, nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('new_user.id'))

#this model holds deposit, trade, withdrawal transactions info for notification purposes
class NewNotifications(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    Title = db.Column(db.String(100), nullable=False)
    Amount = db.Column(db.String(100), nullable=False)
    Status = db.Column(db.String(100), nullable=False)
    Date = db.Column(db.DateTime(timezone=True), default=func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('new_user.id'))

class NewComments(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    User_name = db.Column(db.String(100))   
    Email = db.Column(db.String(100))
    Comment = db.Column(db.String(200))
    Date = db.Column(db.DateTime(timezone=True), default=func.now())





