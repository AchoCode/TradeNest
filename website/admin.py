from flask import Blueprint, render_template, request, jsonify, flash, redirect,url_for
from .models import *
from .models import *
from flask_login import login_required, current_user
from .functions import *
from .views import SUCCESS,PENDING,OPEN,CLOSED
import json
import bcrypt
from flask_mail import Message
from . import mail
admin = Blueprint('admin', __name__)


@admin.route('/dashboard', methods=['GET', 'POST'])
def admin_dashboard():
    active_page = 'Overview'
    page = request.args.get('activepage')
    
    if page == None:
        pass
    else:
        if page == 'comment':
            active_page = 'CommentTab'
        elif page == 'deposit':
            active_page = 'DepositTab'
        elif page == 'post':
            active_page = 'PostTab'
        elif page == 'user':
            active_page = 'UserTab'
        else:
            active_page = 'overview'
    

    trades = Transactions.query.filter_by(Title='Trade', Status=OPEN).all()
    #query for admin and wallet
    admins = User.query.filter_by(Role='admin').all()
    site_wallet = Wallet.query.all()

    form_status = False
    #for dasboardtab
    users = User.query.filter_by(Role='user').all()
    number_of_users = len(users)

    #for dasboard overview
    income = db.session.query(db.func.sum(Transactions.Amount)).filter_by(Title='Deposit', Status=SUCCESS).scalar()
    payouts = db.session.query(db.func.sum(Transactions.Amount)).filter_by(Title='Withdrawal', Status=SUCCESS).scalar()
    if income is None:
        income = 0
    if payouts is None:
        payouts = 0

    profit = income - payouts

    #for the withdrawal tab
    withdrawals = Transactions.query.filter_by(Title='Withdrawal', Status=PENDING).all()

    # for deposit tab
    deposits = Transactions.query.filter_by(Title='Deposit', Status=PENDING).all()
    deposit_details = []
    for deposit in deposits:
        deposit_usr = User.query.get(deposit.user_id)
        if deposit_usr:
            details = {
                'id' : deposit.id,
                'Username' : f'{deposit_usr.First_name} {deposit_usr.Last_name}',
                'Email': deposit_usr.Email,
                'Date': deposit.Date,
                'Amount' : deposit.Amount
            }
            deposit_details.append(details)

    # for comments tab
    comments = Comments.query.all()
 
    #for user tab
    active_users = []
    for x in users:
        if x.is_active == True:
            active_users.append(x)

    number_of_active_users = len(active_users)

    #for post tab
    posts = Post.query.all()

    if request.method == 'POST':
        #get the formtype
        form_type = request.form.get('form-type')

        if form_type == 'Trade-form':
            #get from data
            trade_usr_id = request.form.get('usr-id')
            amount = request.form.get('amount')
            trade_profit = request.form.get('profit')
            duration = request.form.get('duration')

            #query for user
            trade_usr = User.query.get(trade_usr_id)
            if trade_usr:
                #calculate the balance left after subtracting the amount
                trade_usr.Balance = float(trade_usr.Balance) - float(amount)
                if trade_usr.Subscription_plan == 'Bronze':
                    lot_size = 0.30
                elif trade_usr.Subscription_plan == 'Silver':
                    lot_size = 0.35
                else: 
                    #for gold subscription
                    lot_size = 0.40
                new_trade = Transactions(Title='Trade', Amount=amount, Duration=duration,Lot_size=lot_size, Profit=trade_profit, Status=OPEN, user_id=trade_usr.id)
                new_notification = Notifications (Title='Trade', Amount=amount, Status=OPEN,  user_id=trade_usr.id)
                db.session.add_all([new_trade,new_notification])
                db.session.commit()
                flash('Trade has been Initiated', category='success')

                # trade email message
                
                msg = Message('Trade Activation', recipients=[trade_usr.Email])
                msg.html = f''' 
                Dear {trade_usr.First_name.upper()} {trade_usr.Last_name.upper()},
                
                A trade of equity <strong>${amount}.00</strong> and lot size of <strong>{lot_size}</strong> <br>
                has been initiated Successfully. Your estimated profit return is <strong>${trade_profit}</strong>. <br>
                After a period of {duration} days, your profit will be added to your available balance and your<br>
                equity will saved. Visit your profile dashboard for more information.<br>

                For further enquiries, please contact our customer support through the following channels:<br>
                Email: tradenestxchange@gmail.com<br>
                Phone: 07008888328<br>
                
                Thank you for choosing TradeNest.

                '''
                mail.send(msg)
                return redirect(url_for('admin.admin_dashboard',activepage='user'))

        elif form_type == 'admin-form':
            email = request.form.get('email')
            password1 = request.form.get('pwd1')
            confirmed_password = request.form.get('pwd2')
            wallet = request.form.get('wallet')
            admin_wallet = Wallet.query.filter_by(id="1").first()

            #check for email
            if email:
                admin_usr = User.query.filter_by(Email=email).first()
                if not admin_usr:
                    if password1 == '':
                        flash('Please enter a Password!', category='error')
                    else:
                        if password1 != confirmed_password:
                            flash('Password mismatch. Try again!', category='error')
                            form_status = True
                        else:
                            if wallet:
                                new_admin = User(Email=email, Password=bcrypt.hashpw(password1.encode('utf-8'), bcrypt.gensalt()), Role='admin')
                                if admin_wallet:
                                    admin_wallet.Wallet = wallet
                                else:
                                    new_wallet = Wallet(Wallet=wallet)
                                    db.session.add_all([new_admin,new_wallet])
                                flash('Admin User and Wallet created Successfully', category='success')
                            else:
                                new_admin = User(Email=email,Password=bcrypt.hashpw(password1.encode('utf-8'), bcrypt.gensalt()), Role='admin')
                                db.session.add(new_admin)
                                flash('Admin User created Successfully', category='success')
                            #commit to database
                            db.session.commit()
                else:
                    flash('Admin User already exist!', category='error')
            else:
                admin_wallet = Wallet.query.filter_by(id="1").first()
                admin_wallet.Wallet = wallet
                db.session.commit()
                flash('Wallet updated successfully', category='success')

        elif form_type == 'Dash-mail-form':

            #get form data
            email = request.form.get('recepient-mail')
            mail_title = request.form.get('mail-title')
            mail_body = request.form.get('mail-body')

            if email != 'users':
                msg = Message(mail_title, recipients=[email])
                msg.body = mail_body
                mail.send(msg)
                flash(f'Email sent to {email}', category='success')
            else:
                users_emails = []
                users = User.query.all()
                for usr in users:
                    usr_email = usr.Email
                    users_emails.append(usr_email)
                msg = Message(mail_title, recipients=[], bcc=users_emails)
                msg.body = mail_body
                mail.send(msg)
                flash(f'Email sent to {email}', category='success')               

        elif form_type == 'User-form':
            
            active_page = 'UserTab'
            #get form data
            user_mail = request.form.get('email')
            subscription = request.form.get('sub-plan')
            balance = request.form.get('balance')
            avail_balance = request.form.get('avail-balance')
            active_status = request.form.get('optradio')

            #query for the user
            user = User.query.filter_by(Email=user_mail).first()
            if user:
                #update user
                user.Subscription_plan = subscription
                user.Balance = balance
                user.Available_balance = avail_balance
                if active_status == 'True':
                    user.is_active = True
                else:
                    user.is_active = False
                db.session.commit()
                flash('Update successful!', category='success')

            else:
                flash('User does not exist!', category='error')
            # return redirect(url_for('admin.admin_dashboard'))

        elif form_type == 'post-form':
            active_page = 'PostTab'

            #get form data
            post_title = request.form.get('post-title')
            post_body = request.form.get('post-body')
            
            new_post = Post(Title=post_title, Message=post_body)
            db.session.add(new_post)
            db.session.commit()
            flash('Post created successfully!', category='success')
            
        else:
            active_page = 'WithdrawalTab'
            #get form data
            transaction_id = request.form.get('transaction-id')
            status = request.form.get('optradio')
            #query for the transaction
            transaction = Transactions.query.get(transaction_id)
            transaction_usr = User.query.get(transaction.user_id)

            if transaction:
                #change the status of the transaction
                if status == SUCCESS:
                    #do necessary arithmetic operations
                    avail_bal = float(transaction_usr.Available_balance)
                    new_bal = avail_bal - float(transaction.Amount) - float(transaction.Fee)
                    if new_bal < 0:
                        flash('Balance is less than zero', category='error')
                    else:
                        withdrawal_id = f'100{random_transaction_id()}'
                        transaction_usr.Available_balance = round(new_bal, 2)
                        transaction.Status = status
                        flash('Withdrawal has been processed', category='success')
                        
                        #withdrawal email message
                        msg = Message('Withdrawal successful', recipients=[transaction_usr.Email])
                        msg.html = f''' 
                        Dear {transaction_usr.First_name.upper()} {transaction_usr.Last_name.upper()},
                        
                        Your withdrawal of <strong>${transaction.Amount}.00</strong> was successful. <br>
                        The recipient wallet will be credicted in the next 24hours. <br>
                        Your available balance is <strong>${transaction_usr.Available_balance}</strong> <br>.
                        
                        Withdrawal Details:
                        Wallet: <strong>{secure_wallet(transaction.Wallet)}</strong><br>
                        Fee: <strong>${transaction.Fee}</strong><br>
                        Amount: <strong>${transaction.Amount}.00</strong><br>
                        Date: <strong>{transaction.Date}</strong><br>
                        Transaction id: <strong>{withdrawal_id}</strong><br>
                        For further enquiries, please contact our customer support through the following channels:<br>
                        Email: tradenestxchange@gmail.com <br>
                        Phone: 07008888328<br>
                        
                        Thank you for choosing TradeNest.

                        '''
                        mail.send(msg)
                else:
                    #set the status to denied
                    transaction.Status = status

                #create a new notification
                new_notification = Notifications(Title=transaction.Title, Amount=transaction.Amount, Status=transaction.Status, user_id=transaction.user_id)
                db.session.add(new_notification)
                db.session.commit()
                return redirect(url_for("admin.admin_dashboard"))
    else:
        admin_usr = User.query.filter_by(Role='admin').first()
        if admin_usr:
            usr_id = current_user.id
            usr = User.query.get(usr_id)
            if usr:
                if usr.Role == 'admin':
                    pass
                else:
                    flash('You are not and Admin. Only Admins can access this Interface', category='error')
                    return redirect(url_for('views.home'))
    return render_template('Admin.html', active_page=active_page,form_status=form_status, usr=current_user, clients=users, number_of_users=number_of_users, income=float(income), payouts=float(payouts), profit=float(profit),
                           active_user=number_of_active_users, number_of_requests=len(withdrawals), transaction_details=withdrawals,posts=posts, admins=admins, wallet=site_wallet, Trades=trades, number_of_trade=len(trades),
                           deposit_details=deposit_details, number_of_deposits=len(deposits), comments=comments, number_of_comments=len(comments))


@admin.route('/get-user', methods=['GET','POST'])
def get_user():
    #load json data
    data = json.loads(request.data)
    usr_id = data['usrId']

    #query the databse with data from json
    user = User.query.filter_by(id=usr_id).first()

    if user:
        #parse a dictionary with user info
        user_data = {
            'Username': f'{user.First_name} {user.Last_name}',
            'Email': user.Email,
            'Subscription' : user.Subscription_plan,
            'AvailableBalance' : user.Available_balance,
            'Balance' : user.Balance,
            'PhoneNumber' : user.Phone_number,
            'Earnings' : user.Earnings,
            'DateJoined' : user.Date_joined,
            'ActiveStatus' : user.is_active
        }
        return jsonify(user_data)
    else:
        return jsonify({'error': 'User not found'}), 404

@admin.route('/delete-user', methods=['GET','POST'])
def delete_user():
    # load the json data
    data = json.loads(request.data)
    user_id = data['usrId']

    #query database for the user
    user = User.query.get(user_id)
    user_transactions = Transactions.query.filter_by(user_id=user.id).all()
    user_notifications = Notifications.query.filter_by(user_id=user.id).all()

    if user:
        #delete the user
        db.session.delete(user)
        for transaction in user_transactions:
            db.session.delete(transaction)
        for notification in user_notifications:
            db.session.delete(notification)
        db.session.commit()
        return jsonify({'Status': 'success'})
    else:
        return jsonify({'Status': 'failed'})
    


@admin.route('/get-withdrawal', methods=['GET','POST'])
def get_withdrawal():
    #load json data
    data = json.loads(request.data)
    transaction_id = data['TransactionId']

    #query the database with data from json
    transaction = Transactions.query.filter_by(id=transaction_id).first()
    user = User.query.filter_by(id=transaction.user_id).first()

    if transaction:
        #parse a dictionary with transaction info
        transaction_data = {
            'Username': f'{user.First_name} {user.Last_name}',
            'Email': user.Email,
            'id' : transaction.id,
            'User_avail_balance' : user.Available_balance,
            'Amount' : transaction.Amount,
            'Wallet' : transaction.Wallet,
            'Fee_charge' : transaction.Fee,
            'Date' : transaction.Date,
            'ActiveStatus' : user.is_active
        }
        return jsonify(transaction_data)
    else:
        return jsonify({'error': 'User not found'}), 404

@admin.route('/approve-deposit', methods=['GET','POST'])
def approve_deposit():
    #load json data
    data = json.loads(request.data)
    deposit_id = data['depositId']
    active_page = 'DepositTab'

    #query database for the deposit transaction
    deposit_transaction = Transactions.query.get(deposit_id)

    if deposit_transaction:

        #get user making the deposit
        deposit_usr = User.query.get(deposit_transaction.user_id)

        #approve the deposit
        deposit_transaction.Status = SUCCESS
        deposit_usr.Balance = float(deposit_usr.Balance) + float(deposit_transaction.Amount)
        #create a new notification
        new_deposit = Notifications(Title=deposit_transaction.Title, Amount=deposit_transaction.Amount, Status=deposit_transaction.Status, user_id=deposit_usr.id )
        db.session.add(new_deposit)
        db.session.commit()

        #withdrawal email message
        msg = Message('Deposit of Funds', recipients=[deposit_usr.Email])
        msg.html = f''' 
        Dear {deposit_usr.First_name.upper()} {deposit_usr.Last_name.upper()},
        
        Your deposit of <strong>${deposit_transaction.Amount}.00</strong> was successful <br>
        and it's has been credicted successfully into your TradeNest account. <br>
        Your new Account balance is <strong>${deposit_usr.Balance}</strong>. <br>
        Following this deposit, a trade will be initiated shortly.<br> Visit your profile for
        more info<br>
        
        Save, invest and trade with TradeNest.<br>
        
        Thank you for choosing TradeNest.

        '''
        mail.send(msg)
    return jsonify({})

@admin.route('/delete-deposit', methods=['GET', 'POST'])
def delete_deposit():
    data = json.loads(request.data)
    deposit_id = data['depositId']
    active_page = 'DepositTab'
    #query database for the deposit transaction
    deposit_transaction = Transactions.query.get(deposit_id)

    if deposit_transaction:
        #delete the transaction
        db.session.delete(deposit_transaction)
        db.session.commit()
    return jsonify({})


@admin.route('/delete-comment', methods=['GET','POST'])
def delete_comment():
    # load the json data
    data = json.loads(request.data)
    comment_id = data['commentId']
    active_page = 'CommentTab'
    #query database for the comment
    comment = Comments.query.get(comment_id)

    if comment:
        #delete the comment
        db.session.delete(comment)
        db.session.commit()
    return jsonify({})


@admin.route('/delete-post', methods=['GET','POST'])
def delete_post():
    # load the json data
    data = json.loads(request.data)
    post_id = data['postId']
    active_page = 'postTab'

    #query database for the post
    post = Post.query.get(post_id)

    if post:
        #delete the post
        db.session.delete(post)
        db.session.commit()
    return jsonify({})

@admin.route('/set-trade', methods=['GET','POST'])
def set_trades():

    data = json.loads(request.data)
    trade_usr_id = data['tradeUsrId']
    
    #query database for transactions and user balance
    trade_usr = User.query.get(trade_usr_id)
    usr_details = {
        'id': trade_usr.id,
        'Username': f'{trade_usr.First_name} {trade_usr.Last_name}',
        'UserBalance': trade_usr.Balance,
        'TradeCount': "0",
        'SubscriptionPlan' : trade_usr.Subscription_plan
    }
    return jsonify(usr_details)

@admin.route('/close-trade', methods=['GET', 'POST'])
def close_trade():
    #load data
    data = json.loads(request.data)
    trade_id = data['tradeId']

    #query for the trade
    open_trade = Transactions.query.get(trade_id)

    #query for the user
    usr = User.query.get(open_trade.user_id)
    if open_trade.Status == OPEN:
        open_trade.Status = CLOSED
        usr.Available_balance = float(usr.Available_balance) + float(open_trade.Profit)
        usr.Earnings = float(usr.Earnings) + float(open_trade.Profit) 
        usr.Total_balance = float(usr.Total_balance) + float(open_trade.Amount)
        new_notification = Notifications (Title='Trade', Amount=open_trade.Amount, Status=CLOSED, user_id=open_trade.user_id)
        db.session.add(new_notification)
        db.session.commit()

        #withdrawal email message
        msg = Message('Trade Conclusion successful', recipients=[usr.Email])
        msg.html = f''' 
        Dear {usr.First_name.upper()} {usr.Last_name.upper()},
        Your Open trade of Equity: <strong>${open_trade.Amount}.00</strong> and lot size of <strong>{open_trade.Lot_size}</strong> <br>
        has been closed. The profit return of <strong>${open_trade.Profit}</strong> has been credicted to your available balance. <br>
        Your Equity has been saved in your wallet.<br> Visit your profile to Cashout your Available funds. <br>

        For further enquiries, please contact our customer support through the following channels: <br>
        Email: tradenestxchange@gmail.com <br>
        Phone: 07008888328 <br>
        
        Thank you for choosing TradeNest.

        '''
        mail.send(msg)
    return jsonify({})
   