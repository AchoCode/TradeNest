from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_user, logout_user, login_required, current_user
from . import db, mail
from itsdangerous import URLSafeTimedSerializer, SignatureExpired, BadSignature
from flask_mail import Message
from .models import User
import bcrypt
import time
auth = Blueprint('auth', __name__ )

s = URLSafeTimedSerializer('this is a secret')

@auth.route('/login', methods=['GET', 'POST'])
def login():
    reset = request.args.get('reset')
    resetForm = False
    if reset:
        if reset == 'live':
            resetForm = True
    if request.method == 'POST':
        # get form type
        form_type = request.form.get('form-type')

        if form_type == 'resetForm':
            email = request.form.get('email')
            #query database for usr
            usr = User.query.filter_by(Email=email).first()

            if usr:
                token = s.dumps(usr.Email, salt='email-pwd-reset')
                reset_link = url_for('auth.reset', token=token, _external=True)
                msg = Message('Password Reset!!', recipients=[usr.Email])
                msg.html = f'''
                click the link below to <a href='{reset_link}'>reset your password</a>
                This link expires in 30 minutes.
                
                '''
                mail.send(msg)
                flash('A password email link has been sent to your email', category='success')
                resetForm = True
            else:
                resetForm = True
                flash('Account not found! check your email address', category='error')
        else:
            #get login details
            email = request.form.get('email')
            password = request.form.get('pwd')

            #query database to see if user exists
            usr = User.query.filter_by(Email=email).first()

            if usr:
                #check if password is correct
                if bcrypt.checkpw(password.encode('utf-8'), usr.Password):
                    flash('Login Successful....!', category='success')
                    login_user(usr)
                    if usr.Role == 'user':
                        return redirect(url_for('views.profile'))
                    else:
                        return redirect(url_for('admin.admin_dashboard'))
                else:
                    flash('Incorrect Password! Try again.', category='error')
            else:
                flash('Account not found! check your email address', category='error')
    return render_template('login.html', usr=current_user, resetForm=resetForm)

@auth.route('/register', methods=['GET', 'POST'])
def register():
    plan = request.args.get('plan')
    if request.method == 'POST':

        #get registration details
        firstname = request.form.get('fname')
        lastname = request.form.get('lname')
        email = request.form.get('email')
        phone_number = request.form.get('phone-no')
        password1 = request.form.get('pwd1')
        password2 = request.form.get('pwd2')
        subscription = request.form.get('optradio')

        #query database to see if user exists
        usr = User.query.filter_by(Email=email).first()

        #checks 
        if usr:
            flash('Registration failed....... Account Already Exists! Login to see your profile.', category='success')
            return redirect(url_for("auth.login"))
        elif len(email) < 4:
            flash('Invalid Email Address. Check your email and try again!.', category='error')
        elif len(phone_number) > 11:
            flash('Invalid Phone Number....... Check and Try Again!', category='error')
        elif password1 != password2:
            flash('Passwords do not Match!...... Please Try Again.', category='error')
        else:
            new_usr = User(First_name=firstname.capitalize(), Last_name=lastname.capitalize(), Email=email, 
                            Phone_number=phone_number, Subscription_plan=subscription,
                            Password=bcrypt.hashpw(password1.encode('utf-8'), bcrypt.gensalt()),
                            Pin=bcrypt.hashpw('0000'.encode('utf-8'), bcrypt.gensalt()))
            db.session.add(new_usr)
            db.session.commit()
            login_user(new_usr)
            flash('Registration complete', category='success')

            # email message
            web_link = url_for('views.home', _external=True)
            profile_link = url_for('auth.login', _external=True)

            html_content = render_template('email-template.html', website_link=web_link, profile_link=profile_link)

            msg = Message('Account Creation Successful!!!', recipients=[email], html=html_content)
            # msg.body = f'''Dear {firstname.upper()} {lastname.upper()},
            # Your account registration has been completed. Please check your Profile settings
            # to verify your email to be able to CashOut your Profits and Equity. 

            # Save, invest and trade at the same time with TradeNest....

            # If you have more Questions please contact us through our Customer care
            # Thanks for your Patronage: TradeNestXchange mgt
            
            # '''
            try:
                mail.send(msg)
            except:
                flash('Error occured')
            return redirect(url_for('views.profile'))
    return render_template('register.html', usr=current_user, selected_plan=plan)

@login_required
@auth.route('/logout', methods=['GET', 'POST'])
def logout():
    logout_user()
    return redirect(url_for('views.home'))

@auth.route('/reset/<token>', methods=['GET', 'POST'])
def reset(token):
    try:
        email = s.loads(token, salt='email-pwd-reset', max_age=1800)
        if request.method == 'POST':
            #get the new password
            new_password = request.form.get('new-pwd')
            confirm_password = request.form.get('confirm-pwd')
            #query database for user
            usr = User.query.filter_by(Email=email).first()
            if new_password == confirm_password:
                usr.Password = bcrypt.hashpw(new_password.encode('utf-8'), bcrypt.gensalt())
                db.session.commit()
                flash('Password has been Updated')

                #send success email
                msg = Message('Password Changed', recipients=[usr.Email])
                msg.body = f'''
                Dear {usr.First_name.capitalize()} {usr.Last_name.capitalize()},
                your password reset was successful, if this wasnt your please contact us to secure your account.
                Thanks
                '''
                mail.send(msg)
                return redirect(url_for('auth.login'))
            else:
                flash('Password mismatch. Try again!', category='error')
    except SignatureExpired:
        return render_template('reset-pwd-pin.html', token_expired=True, confirm_email=False)
    except BadSignature:
        flash('Reset token does not match!!!', category='error')
        return redirect(url_for('auth.login', reset='live'))
    return render_template("reset-pwd-pin.html", token_expired=False, confirm_email=False)

@auth.route('/confirm-email/<token>')
def confirm_email(token): 
    try:
        email = s.loads(token, salt='verify-email', max_age=1800)
        usr = User.query.filter_by(Email=email).first()
        if usr:
            usr.is_verified = True
            db.session.commit()
            flash('Email verification successful')

            #send success email
            msg = Message('Email Verification Successful', recipients=[usr.Email])
            msg.body = f'''
            Dear {usr.First_name.capitalize()} {usr.Last_name.capitalize()},
            your Email has been verified, you are now eligible to withdraw your funds 
            from your account.
            Save, invest and trade with TradeNestXchange..
            Thanks
            '''
            mail.send(msg)
            login_user(usr)
            return redirect(url_for('views.profile'))
    except SignatureExpired:
        return render_template('reset-pwd-pin.html', token_expired=True, confirm_email=True)
    except BadSignature:
        flash('email confirm token does not match!!!', category='error')
        return redirect(url_for('views.profile'))

@auth.route('/send-email')
def send():
    email = ['luckyacho2@gmail.com']
    web_link = url_for('views.home', _external=True)
    profile_link = url_for('auth.login', _external=True)

    html_content = render_template('withdrawal-email.html', website_link=web_link, profile_link=profile_link, usr='Lucky Acho')

    msg = Message('Deposit of Funds!', recipients=email, html=html_content)
    try:
        mail.send(msg)
    except:
        flash('error occured!', category='error')
        time.sleep(180)
        mail.send(msg)

    return 'Email sent'
