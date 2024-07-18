from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///school.db'
db = SQLAlchemy(app)

# Model definitions for User, Principal, Student, Teacher, and Assignment

def validate_principal(request):
    # Implement logic to validate X-Principal header and check if user is a principal
    pass

@app.route('/principal/assignments', methods=['GET'])
def get_principal_assignments():
    principal_id = validate_principal(request)  # Extract principal_id from header
    # Query database for assignments
    assignments = Assignment.query.filter(Assignment.state.in_(['SUBMITTED', 'GRADED'])).all()
    return jsonify({'data': [assignment.to_dict() for assignment in assignments]})

@app.route('/principal/teachers', methods=['GET'])
def get_principal_teachers():
    principal_id = validate_principal(request)  # Extract principal_id from header
    # Query database for teachers
    teachers = Teacher.query.all()
    return jsonify({'data': [teacher.to_dict() for teacher in teachers]})

@app.route('/principal/assignments/grade', methods=['POST'])
def grade_assignment():
    principal_id = validate_principal(request)  # Extract principal_id from header
    data = request.get_json()
    assignment_id = data.get('id')
    grade = data.get('grade')
    # Query database for assignment, update grade, and save
    assignment = Assignment.query.get(assignment_id)
    assignment.grade = grade
    assignment.state = 'GRADED'
    db.session.commit()
    return jsonify({'data': assignment.to_dict()})
