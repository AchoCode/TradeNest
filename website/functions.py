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
    if model:
        print(f'{DB_NAME} {model}')
        print(f"Number of {model}: {len(model)}")
        i = 0
        for transaction in model:
            i += 1
            usr_id = transaction.user_id
            usr = NewUser.query.get(usr_id)
            print(f'{i}. User: {usr.First_name} {usr.Email}: {transaction.Title} {transaction.Title} {transaction.Amount} {transaction.Status}')
    else:
        print(f'No {model} found in {DB_NAME}')


#function to display admin and comment after database migration
def admin_comments(model):
    admins = []
    if model:
        print(f'{DB_NAME} {model}')
        print(f"Number of {model}: {len(model)}")
        i = 0
        for counter in model:
            i += 1
            if model == admins:
                print(f'{i}. {counter.First_name} {counter.Last_name} {counter.Email}')
            else:
                print(f'{i}. User: {counter.User_name} {counter.Email} | comment: {counter.Comment} {counter.Date} ')
    else:
        print(f'No {model} found in {DB_NAME}')