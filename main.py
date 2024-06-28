
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///club_fitting.db'
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    email = db.Column(db.String(120))
    shots = db.relationship('Shot', backref='user')

class Shot(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    club_model_id = db.Column(db.Integer, db.ForeignKey('club_model.id'))
    club_head_speed = db.Column(db.Float)
    ball_speed = db.Column(db.Float)
    launch_angle = db.Column(db.Float)
    spin_rate = db.Column(db.Float)
    peak_height = db.Column(db.Float)
    land_angle = db.Column(db.Float)
    club_path = db.Column(db.Float)
    club_face_angle = db.Column(db.Float)
    attack_angle = db.Column(db.Float)
    ft_off_line = db.Column(db.Float)

class ClubModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    loft_sleeve_adjustments = db.Column(db.String(120))
    sliding_weight_adjustments = db.Column(db.String(120))
    shots = db.relationship('Shot', backref='club_model')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/results', methods=['POST'])
def results():
    user_name = request.form['name']
    user_email = request.form['email']

    new_user = User(name=user_name, email=user_email)
    db.session.add(new_user)
    db.session.commit()

    club_model_name = request.form['club_model']
    club_model = ClubModel.query.filter_by(name=club_model_name).first()

    shots = []
    for i in range(1, 4):
        club_head_speed = request.form[f'club_head_speed_{i}']
        ball_speed = request.form[f'ball_speed_{i}']
        launch_angle = request.form[f'launch_angle_{i}']
        spin_rate = request.form[f'spin_rate_{i}']
        peak_height = request.form[f'peak_height_{i}']
        land_angle = request.form[f'land_angle_{i}']
        club_path = request.form[f'club_path_{i}']
        club_face_angle = request.form[f'club_face_angle_{i}']
        attack_angle = request.form[f'attack_angle_{i}']
        ft_off_line = request.form[f'ft_off_line_{i}']

        new_shot = Shot(
            user_id=new_user.id,
            club_model_id=club_model.id,
            club_head_speed=club_head_speed,
            ball_speed=ball_speed,
            launch_angle=launch_angle,
            spin_rate=spin_rate,
            peak_height=peak_height,
            land_angle=land_angle,
            club_path=club_path,
            club_face_angle=club_face_angle,
            attack_angle=attack_angle,
            ft_off_line=ft_off_line
        )
        shots.append(new_shot)

    db.session.add_all(shots)
    db.session.commit()

    club_adjustments = ...  # Implement the logic to recommend club adjustments

    return render_template('results.html', club_adjustments=club_adjustments)

@app.route('/club_models/<int:club_model_id>/shots')
def club_model_shots(club_model_id):
    shots = Shot.query.filter_by(club_model_id=club_model_id).all()
    return jsonify([shot.to_dict() for shot in shots])

if __name__ == '__main__':
    app.run(debug=True)
