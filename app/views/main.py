from flask import render_template, flash, request
from flask.ext.login import login_required
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

@app.route('/diagnose', methods=['POST', 'GET'])
@login_required
def diagnose():
    if request.method == 'POST':
        filecount=0
        for key, f in request.files.items():
            if key.startswith('file'):
                filecount += 1
                f.save(os.path.join(app.config['UPLOADED_PATH'], f.filename))

        flash(f"Uploaded {filecount} files")
        return redirect(url_for('diagnose'))
    return render_template('user/diagnose.html', key=stripe_keys['publishable_key'])
