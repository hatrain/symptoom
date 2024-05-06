from flask import Flask, request, jsonify, session
from flask_bcrypt import Bcrypt
from flask_session import Session
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin
from config import ApplicationConfig
from models import db, user
from flask_cors import CORS

app = Flask(__name__)
CORS(app, supports_credentials=True)
bcrypt = Bcrypt(app)
app.config.from_object(ApplicationConfig)
db.init_app(app)
server_session = Session(app)

#TODO: add migrate functions
#migrate = Migrate(app, db)
login = LoginManager(app)


class User(UserMixin, db.Model):
    __tablename__ = "users" #for table name
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(30), nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=False)

class SymptomEpisode(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    date = db.Column(db.Date, nullable=False)
    symptom = db.Column(db.String(50), nullable=False)
    notes = db.Column(db.Text)
    severity = db.Column(db.Integer, nullable=False)

@login.user_loader
def load_user(user_id):
    return User.get(user_id)

@app.route('/status', methods=['GET'])
def get_api_status():
    return jsonify({'status': 'API is running'})

#TODO: add human verification for creating user
@app.route('/createuser', methods=['POST'])
def create_user():
    username = request.json.get('username')
    password = request.json.get('password')
    email = request.json.get('email')
    user_email_exists = User.query.filter_by(email=email).first()
    if user_email_exists:
        return jsonify({"error": "User already exists"}), 409
    user_username_exists = User.query.filter_by(username=username).first()
    if user_username_exists:
        return jsonify({"error": "User already exists"}), 409
    hashed_password = bcrypt.generate_password_hash(password)
    user = User(username=username, password=hashed_password, email=email)
    db.session.add(user)
    db.session.commit()
    return jsonify({
        "id": user.id,
        "email": user.email
    })

@app.route('/authenticate', methods=['POST'])
def authenticate():
    #TODO: rewrite this to use flask-login
    #TODO: return session token for future requests
    email = request.json["email"]
    password = request.json('password')
    user = User.query.filter_by(email=email).first()

    if user is None:
        return jsonify({"error": "Unauthorized"}), 401

    if not bcrypt.check_password_hash(user.password, password):
        return jsonify({"error": "Unauthorized"}), 401
    
    session["user_id"] = user.id
    return jsonify({
        "id": user.id,
        "username": user.username,
        "email": user.email
    })

@app.route("/logout", methods=["POST"])
def logout_user():
    session.pop("user_id")
    return "200"

@app.route("/@me")
def get_current_user():
    user_id = session.get("user_id")

    if not user_id:
        return jsonify({"error": "Unauthorized"}), 401
    
    user = User.query.filter_by(id=user_id).first()
    return jsonify({
        "id": user.id,
        "email": user.email
    }) 

#only authenticated users should be able to access this method
@app.route('/password', methods=['PUT'])
def update_user_password():
    #TODO: make sure the data is hashed before proceeding
    username = request.json.get('username')
    new_password = request.json.get('new_password')
    user = User.query.filter_by(username=username).first()
    if user:
        user.password = new_password
        db.session.commit()
        return jsonify({'message': 'User password updated'})
    else:
        return jsonify({'message': 'User not found'})

#only authenticated users should be able to access this method
@app.route('/add', methods=['POST'])
def add_symptom_episode():
    username = request.json.get('username')
    date = request.json.get('date')
    symptom = request.json.get('symptom')
    notes = request.json.get('notes')
    severity = request.json.get('severity')
    user = User.query.filter_by(username=username).first()
    if user:
        symptom_episode = SymptomEpisode(user_id=user.id, date=date, symptom=symptom, notes=notes, severity=severity)
        db.session.add(symptom_episode)
        db.session.commit()
        return jsonify({'message': 'Symptom episode added'})
    else:
        return jsonify({'message': 'User not found'})

#only authenticated users should be able to access this method
@app.route('/delete', methods=['DELETE'])
def delete_symptom_episode():
    username = request.json.get('username')
    episode_id = request.json.get('episode_id')
    user = User.query.filter_by(username=username).first()
    if user:
        symptom_episode = SymptomEpisode.query.filter_by(user_id=user.id, id=episode_id).first()
        if symptom_episode:
            db.session.delete(symptom_episode)
            db.session.commit()
            return jsonify({'message': 'Symptom episode deleted'})
        else:
            return jsonify({'message': 'Symptom episode not found'})
    else:
        return jsonify({'message': 'User not found'})

#only authenticated users should be able to access this method
@app.route('/update', methods=['PUT'])
def update_symptom_episode():
    username = request.json.get('username')
    episode_id = request.json.get('episode_id')
    date = request.json.get('date')
    symptom = request.json.get('symptom')
    notes = request.json.get('notes')
    severity = request.json.get('severity')
    user = User.query.filter_by(username=username).first()
    if user:
        symptom_episode = SymptomEpisode.query.filter_by(user_id=user.id, id=episode_id).first()
        if symptom_episode:
            symptom_episode.date = date
            symptom_episode.symptom = symptom
            symptom_episode.notes = notes
            symptom_episode.severity = severity
            db.session.commit()
            return jsonify({'message': 'Symptom episode updated'})
        else:
            return jsonify({'message': 'Symptom episode not found'})
    else:
        return jsonify({'message': 'User not found'})

#only authenticated users should be able to access this method
@app.route('/fullchart', methods=['GET'])
def get_all_symptom_episodes():
    username = request.args.get('username')
    user = User.query.filter_by(username=username).first()
    if user:
        symptom_episodes = SymptomEpisode.query.filter_by(user_id=user.id).all()
        result = [{'date': episode.date, 'symptom': episode.symptom, 'notes': episode.notes, 'severity': episode.severity} for episode in symptom_episodes]
        return jsonify(result)
    else:
        return jsonify({'message': 'User not found'})

#only authenticated users should be able to access this method
@app.route('/search/range', methods=['GET'])
def get_symptom_episodes_in_range():
    username = request.args.get('username')
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    user = User.query.filter_by(username=username).first()
    if user:
        symptom_episodes = SymptomEpisode.query.filter_by(user_id=user.id).filter(SymptomEpisode.date.between(start_date, end_date)).all()
        result = [{'date': episode.date, 'symptom': episode.symptom, 'notes': episode.notes, 'severity': episode.severity} for episode in symptom_episodes]
        return jsonify(result)
    else:
        return jsonify({'message': 'User not found'})

#only authenticated users should be able to access this method
@app.route('/search/notes', methods=['GET'])
def get_symptom_episodes_by_notes():
    username = request.args.get('username')
    notes = request.args.get('notes')
    user = User.query.filter_by(username=username).first()
    if user:
        symptom_episodes = SymptomEpisode.query.filter_by(user_id=user.id, notes=notes).all()
        result = [{'date': episode.date, 'symptom': episode.symptom, 'notes': episode.notes, 'severity': episode.severity} for episode in symptom_episodes]
        return jsonify(result)
    else:
        return jsonify({'message': 'User not found'})

#only authenticated users should be able to access this method
@app.route('/search/severity', methods=['GET'])
def get_symptom_episodes_by_severity():
    username = request.args.get('username')
    severity = request.args.get('severity')
    user = User.query.filter_by(username=username).first()
    if user:
        symptom_episodes = SymptomEpisode.query.filter_by(user_id=user.id, severity=severity).all()
        result = [{'date': episode.date, 'symptom': episode.symptom, 'notes': episode.notes, 'severity': episode.severity} for episode in symptom_episodes]
        return jsonify(result)
    else:
        return jsonify({'message': 'User not found'})

if __name__ == '__main__':
    app.run(debug=True)