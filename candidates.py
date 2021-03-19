import os

from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class candidates(db.Model):
    __tablename__ = "candidates"
    candidate_name = db.Column(db.String, primary_key=True)
    votes = db.Column(db.Integer, nullable=True)

    def __init__(self, names, votes):
        self.candidate_name = names
        self.votes = votes
