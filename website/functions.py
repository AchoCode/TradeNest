from . import db

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

