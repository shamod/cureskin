from flask import render_template, flash
from app import app
from app.forms import contact as contact_forms

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', title='Your Personal 24/7 Dermatologist')

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    form = contact_forms.ContactUs()
    if form.validate_on_submit():
        flash('Your Message Has Been Sent To The Team', 'positive')

    return render_template('contact.html', form=form, title='Contact Us')
