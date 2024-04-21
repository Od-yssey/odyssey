import csv
from flask import Blueprint, redirect, render_template, request, send_from_directory, jsonify
from App.models import db
from App.controllers import create_user

index_views = Blueprint('index_views', __name__, template_folder='../templates')

def parse_students():
   with open('students.csv', mode='r', encoding='utf-8') as file:
     csv_reader = csv.DictReader(file)
     for row in csv_reader:
       student = Student(student_id=row['ID'],
                         first_name=row['FirstName'],
                         image=row['Picture'],
                         last_name=row['LastName'],
                         programme=row['Program'],
                         faculty=row['Faculty'],
                         gpa=row['GPA'],
                         info=row['Info'],
                        email=row['Email'],
                        username=row['ID'],
                        password = row['ID'])
       db.session.add(student)
     db.session.commit()

def parse_companies():
  with open('company.csv', mode='r', encoding='utf-8') as file:
    csv_reader = csv.DictReader(file)
    for row in csv_reader:
      company = Company(company_id=row['ID'],
                         name=row['Company_Name'],
                         location=row['Location'],
                         description=row['Description'],
                         email=row['Email'],
                         contact=row['Contact'],
                         username=row['ID'],
                         password = row['ID'])
      db.session.add(company)
    db.session.commit()

def parse_internships():
    with open('internship.csv', mode='r', encoding='utf-8') as file:
        csv_reader = csv.DictReader(file)
        for row in csv_reader:
            internship = Internship(
                company_id=row['Company_ID'],
                description=row['Description'],
                title=row['Title'],
                deadline=row['Deadline'],
                start_period=row['Start_Period'],
                end_period=row['End_Period']
            )
            db.session.add(internship)
        db.session.commit()


@index_views.route('/', methods=['GET'])
def index_page():
    return render_template('index.html')

@index_views.route('/init', methods=['GET'])
def init():
    db.drop_all()
    db.create_all()
    create_user('bob', 'bobpass')
    parse_students()
    parse_companies()
    parse_internships()
    return jsonify(message='db initialized!')

@index_views.route('/health', methods=['GET'])
def health_check():
    return jsonify({'status':'healthy'})
