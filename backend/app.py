from flask import Flask, request, jsonify, session
from flask_bcrypt import Bcrypt
from flask_cors import CORS, cross_origin
from flask_session import Session
from config import ApplicationConfig
from models import db, Patient, Medical, TBHistory
import datetime

app = Flask(__name__)
app.config.from_object(ApplicationConfig)

bcrypt = Bcrypt(app)
CORS(app, supports_credentials=True)
server_session = Session(app)
db.init_app(app)

with app.app_context():
    db.create_all()


@app.route("/@me")
def get_current_patient():
    patient_id = session.get("patient_id")

    if not patient_id:
        return jsonify({"error": "Unauthorized"}), 401
    
    patient = Patient.query.filter_by(id=patient_id).first()
    dataone = Medical.query.filter_by(id=patient_id).first() 

    return jsonify({
        "id": patient.id,
        "email": patient.email,
        "heartrate": dataone.heartrate,
        "bloodpressure": dataone.bloodpressure
    }) 

@app.route("/@me/update", methods=["POST"])
def update_patient_details():
    patient_id = session.get("patient_id")
    heartrate = request.json["heartrate"]
    bloodpressure = request.json["bloodpressure"]

    if not patient_id:
        return jsonify({"error": "Unauthorized"}), 401
    
    dataone = Medical.query.filter_by(id=patient_id).first()
    dataone.heartrate=heartrate
    dataone.bloodpressure=bloodpressure

    db.session.commit()
    # datatwo = TBHistory.query.filter_by(id=patient_id).first()

    return jsonify({
        "id": dataone.id,
        "heartrate": dataone.heartrate,
        "bloodpressure": dataone.bloodpressure
    }) 

@app.route("/register", methods=["POST"])
def register_patient():
    email = request.json["email"]
    password = request.json["password"]
    heartrate = request.json["heartrate"]
    bloodpressure = request.json["bloodpressure"]

    patient_exists = Patient.query.filter_by(email=email).first() is not None

    if patient_exists:
        return jsonify({"error": "Patient already exists"}), 409

    hashed_password = bcrypt.generate_password_hash(password)
    new_patient = Patient(email=email, password=hashed_password)
    db.session.add(new_patient)
    db.session.commit()

    new_medical = Medical(id=new_patient.id, heartrate=heartrate, bloodpressure=bloodpressure)
    db.session.add(new_medical)
    db.session.commit()
    
    session["patient_id"] = new_patient.id

    return jsonify({
        "id": new_patient.id,
        "email": new_patient.email,
        "heartrate": new_medical.heartrate,
        "bloodpressure": new_medical.bloodpressure
    })

@app.route("/login", methods=["POST"])
def login_patient():
    email = request.json["email"]
    password = request.json["password"]

    patient = Patient.query.filter_by(email=email).first()
    session["patient_id"] = patient.id
    dataone = Medical.query.filter_by(id=patient.id).first() 

    if patient is None:
        return jsonify({"error": "Unauthorized"}), 401

    if not bcrypt.check_password_hash(patient.password, password):
        return jsonify({"error": "Unauthorized"}), 401

    return jsonify({
        "id": patient.id,
        "email": patient.email,
        "heartrate": dataone.heartrate,
        "bloodpressure": dataone.bloodpressure
    })

@app.route("/sethistory", methods=["POST"])
def set_tbhistory():
    patient_id = session.get("patient_id")
    tbval = request.json["tbval"]


    if not patient_id:
        return jsonify({"error": "Unauthorized"}), 401

    new_record = TBHistory(id=None, tbval=tbval, date=datetime.datetime.utcnow(), patient_id=patient_id)
    db.session.add(new_record)
    db.session.commit()

    return jsonify({
        "id": new_record.id,
        "tbval": tbval,
        "date": str(new_record.date.isoformat()),
        "patient_id": new_record.patient_id
    }) 

@app.route("/gethistory", methods=["GET"])
def get_tbhistory():
    patient_id = session.get("patient_id")

    if not patient_id:
        return jsonify({"error": "Unauthorized"}), 401
    
    # patient = Patient.query.filter_by(id=patient_id).first()
    patient_history = TBHistory.query.all()

    patient_history_dict = []
    for history in patient_history:
        entry = {
            "id": history.id,
            "tbval": history.tbval,
            "date": str(history.date.isoformat()),
            "patient_id": history.patient_id
        }
        patient_history_dict.append(entry)
    return jsonify(patient_history_dict) 

@app.route("/logout", methods=["POST"])
def logout_patient():
    session.pop("patient_id")
    return "200"

if __name__ == "__main__":
    app.run(debug=True)


# redis deployment figure out 
# postgres sql?
# table in table