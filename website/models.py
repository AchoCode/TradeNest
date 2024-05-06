from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func

class Wallet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    Wallet = db.Column(db.String(150), nullable=True)

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    Title = db.Column(db.String(100), nullable=False)
    Message = db.Column(db.String(300), nullable=False)
    Date = db.Column(db.DateTime(timezone=True), default=func.now())
    
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    First_name = db.Column(db.String(100), nullable=True)    
    Last_name = db.Column(db.String(100), nullable=True)   
    Email = db.Column(db.String(100), unique=True) 
    Phone_number = db.Column(db.String(100), nullable=True)
    Password = db.Column(db.String(100))
    Pin = db.Column(db.String(100), nullable=True)
    Balance = db.Column(db.Float, default=0.00, nullable=True)
    Total_balance = db.Column(db.Float, default=0.00, nullable=True)
    Earnings = db.Column(db.Float, default=0.00, nullable=True)
    Available_balance = db.Column(db.Float, default=0.00, nullable=True)
    Subscription_plan = db.Column(db.String(100), nullable=True)
    is_active = db.Column(db.Boolean, default=True)
    is_verified = db.Column(db.Boolean, default=False)
    Date_joined = db.Column(db.DateTime(timezone=True), default=func.now())
    Role = db.Column(db.String(100), default='user')
    transactions = db.relationship('Transactions')
    notifications = db.relationship('Notifications')

#this model holds deposit, trade, withdrawal transactions
class Transactions(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    Fee = db.Column(db.Float, nullable=True)
    Title = db.Column(db.String(100), nullable=False)
    Amount = db.Column(db.String(100), nullable=False)
    Profit = db.Column(db.String(100), nullable=True)    
    Status = db.Column(db.String(100), nullable=False)
    Wallet = db.Column(db.String(150), nullable=True)
    Duration = db.Column(db.String(100), nullable=True)
    Lot_size = db.Column(db.String(100), nullable=True)
    Date = db.Column(db.DateTime(timezone=True), default=func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

#this model holds deposit, trade, withdrawal transactions info for notification purposes
class Notifications(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    Title = db.Column(db.String(100), nullable=False)
    Amount = db.Column(db.String(100), nullable=False)
    Status = db.Column(db.String(100), nullable=False)
    Date = db.Column(db.DateTime(timezone=True), default=func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))


class Comments(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    User_name = db.Column(db.String(100))   
    Email = db.Column(db.String(100))
    Comment = db.Column(db.String(200))
    Date = db.Column(db.DateTime(timezone=True), default=func.now())





