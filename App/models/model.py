from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import check_password_hash, generate_password_hash

db = SQLAlchemy()

class User(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  username = db.Column(db.String(80), unique=True, nullable=False)
  password = db.Column(db.String(120), nullable=False)

  def __init__(self, username, password):
    self.username= username
    self.set_password(password)

  def set_password(self, password):
    self.password = generate_password_hash(password)

  def check_password(self, password):
    return check_password_hash(self.password, password)

class Student(db.Model):
  id = db.Column(db.String(9), primary_key=True)
  first_name = db.Column(db.String(80), nullable=False)
  last_name = db.Column(db.String(80), nullable=False)
  image = db.Column(db.String(80), nullable=True)
  programme = db.Column(db.String(80), nullable=False)
  faculty = db.Column(db.String(80), nullable=False)
  gpa = db.Column(db.String(80), nullable=True)
  info = db.Column(db.String(80), nullable=False)
  email = db.Column(db.String(80), nullable=True)


  def __init__(self, id, first_name, last_name, image, programme, faculty, gpa, info, email):
    self.id = id
    self.first_name = first_name
    self.last_name = last_name
    self.image = image
    self.programme = programme
    self.faculty = faculty
    self.gpa = gpa
    self.info = info
    self.email = email


class Company(db.Model):
  id = db.Column(db.String(9), primary_key=True)
  name = db.Column(db.String(80), nullable=False)
  location = db.Column(db.String(120), nullable=False)
  description = db.Column(db.String(120), nullable=False)
  email = db.Column(db.String(120), nullable=False)
  contact = db.Column(db.String(120), nullable=False)

  def __init__(self, id, name, location, description, email, contact):
    self.id = id
    self.name = name
    self.location = location
    self.description = description
    self.email = email
    self.contact = contact


class Internship(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  company_id = db.Column(db.String(9), db.ForeignKey('company.id'), nullable=False)
  description = db.Column(db.String(120), nullable=False)
  title = db.Column(db.String(120), nullable=False)
  deadline = db.Column(db.String(120), nullable=False)
  start_period = db.Column(db.String(120), nullable=False)
  end_period = db.Column(db.String(120), nullable=False)

  def __init__(self, company_id, description, deadline, start_period, end_period):
    self.course_id = company_id
    self.description = description
    self.deadline = deadline
    self.start_period = start_period
    self.end_period = end_period