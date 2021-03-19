
import os
from voterlogin import *
# from candidates import *
from flask import Flask, session, render_template, request, redirect, url_for, jsonify
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import exc, or_, and_
from werkzeug.security import check_password_hash, generate_password_hash
import json

os.environ["DATABASE_URL"] = "postgres://fldsfqxmwyfgge:5ed5a007b5e126dae5bc744246856a8fd72e20e8b87b6d5512356721ee553331@ec2-52-21-252-142.compute-1.amazonaws.com:5432/d2qc1vldgm7o0s"


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db.init_app(app)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
app.config.from_object(__name__)
Session(app)

app.config["TEMPLATES_AUTO_RELOAD"] = True

engine = create_engine(os.getenv("DATABASE_URL"))
db1 = scoped_session(sessionmaker(bind=engine))


@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        uname = request.form.get("username")
        password = request.form.get("password")
        queryres = voterlogin.query.filter_by(username=uname).first()
        if queryres is None:
            me = voterlogin(uname, password, False)
            db.session.add(me)
            db.session.commit()
            session["user"] = uname
            return redirect(f"/votehome/{uname}")
        elif queryres.voted is False:
            session["user"] = uname
            return redirect(f"/votehome/{uname}")
        else:
            if uname == "admin":
                return redirect("admin")
            # flash("You have already casted your vote.")
            return redirect("/")
    return render_template("login.html")


@app.route("/logout")
def logout():
    session.pop("user", None)
    return render_template("login.html")


@app.route("/votehome/<string:username>", methods=["GET", "POST"])
def votehome(username):
    if request.method == "POST":
        can = request.form.get("type")
        print(request.form.get("type"))
        candidate = candidates.query.filter_by(candidate_name=can).first()
        print(candidate)
        voter = voterlogin.query.filter_by(username=username).first()
        candidate.votes = candidate.votes + 1
        voter.voted = True
        db.session.add(candidate)
        db.session.add(voter)
        db.session.commit()
        return redirect("/logout")
    else:
        print(session["user"])
        if "user" in session:
            user = session["user"]
            candidate = candidates.query.all()
            return render_template("home.html", candidates=candidate, username=username)
        else:
            # flash("Login with the credentails.")
            return render_template("login.html")


@app.route("/admin")
def admin():
    user = candidates.query.all()
    return render_template("admin.html", users=user)
