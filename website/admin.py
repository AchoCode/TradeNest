from flask import Blueprint, render_template, request
from .models import *
from .newmodels import *
from flask_login import login_required, current_user
from .functions import *
from . import DB_NAME
from .views import SUCCESS

admin = Blueprint('admin', __name__)


@admin.route('/dashboard', methods=['GET', 'POST'])
@login_required
def admin_dashboard():

    #get the total deposit
    income = NewTransactions.query.all()
    for fund in income:
        if fund.Title == 'Deposit':
            print('Deposit')
        if fund.Title == 'Withdrawal':
            print('withdrawal')

    users = NewUser.query.all()
    number_of_users = len(users)

    active_users = []
    for x in users:
        if x.is_active == True:
            active_users.append(x)

    number_of_active_users = len(active_users)

    #get the formtype
    if request.method == 'POST':
        form_type = request.form.get('form-type')

        if form_type == 'Dash-mail-form':
            recepient_mail = request.form.get('recepient-mail')
            mail_title = request.form.get('mail-title')
            mail_body = request.form.get('mail-body')

            if recepient_mail != 'All users':
                print(recepient_mail)
            else:
                pass                

            print(F'{form_type} submitted')
        elif form_type == 'User-form':

            #query database for users
           

            print(F'{form_type} submitted')
        elif form_type == 'post-form':
            print(F'{form_type} submitted')
        else:
            print(F'{form_type} submitted')
        




    return render_template('Admin.html', usr=current_user,  clients=users, number_of_users=number_of_users,
                           active_user=number_of_active_users)




#DOCUMENTATION: 
#Due to the structure of the codebase we cant used flask-migrate. it is structured in the factory application format
#We manually query our old database and transfer the data to the new model from this route
#! Before you run this route configure the database models and your new database should be your default database
#! Add the bind key of OLD_DB to all the class tables in the old model script
#! Uncomment the app.config_sqlalchemybinds in the Init.py file
#! your old database model should be the database in your app.config-sqlalchemybinds
@admin.route('/database-migrate')
@login_required
def migrate_database():
    if request.method == "GET":
        #query all the tables of the old database
        old_admins = Admin.query.all()
        old_users = User.query.all()
        old_comments = Comments.query.all()
        old_transactions = Transactions.query.all()
        old_notifications = Notifications.query.all()

        #query users from the new database
        users = NewUser.query.all()
        admins = NewAdmin.query.all()
        comments = NewComments.query.all()
        transactions = NewTransactions.query.all()
        notifications = NewNotifications.query.all()


        #map data from the old database to the new one
        # for the Users
        if old_users:
            print(' Old Database users')
            print(f"Number of users: {len(old_users)}")
            print('data transfer initiated')
            i = 0
            for usr in old_users:
                if usr in users:
                    i += 1
                    print(F'user "{usr.First_name} {usr.Last_name} {usr.Email}" already exist in {DB_NAME}')
                else:
                    i += 1
                    print(f'{i}. {usr.First_name} {usr.Last_name} {usr.Email}')
                    new_user = NewUser(First_name=usr.First_name, Last_name=usr.Last_name, Email=usr.Email,
                                    Phone_number=usr.Phone_number, Password=usr.Password, Balance=usr.Balance,
                                    Total_balance=usr.Total_balance, Available_balance=usr.Available_balance,
                                    Subscription_plan=usr.Subscription_plan, Date_joined=usr.Date_joined)
                    db.session.add(new_user)
                    db.session.commit()
            print('User data transfer successful')
        else:
            print('No user found')

        # For Admins
        if old_admins:
            print('Old Database Admins')
            print(f"Number of Admins: {len(old_admins)}")
            i = 0
            for admin in old_admins:
                if admin in admins:
                    print(f'Admin User "{admin.First_name} {admin.Last_name} {admin.Email}" Already Exists in the database')
                else:
                    i += 1
                    print(f'{i}. {admin.First_name} {admin.Last_name} {admin.Email}')
                    new_admin = Admin(Email=admin.Email,Password=admin.Password)
                    db.session.add(new_admin)
                    db.session.commit()
            print('Admin data transfer successful')
        else:
            print('No Admin user found')
        
        # For Comments
        if old_comments:
            print('Old Database Comments')
            print(f"Number of Comments: {len(old_comments)}")
            i = 0
            for comment in old_comments:
                if comment in comments:
                    print(f'Comment by user "{comment.First_name} {comment.Last_name} {comment.Email}" already exists in the database')
                else:
                    i += 1
                    print(f'{i}. {comment.First_name} {comment.Last_name} {comment.Email}')
                    new_comment = Comments(Email=comment.Email,Comment=comment.Comment,User_name=comment.Comment_name)
                    db.session.add(new_comment)
                    db.session.commit()
            print('Comment data transfer successful')
        else:
            print('No Comment Found')

        # For Transactions
        if old_transactions:
            print('Old Database Transactions')
            print(f"Number of Transactions: {len(old_transactions)}")
            i = 0
            for transaction in old_transactions:
                if transaction in transactions:
                    print(f'Transaction "{transaction.Title} {transaction.Amount} {transaction.Status}" already exists in the database')
                else:
                    i += 1
                    print(f'{i}. {transaction.Title} {transaction.Amount} {transaction.Status}')
                    new_transaction = Transactions(Title=transaction.Title, Amount=transaction.Amount, Status=transaction.Status,
                                    Wallet=transaction.Wallet, Profit=transaction.Profit, user_id=transaction.user_id)
                    db.session.add(new_transaction)
                    db.session.commit()
            print('Transaction data transfer successful')
        else:
            print('No Transaction found')

        # for Notifications
        if old_notifications:
            print('Old Database Notification')
            print(f"Number of Notification: {len(old_notifications)}")
            i = 0
            for notification in old_notifications:
                if notification in notifications:
                    print(f'Notification "{notification.Title} {notification.Amount} {notification.Status}" already exists in the database')
                else:
                    i += 1
                    print(f'{i}. {notification.Title} {notification.Amount} {notification.Status}')
                    new_notification = Notifications(Title=notification.Title, Amount=notification.Amount, Status=notification.Status,
                                    Date=notification.Date,user_id=notification.user_id)
                    db.session.add(new_notification)
                    db.session.commit()
            print('Notification data transfer successful')
        else:
            print('No Notification found')


        if users:
            print(f'{DB_NAME} users')
            print(f"Number of Users: {len(users)}")
            i = 0
            for usr in users:
                i += 1
                print(f'{i}. {usr.First_name} {usr.Last_name} {usr.Email} {usr.Pin} {usr.is_active}')
        else:
            print(f'No user found in {DB_NAME}')

        #for admins
        admin_comments(admins)

        #for comments
        admin_comments(comments)
        
        #for transactions
        transaction_notification(transactions)

        #for notifications
        transaction_notification(notifications)


    return F'Migration into {DB_NAME} was successful!!!!'