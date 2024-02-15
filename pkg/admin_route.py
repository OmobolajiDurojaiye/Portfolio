from flask import Flask, render_template, url_for, redirect, request, session, flash
from pkg import app, mail
from pkg.models import User, db, Admin
from flask_mail import Message

# ...

@app.route('/user_management/', methods=['GET', 'POST'])
def user_management():
    if request.method == 'GET':
        users = User.query.all()
        return render_template('admin/user_management.html', user=users)
    elif request.method == 'POST':
        pass

@app.route('/send_message/<int:user_id>', methods=['POST'])
def send_message(user_id):
    user = User.query.get(user_id)
    if not user:
        flash('User not found')
        return redirect(url_for('user_management'))

    if request.method == 'POST':
        message_content = request.form.get('message_content')
    
        if not message_content:
            flash('Please provide a message content')
            return redirect(url_for('user_management'))

        subject = f'Message from Omobolaji Durojaiye'
        body = f'Hello {user.users_fullname},\n\n{message_content}\n\nBest regards,\nOmobolaji Durojaiye'

        try:
            msg = Message(subject, sender=app.config['MAIL_USERNAME'], recipients=[user.users_email])
            msg.body = body
            mail.send(msg)
            flash(f'Message sent to {user.users_fullname} via email')
        except Exception as e:
            flash(f'Error sending email: {str(e)}')

        return redirect(url_for('user_management'))



@app.route('/delete_user/<int:user_id>', methods=['POST'])
def delete_user(user_id):
    user_to_delete = User.query.get_or_404(user_id)
    db.session.delete(user_to_delete)
    db.session.commit()
    flash("User deleted successfully")
    return redirect(url_for('user_management'))

@app.route('/admin/login/', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'GET':
        return render_template('admin/admin_login.html')
    else:
        username = request.form.get('adminusername')
        password = request.form.get('adminpwd')

        admin = db.session.query(Admin).filter(Admin.admin_username == username).first()
        if admin and admin.admin_password == password:
            session['adminonline'] = admin.id
            flash("Welcome", category="success")
            return redirect('/user_management/')
        else:
            flash("Invalid credentials", category="error")
            return redirect('/admin/login/')
        
@app.route('/adminlogout/')
def adminlogout():
    session.pop('adminonline', None)
    return redirect('/admin/login/')