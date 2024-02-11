from flask import Flask, render_template, url_for, redirect, request, session, flash
from pkg import app
from pkg.models import User, db

@app.route('/', methods= ['POST', 'GET'])
def index():
    if request.method == 'GET':
        return render_template('user/index.html')
    else:
        fullname = request.form.get('name')
        email = request.form.get('email')
        message = request.form.get('description')

        if fullname == '' or email == '' or message == '':
            flash('No field should be left empty', 'success')
            return redirect('/')
        else:
            user = User(users_fullname = fullname, users_email = email, message = message)

            db.session.add(user)
            db.session.commit()
            flash('Your message has been sent successfully', 'success')
            return redirect('/')



@app.route('/about/')
def about():
    return render_template('user/about.html')

@app.route('/services/')
def services():
    return render_template('user/services.html')

@app.route('/portfolio/')
def portfolio():
    return render_template('user/portfolio.html')

@app.route('/contact/', methods= ['POST', 'GET'])
def contact():
    if request.method == 'GET':
        return render_template('user/contact.html')
    else:
        fullname = request.form.get('name')
        email = request.form.get('email')
        message = request.form.get('description')

        user = User(
            users_fullname = fullname,
            users_email = email,
            message = message
        )

        db.session.add(user)
        db.session.commit()
        flash('Your message has been sent successfully', 'success')
        return redirect('/contact')