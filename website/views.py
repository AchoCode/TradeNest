from flask import Blueprint, render_template, request, flash, redirect, url_for, jsonify, session
from flask_login import login_required, current_user
from .newmodels import NewComments, NewUser, NewTransactions, NewNotifications
from .functions import commit, secure_wallet
from . import db
import bcrypt
import requests
import json

#status messages to keep it consistent
SUCCESS = 'Success'
DENIED = 'Denied'
OPEN = 'Open'
CLOSED = 'Closed'
PENDING = 'Pending'

views = Blueprint('views', __name__ )

@views.route('/', methods = ['GET', 'POST'])
def home():
 return render_template('home.html', usr=current_user)

@views.route('/contact', methods = ['GET', 'POST'])
def contact():
    if request.method == 'POST':
        
        #get comment form details
        username = request.form.get('usrname')
        email = request.form.get('email')
        comment = request.form.get('text')

        #query database if user exists
        usr = NewUser.query.filter_by(Email=email).first()
        if not usr:
          flash('Please Sign Up to drop a comment......', category='error')
        else:
           #if user exists, add the comment to the database
           new_comment = NewComments(NewUser_name=username, Email=email, Comment=comment)
           db.session.add(new_comment)
           db.session.commit()
           flash('Comment Posted successfully....', category='success')
          
    return render_template('contact.html', usr=current_user)

@views.route('/profile', methods = ['GET', 'POST'])
@login_required
def profile():
    # usr_id = current_user.id
    # new_trade1 = NewTransactions(Title='Trade', Amount='150', Status='Open', user_id=usr_id)
    # new_trade2 = NewTransactions(Title='Trade', Amount='120', Status='Closed', user_id=usr_id)
    # new_trade3 = NewTransactions(Title='Trade', Amount='190', Status='Pending', user_id=usr_id)
    # new_trade4 = NewTransactions(Title='Trade', Amount='400', Status='Closed', user_id=usr_id)

    # db.session.add_all([new_trade1,new_trade2,new_trade3,new_trade4])
    # db.session.commit()
    # print('added to database')

    #query database for Trade transactions associated with the leader
    Trade = NewTransactions.query.filter_by(Title='Trade', user_id=current_user.id).all()

    #get all closed transactions and append to the list
    Closed_trades =[]
    for x in Trade:
       if x.Status == CLOSED:
          Closed_trades.append(x)

    #get all Open transactions and append to the list
    Open_trades =[]
    for x in Trade:
       if x.Status == OPEN:
          Open_trades.append(x)

    #get all Pending transactions and append to the list
    Pending_trades =[]
    for x in Trade:
       if x.Status == PENDING:
          Pending_trades.append(x)

    Number_of_trades = len(Trade)
    return render_template('Myprofile.html', usr=current_user, Trade=Trade, Number_of_trades=Number_of_trades,
                           Closed_trades=Closed_trades, Number_of_Closed_trades=len(Closed_trades), 
                           Number_of_Open_trades=len(Open_trades), Number_of_Pending_trades=len(Pending_trades))  

@views.route('/deposit', methods=['GET', 'POST'])
@login_required
def deposit():
    #load data from json

    data = json.loads(request.data)
    usr_id = data['usrId']
    
    #query database to find user information
    usr = NewUser.query.get(usr_id)
    message = f'{usr.First_name} with email {usr.Email} is trying to make a deposit'
    if usr:
        print(message)
    return render_template('deposit.html', usr=current_user)

@views.route('/notifications', methods = ['GET', 'POST'])
@login_required
def notifications():
    #query database for all notifications associated with the user

    # usr_id = current_user.id
    # usr = NewUser.query.get(usr_id)
    # current_bal = usr.Available_balance
    # usr.Available_balance = 2000.00 + current_bal
    # usr.Balance = 2000.00
    # usr.Total_balance = 500.00
    # db.session.commit()
    # print(SUCCESS)

    # new_trade1 = NewNotifications(Title='Savings', Amount='Enhance your trading with savings', Status='Success', user_id=usr_id)
    # new_trade2 = NewNotifications(Title='Withdrawal', Amount='200', Status='success', user_id=usr_id)
    # new_trade3 = NewNotifications(Title='Trade', Amount='300', Status='Success', user_id=usr_id)
    # new_trade4 = NewNotifications(Title='Withdrawal', Amount='500', Status=DENIED, user_id=usr_id)

    # db.session.add_all([new_trade2,new_trade3,new_trade4])
    # db.session.commit()
    # print('added to database')

    notifications = NewNotifications.query.filter_by(user_id=current_user.id).all()
    return render_template('notifications.html', usr=current_user, notifications=notifications)

@views.route('/history', methods = ['GET', 'POST'])
@login_required
def Transaction_history():
    #query database for transactions related to the user
    Record = NewTransactions.query.filter_by(user_id=current_user.id).all()
    return render_template('transaction history.html', usr=current_user, record=Record)

@views.route('/trade', methods = ['GET', 'POST'])
@login_required
def trade():
    #query database for open trades related to the user
    Trade = NewTransactions.query.filter_by(Title='Trade', Status='Open', user_id=current_user.id).all()
    return render_template('trade.html', usr=current_user, number_of_trades = len(Trade))

@views.route('/withdraw-request', methods = ['GET', 'POST'])
@login_required
def withdraw_request():
    if request.method == 'POST':

        #get form data
        amount = request.form.get('amount')
        Wallet_address = request.form.get('wallet-address')

        #python checks
        if amount.isdigit():
           #change amount to an integer
           Amt = float(amount)
        elif Wallet_address == '':
            flash('Please enter a valid wallet address')
        else:
           flash('Please enter a valid number')

        session['amount'] = Amt
        session['wallet-address'] = Wallet_address    
        return redirect(url_for('views.withdraw'))   
           
    return render_template('Withdraw-request.html', usr=current_user)

@views.route('/withdraw', methods = ['GET', 'POST'])
@login_required
def withdraw():
        
    #get the session data
    Amt = session['amount']
    wallet_address = session['wallet-address']
    wallet = secure_wallet(wallet_address)
    fee_charge = 0.05 * Amt
    Balance = Amt + fee_charge

    if request.method == 'POST':
        user_id = current_user.id
        
        #get password from form data
        password = request.form.get('pwd')

        #query database to get user and user info
        usr = NewUser.query.get(user_id)
        avail_bal = float(usr.Available_balance)
        result_bal = avail_bal - Balance

        if bcrypt.checkpw(password.encode('utf-8'), usr.Password):
            #check if amt is greater than avail_bal and deny the withdrawal
            if Amt > avail_bal:
                new_transaction = NewTransactions(Title='Withdrawal', Amount=Amt, Status=DENIED, Wallet=wallet_address, user_id=user_id)
                new_notification = NewNotifications(Title='Withdrawal', Amount=Amt, Status=DENIED, user_id=user_id)
                commit(new_transaction, new_notification)
                flash('Transaction is being processed')
                return redirect(url_for('views.profile'))
            elif result_bal < 0:
                new_transaction = NewTransactions(Title='Withdrawal', Amount=Amt, Status=DENIED, Wallet=wallet_address, user_id=user_id)
                new_notification = NewNotifications(Title='Withdrawal', Amount=Amt, Status=DENIED, user_id=user_id)
                commit(new_transaction, new_notification)
                flash('Transaction is being processed')
                return redirect(url_for('views.profile'))
            #check if amt is equal to avail_bal or if it less than it and accept the transaction and update available balance
            elif Amt == avail_bal:
                new_transaction = NewTransactions(Title='Withdrawal', Amount=Amt, Status=SUCCESS, Wallet=wallet_address, user_id=user_id)
                new_notification = NewNotifications(Title='Withdrawal', Amount=Amt, Status=SUCCESS, user_id=user_id)
                new_bal = avail_bal - Amt - fee_charge
                usr.Available_balance = new_bal
                commit(new_transaction, new_notification)
                flash('Transaction is being processed')
                return redirect(url_for('views.profile'))
            else:
                new_transaction = NewTransactions(Title='Withdrawal', Amount=Amt, Status=SUCCESS, Wallet=wallet_address, user_id=user_id)
                new_notification = NewNotifications(Title='Withdrawal', Amount=Amt, Status=SUCCESS, user_id=user_id)
                new_bal = avail_bal - Amt - fee_charge
                usr.Available_balance = new_bal
                commit(new_transaction, new_notification)
                flash('Transaction is being processed')
                return redirect(url_for('views.profile'))
        else:
            flash('Incorrect Password! Try again.', category='error')
       
    return render_template('Withdraw.html', usr=current_user, amount=Amt, Wallet_address=wallet, fee=fee_charge )


@views.route('/settings', methods = ['GET', 'POST'])
@login_required
def settings():
    return render_template('settings.html', usr=current_user)