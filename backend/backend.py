from flask import Flask, request, jsonify, session
from flask_bcrypt import Bcrypt
from flask_session import Session
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin
from config import ApplicationConfig

app = Flask(__name__)
bcrypt = Bcrypt(app)
app.config.from_object(ApplicationConfig)
db = SQLAlchemy(app)
server_session = Session(app)
login = LoginManager(app)

class User(UserMixin, db.Model):
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

@app.route('/status', methods=['GET'])
def get_api_status():
    return jsonify({'status': 'API is running'})

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