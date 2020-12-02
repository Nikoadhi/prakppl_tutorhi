from flask import redirect, render_template, url_for, flash, request, session
from shop import db, app, photos
from .models import Addcourse
from .forms import Addcourses
 


@app.route('/')
def home():
    courses = Addcourse.query.filter(Addcourse.price > 0)
    return render_template('products/index.html', courses=courses) 

@app.route('/course/<int:id>')
def single_page(id):
    course = Addcourse.query.get_or_404(id)
    return render_template('products/single_page.html', course=course)

@app.route('/addcourse', methods=['GET','POST'])
def addcourse():
    form = Addcourses(request.form)
    if 'email' not in session:
        flash(f'Please Login First', 'danger')
        return redirect(url_for('login'))
    if request.method=="POST":
        name = form.name.data
        price = form.price.data
        description = form.description.data
        image_1 = photos.save(request.files.get('image_1'))
        image_2 = photos.save(request.files.get('image_2'))

        addcourse = Addcourse(name=name, price=price, description=description, image_1=image_1, image_2=image_2)
        db.session.add(addcourse)
        flash(f'The course {name} was added in the database','success')
        db.session.commit()

    return render_template('products/addcourse.html', form=form, title='Add Course')

@app.route('/deletecourse/<int:id>', methods=['POST'])
def deletecourse(id):
    course = Addcourse.query.get_or_404(id)
    if request.method =="POST":
        try:
            os.unlink(os.path.join(current_app.root_path, "static/images/" + course.image_1))
            os.unlink(os.path.join(current_app.root_path, "static/images/" + course.image_2))
            os.unlink(os.path.join(current_app.root_path, "static/images/" + course.image_3))
        except Exception as e:
            print(e)

        db.session.delete(course)
        db.session.commit()
        flash(f'{course.name} deleted','success')
        return redirect(url_for('admin'))
    flash(f'Can not delete','danger')
    return redirect(url_for('admin'))