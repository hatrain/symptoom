from flask import Flask, request, jsonify
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///symptom.db'
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=False)
class SymptomEpisode(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    date = db.Column(db.Date, nullable=False)
    symptom = db.Column(db.String(50), nullable=False)
    notes = db.Column(db.Text)
    severity = db.Column(db.Integer, nullable=False)

@app.route('/api/createuser', methods=['POST'])
def create_user():
    username = request.json.get('username')
    password = request.json.get('password')
    email = request.json.get('email')
    user = User(username=username, password=password, email=email)
    db.session.add(user)
    db.session.commit()
    return jsonify({'message': 'User created'})

@app.route('/api/authenticate', methods=['POST'])
def authenticate():
    username = request.json.get('username')
    password = request.json.get('password')
    user = User.query.filter_by(username=username, password=password).first()
    if user:
        return jsonify({'message': 'Authentication successful'})
    else:
        return jsonify({'message': 'Authentication failed'})

@app.route('/api/user', methods=['GET'])
def get_user_data():

    username = request.args.get('username')
    user = User.query.filter_by(username=username).first()
    if user:
        return jsonify({'username': user.username})
    else:
        return jsonify({'message': 'User not found'})

@app.route('/api/password', methods=['PUT'])
def update_user_password():
    username = request.json.get('username')
    new_password = request.json.get('new_password')
    user = User.query.filter_by(username=username).first()
    if user:
        user.password = new_password
        db.session.commit()
        return jsonify({'message': 'User password updated'})
    else:
        return jsonify({'message': 'User not found'})

@app.route('/api/add', methods=['POST'])
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

@app.route('/api/delete', methods=['DELETE'])
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

@app.route('/api/update', methods=['PUT'])
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

@app.route('/api/fullchart', methods=['GET'])
def get_all_symptom_episodes():
    username = request.args.get('username')
    user = User.query.filter_by(username=username).first()
    if user:
        symptom_episodes = SymptomEpisode.query.filter_by(user_id=user.id).all()
        result = [{'date': episode.date, 'symptom': episode.symptom, 'notes': episode.notes, 'severity': episode.severity} for episode in symptom_episodes]
        return jsonify(result)
    else:
        return jsonify({'message': 'User not found'})

@app.route('/api/search/range', methods=['GET'])
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

@app.route('/api/search/notes', methods=['GET'])
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

@app.route('/api/search/severity', methods=['GET'])
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
    with app.app_context():
        db.create_all()
    app.run(debug=True)