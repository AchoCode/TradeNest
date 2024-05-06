import random
#function to replace some part of the wallet address with *
def secure_wallet(input_string):
    start_index = 4
    end_index = 27
    modified_string = input_string[:start_index] + '*' * (end_index - start_index + 1) + input_string[end_index + 1:]
    return modified_string

#function to generate random numbers
def random_transaction_id():
    number = random.randrange(1, 99999999)
    return number
if __name__ == '__main__':
    number = random_transaction_id()
    name = 'dfnidngdfgfgnfgndfngiudfgdfngodfngodm'
    print(f'{secure_wallet(name).capitalize()} 100{number}')            