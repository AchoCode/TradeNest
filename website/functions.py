from . import db
from . import DB_NAME
from .newmodels import *
#function to commit to database
def commit(arg1,arg2):
    db.session.add_all([arg1,arg2])
    db.session.commit()

#function to replace some part of the wallet address with *
def secure_wallet(input_string):
    start_index = 4
    end_index = 27
    modified_string = input_string[:start_index] + '*' * (end_index - start_index + 1) + input_string[end_index + 1:]
    return modified_string

#function to display transactions and notifications after migrating database
def transaction_notification(model):
    transaction = []
    if model == transaction:
        if model:
            print(f'{DB_NAME} Transactions')
            print(f"Number of Transactions: {len(model)}")
            i = 0
            for transaction in model:
                i += 1
                usr_id = transaction.user_id
                usr = NewUser.query.get(usr_id)
                print(f'{i}. User: {usr.First_name} {usr.Email}: {transaction.Title} {transaction.Title} {transaction.Amount} {transaction.Status}')
        else:
            print(f'No Transactions found in {DB_NAME}')
    else:
        if model:
            print(f'{DB_NAME} Notification')
            print(f"Number of Notification: {len(model)}")
            i = 0
            for notification in model:
                i += 1
                usr_id = notification.user_id
                usr = NewUser.query.get(usr_id)
                print(f'{i}. User: {usr.First_name} {usr.Email}: {notification.Title} {notification.Title} {notification.Amount} {notification.Status}')
        else:
            print(f'No Notification found in {DB_NAME}')


#function to display admin and comment after database migration
def admin_comments(model):
    admins = []
    if model == admins:
        if model:
            print(f'{DB_NAME} Admin Users')
            print(f"Number of Admin Users: {len(model)}")
            i = 0
            for counter in model:
                i += 1
                print(f'{i}. {counter.First_name} {counter.Last_name} {counter.Email}')
        else:
            print(f'No Admin user(s) found in {DB_NAME}') 
    else:
        if model:
            print(f'{DB_NAME} comments')
            print(f"Number of comments: {len(model)}")
            i = 0
            for counter in model:
                i += 1
                print(f'{i}. User: {counter.User_name} {counter.Email} | comment: {counter.Comment} {counter.Date} ')
        else:
            print(f'No Comments found in {DB_NAME}')
            