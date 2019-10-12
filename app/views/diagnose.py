from flask import request, render_template, abort, jsonify
from flask.ext.login import login_required, current_user
import time

from app import app, models, db
from app.predict_api import PredictAPI

@app.route('/diagnose')
@login_required
def diagnose():

    diagnoses = current_user.diagnoses
    return render_template('diagnose.html', diagnoses=diagnoses)

@app.route('/diagnose/img/<id>')
@login_required
def get_diagnose_img(id):
    """
    Renders the image for the diagnosis as a URL

    :param id:  The ID of the diagnosis to fetch the image for
    :return:    The image returned to the URL
    """

    for diagnosis in current_user.diagnoses:
        if (diagnosis.id == int(id)):
            return app.response_class(diagnosis.img, mimetype='application/octet-stream')

    abort(404)

@app.route('/diagnose/predict', methods=['POST'])
@login_required
def predict():

    if current_user.credits <= 0:
        return jsonify({
            "success": False,
            "error": "Not Enough Credits, Please Buy More."
        })

    if 'file' not in request.files:
        return jsonify({
            "success": False,
            "error": "No image was uploaded. Please select an image and try again"
        })
    else:
        file = request.files['file']
        app.logger.debug(f"File uploaded for prediction: {file.filename}")

        # Initalise prediction class
        model = PredictAPI()
        predict_class, predict_certainty = model.predict(file)
        file.seek(0)

        prediction = models.Diagnosis(
            uid=current_user.email,
            time=int(time.time()),
            filename=file.filename,
            img=file.read(),
            prediction=predict_class,
            certainty=predict_certainty
        )

        # Insert the diagnosis in the database
        db.session.add(prediction)
        current_user.use_credit()
        db.session.commit()

        return jsonify({
            "success": True,
            "id": prediction.id,
            "filename": prediction.filename,
            "prediction": prediction.title,
            "certainty": prediction.certainty,
            "url": prediction.url,
            "credits_left": current_user.credits
        })