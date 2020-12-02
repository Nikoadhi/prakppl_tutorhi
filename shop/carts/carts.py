from flask import redirect, render_template, url_for, flash, request, session
from shop import db, app
from shop.products.models import Addcourse

@app.route('/addcart', methods=['POST'])
def AddCart():
    try:
        course_id = request.form.get('course_id')
        course = Addcourse.query.filter_by(id=course_id).first()
        if course_id and request.method == 'POST':
            DictItems = {course_id:{'name':course.name, 'price':course.price, 'image':course.image_1}}

            if 'Shopcart' in session:
                print(session['Shoppingcart'])
            else:
                session['Shoppingcart'] = DictItems
        return redirect(request.referrer)

    except Exception as e:
        print(e)
    finally:
        return redirect(request.referrer)

@app.route('/carts')
def getCart():
    if 'Shoppingcart' not in session:
        return redirect(request.referrer)

    total = 0
    for key, course in session['Shoppingcart'].items():
        total = float(course['price'])

    return render_template('products/carts.html', total=total)

@app.route('/deleteitem/<int:id>')
def deleteitem(id):
    if 'Shoppingcart' not in session or len(session['Shoppingcart']) <= 0:
        return redirect(url_for('home'))
    try:
        session.modified = True
        for key , item in session['Shoppingcart'].items():
            if int(key) == id:
                session['Shoppingcart'].pop(key, None)
                return redirect(url_for('getCart'))
    except Exception as e:
        print(e)
        return redirect(url_for('getCart'))