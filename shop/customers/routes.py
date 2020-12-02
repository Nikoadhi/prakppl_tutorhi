from flask import redirect, render_template, url_for, flash, request, session
from shop import db, app, photos, bcrypt
from .forms import CustomerForm, CustomerLoginForm
from .models import Register, Order
from flask_login import login_required, current_user, logout_user, login_user
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired
from werkzeug.utils import secure_filename
import secrets

@app.route('/customer/register', methods=['GET','POST'])
def customer_register():
    form = CustomerForm()
    if form.validate_on_submit():
        hash_password = bcrypt.generate_password_hash(form.password.data)
        register = Register(name=form.name.data, username=form.username.data, email=form.email.data,
                    password=hash_password, phone=form.phone.data, institution=form.institution.data,
                    major=form.major.data, semester=form.semester.data, birthday=form.birthday.data)
        db.session.add(register)
        db.session.commit()
        flash(f'Welcome, {form.name.data} Thanks for registering', 'success')
        return redirect(url_for('customer_login'))
    return render_template('customer/register.html', form=form)

@app.route('/customer/login', methods=['GET','POST'])
def customer_login():
    form = CustomerLoginForm()
    if request.method == "POST" and form.validate():
        user = Register.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user)
            next = request.args.get('next')
            return redirect(next or url_for('home'))
        flash('Incorrect email or password','danger')
        return redirect(url_for('customer_login'))
            
    return render_template('customer/login.html', form=form)

@app.route('/customer/logout', methods=['GET','POST'])
def customer_logout():
    logout_user()
    return redirect(url_for('customer_login'))

@app.route('/getorder')
@login_required
def get_order():
    if current_user.is_authenticated:
        customer_id = current_user.id
        invoice = secrets.token_hex(5)
        try:
            order = Order(invoice=invoice,customer_id=customer_id,orders=session['Shoppingcart'])
            db.session.add(order)
            db.session.commit()
            session.pop('Shoppingcart')
            flash('Your order has been sent successfully','success')
            return redirect(url_for('orders',invoice=invoice))
        except Exception as e:
            print(e)
            flash('Some thing went wrong while get order', 'danger')
            return redirect(url_for('getCart'))

@app.route('/orders/<invoice>')
@login_required
def orders(invoice):
    if current_user.is_authenticated:
        customer_id = current_user.id
        customer = Register.query.filter_by(id=customer_id).first()
        orders = Order.query.filter_by(customer_id=customer_id, invoice=invoice).order_by(Order.id.desc()).first()
        for _key, course in orders.orders.items():
            total = float(course['price'])
    else:
        return redirect(url_for('customer_login'))
    return render_template('customer/order.html', invoice=invoice, total=total, customer=customer, orders=orders)
