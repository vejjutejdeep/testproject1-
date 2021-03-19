from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class voterlogin(db.Model):
    __tablename__ = "voterlogin"
    username = db.Column(db.String, primary_key=True)
    password = db.Column(db.String, nullable=False)
    voted = db.Column(db.Boolean, nullable=False)

    def __init__(self, unames, password, voted):
        self.username = unames
        self.password = password
        self.voted = voted


class candidates(db.Model):
    __tablename__ = "candidates"
    candidate_name = db.Column(db.String, primary_key=True)
    votes = db.Column(db.Integer, nullable=True)

    def __init__(self, names, votes):
        self.candidate_name = names
        self.votes = votes
