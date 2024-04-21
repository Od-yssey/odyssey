import click, pytest, sys, csv
from flask import Flask
from flask.cli import with_appcontext, AppGroup

from App.database import db, get_migrate
from App.main import create_app
from App.controllers import ( create_user, get_all_users_json, get_all_users )
from App.models import *

# This commands file allow you to create convenient CLI commands for testing controllers

app = create_app()
migrate = get_migrate(app)

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

# This command creates and initializes the database
@app.cli.command("init", help="Creates and initializes the database")
def initialize():
    db.drop_all()
    db.create_all()
    create_user('bob', 'bobpass','admin')
    parse_students()
    parse_companies()
    print('database intialized')

'''
User Commands
'''

# Commands can be organized using groups

# create a group, it would be the first argument of the comand
# eg : flask user <command>
user_cli = AppGroup('user', help='User object commands') 

# Then define the command and any parameters and annotate it with the group (@)
@user_cli.command("create", help="Creates a user")
@click.argument("username", default="rob")
@click.argument("password", default="robpass")
def create_user_command(username, password):
    create_user(username, password)
    print(f'{username} created!')

# this command will be : flask user create bob bobpass

@user_cli.command("list", help="Lists users in the database")
@click.argument("format", default="string")
def list_user_command(format):
    if format == 'string':
        print(get_all_users())
    else:
        print(get_all_users_json())

app.cli.add_command(user_cli) # add the group to the cli

'''
Test Commands
'''

test = AppGroup('test', help='Testing commands') 

@test.command("user", help="Run User tests")
@click.argument("type", default="all")
def user_tests_command(type):
    if type == "unit":
        sys.exit(pytest.main(["-k", "UserUnitTests"]))
    elif type == "int":
        sys.exit(pytest.main(["-k", "UserIntegrationTests"]))
    else:
        sys.exit(pytest.main(["-k", "App"]))
    

app.cli.add_command(test)