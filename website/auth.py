from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_user, logout_user, login_required, current_user
from . import db 
from .newmodels import NewUser
import bcrypt

auth = Blueprint('auth', __name__ )


@auth.route('/login-Signup', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':

        #get the form type(loginform or signupform)
        Form_type = request.form.get('form-type')
        
        if Form_type == 'loginForm':

            #get login details
            email = request.form.get('email')
            password = request.form.get('pwd')

            #query database to see if user exists
            usr = NewUser.query.filter_by(Email=email).first()
            if usr:
                #check if password is correct
                if bcrypt.checkpw(password.encode('utf-8'), usr.Password):
                # if password == usr.Password:
                    flash('Login Successful....!', category='success')
                    login_user(usr)
                    return redirect(url_for('views.profile'))
                else:
                    flash('Incorrect Password! Try again.', category='error')
            else:
                flash('Account not found.......', category='error')
        elif Form_type == 'signForm': 

            #get registration details
            firstname = request.form.get('fname')
            lastname = request.form.get('lname')
            email = request.form.get('email')
            phone_number = request.form.get('phone-no')
            password1 = request.form.get('pwd1')
            password2 = request.form.get('pwd2')
            subscription = request.form.get('optradio')

            #query database to see if user exists
            usr = NewUser.query.filter_by(Email=email).first()

            #checks
            if usr:
                flash('Registration failed....... Accounts Already Exists! Login to see your profile.', category='success')
                return redirect(url_for("auth.login_sign_up"))
            elif len(email) < 4:
                flash('Invalid Email Address. Check your email and try again!.', category='error')
            elif len(phone_number) > 11:
                flash('Invalid Phone Number....... Check and Try Again!', category='error')
            elif password1 != password2:
                flash('Passwords do not Match!...... Please Try Again.', category='error')
            else:
                new_usr = NewUser(First_name=firstname, Last_name=lastname, Email=email, 
                               Phone_number=phone_number, Subscription_plan=subscription,
                               Password=bcrypt.hashpw(password1.encode('utf-8'), bcrypt.gensalt()))
                db.session.add(new_usr)
                db.session.commit()
                login_user(new_usr)

                return redirect(url_for('views.profile'))
    return render_template('login-register.html', usr=current_user)

@login_required
@auth.route('/logout', methods=['GET', 'POST'])
def logout():
    logout_user()
    return redirect(url_for('views.home'))
