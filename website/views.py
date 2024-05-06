from flask import Blueprint, render_template, request, flash, redirect, url_for, session, jsonify
from flask_login import login_required, current_user
from flask_mail import Message
from .models import *
from .functions import secure_wallet
from . import db, mail
from .auth import s
import bcrypt
import json
import time
#status messages to keep it consistent
SUCCESS = 'Success'
DENIED = 'Denied'
OPEN = 'Open'
CLOSED = 'Closed'
PENDING = 'Pending'
ACTIVE_PAGE = None

views = Blueprint('views', __name__ )
@views.route('/email', methods = ['GET', 'POST'])
def email():
    return render_template('withdrawal-email.html', usr='current_user')


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
        usr = User.query.filter_by(Email=email).first()
        if not usr:
          flash('Please Sign Up to drop a comment......', category='error')
        else:
           #if user exists, add the comment to the database
           new_comment = Comments(User_name=username, Email=email, Comment=comment)
           db.session.add(new_comment)
           db.session.commit()
           flash('Comment Posted successfully....', category='success')
          
    return render_template('contact.html', usr=current_user)

@views.route('/profile', methods = ['GET', 'POST'])
@login_required
def profile():
    notices = Notifications.query.filter_by(user_id=current_user.id).all()
    number_of_notices = len(notices)

    ACTIVE_PAGE = 'dashboard'
    #query database for Trade transactions associated with the leader
    Trade = Transactions.query.filter_by(Title='Trade', user_id=current_user.id).all()

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

    return render_template('Myprofile.html', usr=current_user, active_page=ACTIVE_PAGE, Trade=Trade, Number_of_trades=Number_of_trades,
                           Closed_trades=Closed_trades, Number_of_Closed_trades=len(Closed_trades), number_of_notices=number_of_notices,
                           Number_of_Open_trades=len(Open_trades), Number_of_Pending_trades=len(Pending_trades))  

@views.route('/deposit', methods=['GET', 'POST'])
@login_required
def deposit():
    notices = Notifications.query.filter_by(user_id=current_user.id).all()
    number_of_notices = len(notices)

    ACTIVE_PAGE = 'deposit'
    btc_wallet = Wallet.query.filter_by(id='1').first()
    if request.method == "POST":
        #load data from json
        data = json.loads(request.data)
        usr_id = data['usrId']
        amount = data['Amount']

        #query database to find user information
        usr = User.query.get(usr_id)
        if usr:
            try:
                new_deposit = Transactions(Title='Deposit', Amount=amount,Status=PENDING, user_id=usr.id)
                db.session.add(new_deposit)
                db.session.commit()
            except Exception as e:
               print(str(e))
    return render_template('deposit.html', usr=current_user, active_page=ACTIVE_PAGE, btc=btc_wallet, number_of_notices=number_of_notices,)

@views.route('/notifications', methods = ['GET', 'POST'])
@login_required
def notifications():
    ACTIVE_PAGE = 'notices'
    #query database for all notifications associated with the user
    notifications = Notifications.query.filter_by(user_id=current_user.id).all()
    #query for all posts
    posts = Post.query.all()
    #append to a list
    notification_details = []
    for notification in notifications:
        notification_details.append(notification)
    for post in posts:
        notification_details.append(post)
    return render_template('notifications.html', usr=current_user, active_page=ACTIVE_PAGE, notifications=notification_details)

@views.route('/history', methods = ['GET', 'POST'])
@login_required
def transaction_history():
    ACTIVE_PAGE = 'transaction'
    #query database for transactions related to the user
    Record = Transactions.query.filter_by(user_id=current_user.id).all()
    return render_template('transaction history.html', usr=current_user, active_page=ACTIVE_PAGE, record=Record)

@views.route('/trade', methods = ['GET', 'POST'])
@login_required
def trade():
    ACTIVE_PAGE = 'trade'
    #query database for open trades related to the user
    Trade = Transactions.query.filter_by(Title='Trade', Status='Open', user_id=current_user.id).all()
    return render_template('trade.html', usr=current_user, active_page=ACTIVE_PAGE, number_of_trades = len(Trade))

@views.route('/withdraw-request', methods = ['GET', 'POST'])
@login_required
def withdraw_request():
    notices = Notifications.query.filter_by(user_id=current_user.id).all()
    number_of_notices = len(notices)

    ACTIVE_PAGE = 'withdraw'
    if request.method == 'POST':


        if current_user.is_verified == False:
            flash('Please Verify your account to be able to withdraw.', category='error')
        else:
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
        

           
    return render_template('Withdraw-request.html', usr=current_user, active_page=ACTIVE_PAGE, number_of_notices=number_of_notices)

@views.route('/withdraw', methods = ['GET', 'POST'])
@login_required
def withdraw():
    ACTIVE_PAGE = 'withdraw'

    #get the session data
    Amt = session['amount']
    wallet_address = session['wallet-address']
    wallet = secure_wallet(wallet_address)
    fee_charge = round(0.05 * Amt, 2)
    Balance = Amt + fee_charge
    if request.method == 'POST':
        user_id = current_user.id
        
        #get password from form data
        usr_pin = request.form.get('pin')

        #query database to get user and user info
        usr = User.query.get(user_id)
        avail_bal = float(usr.Available_balance)
        if usr_pin == '':
            flash('Please enter your pin', category='error')
        else:
            if bcrypt.checkpw(usr_pin.encode('utf-8'), usr.Pin):
                new_transaction = Transactions(Title='Withdrawal', Amount=Amt, Status=PENDING, Wallet=wallet_address,Fee=fee_charge, user_id=user_id)
                db.session.add(new_transaction)
                db.session.commit()
                flash(f'Withdrawal of {Amt} is being processed')
                return redirect(url_for('views.profile'))
            else:
                flash('Incorrect Password! Try again.', category='error')
       
    return render_template('Withdraw.html', usr=current_user, active_page=ACTIVE_PAGE, amount=Amt, Wallet_address=wallet, fee=fee_charge )


@views.route('/settings', methods = ['GET', 'POST'])
@login_required
def settings():
    notices = Notifications.query.filter_by(user_id=current_user.id).all()
    number_of_notices = len(notices)

    ACTIVE_PAGE = 'profile'
    return render_template('settings.html', usr=current_user, active_page=ACTIVE_PAGE, number_of_notices=number_of_notices)

@views.route('/profile-security', methods = ['GET', 'POST'])
@login_required
def profile_security():
    notices = Notifications.query.filter_by(user_id=current_user.id).all()
    number_of_notices = len(notices)

    ACTIVE_PAGE = 'profile'
    usr = current_user
    if request.method == 'POST':
        form_type = request.form.get('form-type')
        if form_type == 'pwd-change-form':
            current_pwd = request.form.get('c-pwd')
            new_pwd = request.form.get('n-pwd')   

            if bcrypt.checkpw(current_pwd.encode('utf-8'), usr.Password):
                usr.Password = bcrypt.hashpw(new_pwd.encode('utf-8'), bcrypt.gensalt())
                db.session.commit()
                flash('Password has been updated!', category='success')
                msg = Message('Password Change', recipients=[usr.Email])
                msg.body = f''' 
                Dear {usr.First_name} {usr.Last_name},
                You have successfully changed your TradeNest password.
                Don’t recognize this activity?
                Secure your account immediately.
                '''
                mail.send(msg)
            else: 
                flash('Current password mismatch!', category='error')
        else:
            current_pin = request.form.get('c-pin')
            new_pin = request.form.get('n-pin')   
            if len(new_pin) > 4:
                flash('New pin must be 4 digits', category='error')
            else:
                if bcrypt.checkpw(current_pin.encode('utf-8'), usr.Pin):
                    usr.Pin = bcrypt.hashpw(new_pin.encode('utf-8'), bcrypt.gensalt())
                    db.session.commit()
                    flash('Pin has been updated!', category='success')
                    msg = Message('Pin Change', recipients=[usr.Email])
                    msg.body = f'''
                                Dear {usr.First_name} {usr.Last_name},
                                You have successfully changed your TradeNest withdrawal pin.
                                Don’t recognize this activity?
                                Secure your account immediately.
                            '''
                    mail.send(msg)
                else: 
                    flash('Current Pin mismatch!', category='error')
    return render_template('security.html', usr=current_user, active_page=ACTIVE_PAGE, number_of_notices=number_of_notices)

@views.route('/faq', methods = ['GET', 'POST'])
@login_required
def help():
    ACTIVE_PAGE = 'profile'
    return render_template('faq.html', usr=current_user, active_page=ACTIVE_PAGE)

@views.route('/verify-email', methods = ['GET', 'POST'])
@login_required
def verify_email():
    data = json.loads(request.data)
    usr_email = data['usrEmail']
    if usr_email:
        token = s.dumps(usr_email, salt='verify-email')
        reset_link = url_for('auth.confirm_email', token=token, _external=True)
        msg = Message('Comfirm Email Address', recipients=[usr_email])
        msg.html = f'''
        click the link below to <a href='{reset_link}'>verify your email address</a>
        This link expires in 30 minutes.
        
        '''
        mail.send(msg)
    return jsonify({})