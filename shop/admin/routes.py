from flask import render_template, session, request, redirect, url_for, flash

from shop import app, db, bcrypt
from .forms import AdminForm, LoginForm
from .models import Admin
from shop.products.models import Addcourse
import os

@app.route('/admin')
def admin():
    if 'email' not in session:
        flash(f'Please Login First', 'danger')
        return redirect(url_for('login'))
    courses = Addcourse.query.all()
    return render_template('admin/index.html', title='Admin page', courses=courses)

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = AdminForm(request.form)
    
    if request.method == 'POST' and form.validate():
        hash_password = bcrypt.generate_password_hash(form.password.data)
        admin = Admin(name=form.name.data, username=form.username.data, email=form.email.data,
                    password=hash_password)
        db.session.add(admin)
        db.session.commit()
        flash(f'Welcome, {form.name.data} Thanks for registering', 'success')
        return redirect(url_for('home'))
    return render_template('admin/register.html', form=form, title="Registration Page")

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm(request.form)
    if request.method == "POST" and form.validate():
        admin = Admin.query.filter_by(email = form.email.data).first()
        if admin and bcrypt.check_password_hash(admin.password, form.password.data):
            session['email'] = form.email.data
            flash(f'Welcome Admin {form.email.data}', 'success')
            return redirect(url_for('admin'))
        else:
            flash('Wrong Password', 'danger')

    return render_template('admin/login.html', form=form, title='Login Page')

@app.route('/about', methods=['GET', 'POST'])
def about():
    return render_template('admin/about.html', title='about')