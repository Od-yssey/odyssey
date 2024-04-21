from werkzeug.security import check_password_hash, generate_password_hash
from App.database import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username =  db.Column(db.String, nullable=False, unique=True)
    password = db.Column(db.String(120), nullable=False)
    type = db.Column(db.String(50))
    __mapper_args__ = {'polymorphic_identity': 'user', 'polymorphic_on': type}

    def __init__(self, username, password, type):
        self.username = username
        self.set_password(password)
        self.type = type

    def get_json(self):
        return{
            'id': self.id,
            'username': self.username
        }

    def set_password(self, password):
        """Create hashed password."""
        self.password = generate_password_hash(password)
    
    def check_password(self, password):
        """Check hashed password."""
        return check_password_hash(self.password, password)

class Student(User):
    __tablename__ = 'student'
    __mapper_args__ = {
        'polymorphic_identity': 'student',
    }
    student_id = db.Column(db.String(9), primary_key=True)
    first_name = db.Column(db.String(80), nullable=False)
    last_name = db.Column(db.String(80), nullable=False)
    image = db.Column(db.String(80), nullable=True)
    programme = db.Column(db.String(80), nullable=False)
    faculty = db.Column(db.String(80), nullable=False)
    gpa = db.Column(db.String(80), nullable=True)
    info = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(80), nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))  # Establishing Foreign Key Relationship
    
    def __init__(self, student_id, first_name, last_name, image, programme, faculty, gpa, info, email, username, password):
        super().__init__(username, password, type='student')
        self.student_id = student_id
        self.first_name = first_name
        self.last_name = last_name
        self.image = image
        self.programme = programme
        self.faculty = faculty
        self.gpa = gpa
        self.info = info
        self.email = email

class Company(User):
    __tablename__ = 'company'
    __mapper_args__ = {
        'polymorphic_identity': 'company'
    }
    company_id = db.Column(db.String(9), primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    location = db.Column(db.String(120), nullable=False)
    description = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    contact = db.Column(db.String(120), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id')) 

    def __init__(self, company_id, name, location, description, email, contact, username, password):
        super().__init__(username, password, type='company')
        self.company_id = company_id
        self.name = name
        self.location = location
        self.description = description
        self.email = email
        self.contact = contact

class Admin(User):
    __tablename__ = 'admin'
    __mapper_args__ = {
        'polymorphic_identity': 'admin'
    }
    admin_id = db.Column(db.String(9), primary_key=True)
    admin_name = db.Column(db.String(80), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    
    def __init__(self, admin_id, admin_name, username, password):
        super()._init_(username, password, type='admin')
        self.admin_id = admin_id
        self.admin_name = admin_name

class Internship(db.Model):
    __tablename__  = 'internship'
    id = db.Column(db.Integer, primary_key=True)
    company_id = db.Column(db.String(9), db.ForeignKey('company.company_id'), nullable=False)
    description = db.Column(db.String(120), nullable=False)
    title = db.Column(db.String(120), nullable=False)
    deadline = db.Column(db.String(120), nullable=False)
    start_period = db.Column(db.String(120), nullable=False)
    end_period = db.Column(db.String(120), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    
    def _init_(self, company_id, description, title, deadline, start_period, end_period):
        self.company_id = company_id
        self.description = description
        self.title = title
        self.deadline = deadline
        self.start_period = start_period
        self.end_period = end_period

class StudentInternship(db.Model):
    __tablename__ = 'studentinternship'
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.String(9), db.ForeignKey('student.student_id'), nullable=False)
    internship_id = db.Column(db.Integer, db.ForeignKey('internship.id'), nullable=False)
    status = db.Column(db.String(50), nullable=False)  

    student = db.relationship('Student', backref=db.backref('internships', lazy=True))
    internship = db.relationship('Internship', backref=db.backref('students', lazy=True))

    def __init__(self, student_id, internship_id, status):
        self.student_id = student_id
        self.internship_id = internship_id
        self.status = status