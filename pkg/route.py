from flask import Flask, render_template, url_for, redirect, request, session, flash
from pkg import app
from pkg.models import User, db, Portfolio, SocialMedia

@app.route('/', methods= ['POST', 'GET'])
def index():
    if request.method == 'GET':
        social = db.session.query(SocialMedia).first()
        return render_template('user/index.html', social=social)
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
    social = db.session.query(SocialMedia).first()
    return render_template('user/about.html', social=social)

@app.route('/services/')
def services():
    social = db.session.query(SocialMedia).first()
    return render_template('user/services.html', social=social)

@app.route('/portfolio/')
def portfolio():
    social = db.session.query(SocialMedia).first()
    ports = db.session.query(Portfolio).all()
    return render_template('user/portfolio.html', ports=ports, social=social)

    

@app.route('/contact/', methods= ['POST', 'GET'])
def contact():
    if request.method == 'GET':
        social = db.session.query(SocialMedia).first()
        return render_template('user/contact.html', social=social)
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