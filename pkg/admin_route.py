from flask import Flask, render_template, url_for, redirect, request, session, flash
from pkg import app
from pkg.models import User, db

@app.route('/user_management/')
def user_management():
    user = User.query.all()
    if request.method == 'GET':
        return render_template('admin/user_management.html', user=user)
    else:
        pass