import os, random, string
from werkzeug.utils import secure_filename
from flask import Flask, render_template, url_for, redirect, request, session, flash
from pkg import app, mail
from pkg.models import User, db, Admin, Portfolio, SocialMedia
from flask_mail import Message

ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/user_management/', methods=['GET', 'POST'])
def user_management():
    online = session.get('adminonline')
    if not online:
        return redirect('/admin/login/')

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


@app.route('/admin/form/', methods=['POST', 'GET'])
def admin_form():
    if request.method == 'GET':
        id = session.get('adminonline')
        social = SocialMedia.query.get(id)
        return render_template('admin/admin_form.html', social=social)
    else:
        github_url = request.form.get('github-url')
        live_url = request.form.get('live-url')
        site_desc = request.form.get('site-desc')
        
        site_pic = request.files.get('site-image')
        if site_pic and allowed_file(site_pic.filename):
            filename = secure_filename(site_pic.filename)

            final_name = os.path.join("pkg/static/uploads/", filename)
            site_pic.save(final_name)
        else:
            flash('Invalid file format or no file provided')

        if github_url != '' or site_desc != '':
            port = Portfolio(
                github_url=github_url,
                live_url=live_url,
                port_desc=site_desc,
                site_pic=filename 
            )

            db.session.add(port)
            db.session.commit()
            flash('Inserted successfully')
            return redirect('/admin/form/')
        else:
            flash("No field should be empty")
            return redirect('/admin/form/')


@app.route('/admin/social/', methods=['POST', 'GET'])
def admin_social():
    if request.method == 'GET':
        social = SocialMedia.query.first()  # Assuming there's only one record in the SocialMedia table
        return render_template('admin/admin_form.html', social=social)  
    elif request.method == 'POST':
        x = request.form.get('x-url')
        github = request.form.get('github-url')
        linkedin = request.form.get('linkedin-url')
        instagram = request.form.get('instagram-url')
        thread = request.form.get('thread-url')

        if x != '' or github != '' or linkedin != '' or instagram != '' or thread != '':
            social = SocialMedia.query.first()
            if not social:
                social = SocialMedia()

            social.x_url = x
            social.github_url = github
            social.linkedin_url = linkedin
            social.instagram = instagram
            social.thread = thread

            db.session.add(social)
            db.session.commit()
            flash('Updated successfully')
            return redirect('/admin/social/')
        else:
            flash("No field should be empty")
            return redirect('/admin/social/')