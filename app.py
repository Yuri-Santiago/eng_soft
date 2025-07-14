from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flasgger import Swagger
from os import environ

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = environ.get('DATABASE_URL', 'sqlite:///engsoft.db')
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)
swagger = Swagger(app)

class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    course = db.Column(db.String(100), nullable=False)

    def to_dict(self):
        return {"id": self.id, "name": self.name, "age": self.age, "course": self.course}
    
class Teacher(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    department = db.Column(db.String(100), nullable=False)

    def to_dict(self):
        return {"id": self.id, "name": self.name, "department": self.department}

@app.route("/", methods=["GET"])
def default():
    return 'Hello, World!'

@app.route("/students", methods=["POST"])
def create_student():
    """
    Create a new student
    ---
    tags:
      - Students
    parameters:
      - in: body
        name: body
        required: true
        schema:
          id: Student
          required:
            - name
            - age
            - course
          properties:
            name:
              type: string
              example: Alice
            age:
              type: integer
              example: 17
            course:
              type: string
              example: Mathematics
    responses:
      201:
        description: Student created
    """
    data = request.get_json()
    student = Student(name=data["name"], age=data["age"], course=data["course"])
    db.session.add(student)
    db.session.commit()
    return jsonify(student.to_dict()), 201

@app.route("/students", methods=["GET"])
def list_students():
    """
    Get all students
    ---
    tags:
      - Students
    responses:
      200:
        description: A list of students
    """
    students = Student.query.all()
    return jsonify([s.to_dict() for s in students])

@app.route("/students/<int:id>", methods=["GET"])
def get_student(id):
    """
    Get a student by ID
    ---
    tags:
      - Students
    parameters:
      - name: id
        in: path
        type: integer
        required: true
    responses:
      200:
        description: A single student
      404:
        description: Student not found
    """
    student = db.session.get(Student, id)
    if not student:
        return jsonify({"error": "Not found"}), 404
    return jsonify(student.to_dict())

@app.route("/students/<int:id>", methods=["PUT"])
def update_student(id):
    """
    Update a student
    ---
    tags:
      - Students
    parameters:
      - name: id
        in: path
        type: integer
        required: true
      - in: body
        name: body
        schema:
          properties:
            name:
              type: string
            age:
              type: integer
            course:
              type: string
    responses:
      200:
        description: Student updated
      404:
        description: Student not found
    """
    student = db.session.get(Student, id)
    if not student:
        return jsonify({"error": "Not found"}), 404
    data = request.get_json()
    student.name = data.get("name", student.name)
    student.age = data.get("age", student.age)
    student.course = data.get("course", student.course)
    db.session.commit()
    return jsonify(student.to_dict())

@app.route("/students/<int:id>", methods=["DELETE"])
def delete_student(id):
    """
    Delete a student
    ---
    tags:
      - Students
    parameters:
      - name: id
        in: path
        type: integer
        required: true
    responses:
      204:
        description: Student deleted
      404:
        description: Student not found
    """
    student = db.session.get(Student, id)
    if not student:
        return jsonify({"error": "Not found"}), 404
    db.session.delete(student)
    db.session.commit()
    return '', 204

@app.route("/teachers", methods=["POST"])
def create_teacher():
    """
    Create a new teacher
    ---
    tags:
      - Teachers
    parameters:
      - in: body
        name: body
        required: true
        schema:
          id: Teacher
          required:
            - name
            - department
          properties:
            name:
              type: string
              example: Cesar Olavo
            department:
              type: string
              example: Computação
    responses:
      201:
        description: Teacher created
    """
    data = request.get_json()
    teacher = Teacher(name=data["name"], department=data["department"])
    db.session.add(teacher)
    db.session.commit()
    return jsonify(teacher.to_dict()), 201

@app.route("/teachers", methods=["GET"])
def list_teachers():
    """
    Get all teachers
    ---
    tags:
      - Teachers
    responses:
      200:
        description: A list of teachers
    """
    teachers = Teacher.query.all()
    return jsonify([t.to_dict() for t in teachers])

@app.route("/teachers/<int:id>", methods=["GET"])
def get_teacher(id):
    """
    Get a teacher by ID
    ---
    tags:
      - Teachers
    parameters:
      - name: id
        in: path
        type: integer
        required: true
    responses:
      200:
        description: A single teacher
      404:
        description: Teacher not found
    """
    teacher = db.session.get(Teacher, id)
    if not teacher:
        return jsonify({"error": "Not found"}), 404
    return jsonify(teacher.to_dict())

@app.route("/teachers/<int:id>", methods=["PUT"])
def update_teacher(id):
    """
    Update a teacher
    ---
    tags:
      - Teachers
    parameters:
      - name: id
        in: path
        type: integer
        required: true
      - in: body
        name: body
        schema:
          properties:
            name:
              type: string
            department:
              type: string
    responses:
      200:
        description: Teacher updated
      404:
        description: Teacher not found
    """
    teacher = db.session.get(Teacher, id)
    if not teacher:
        return jsonify({"error": "Not found"}), 404
    data = request.get_json()
    teacher.name = data.get("name", teacher.name)
    teacher.department = data.get("department", teacher.department)
    db.session.commit()
    return jsonify(teacher.to_dict())

@app.route("/teachers/<int:id>", methods=["DELETE"])
def delete_teacher(id):
    """
    Delete a teacher
    ---
    tags:
      - Teachers
    parameters:
      - name: id
        in: path
        type: integer
        required: true
    responses:
      204:
        description: Teacher deleted
      404:
        description: Teacher not found
    """
    teacher = db.session.get(Teacher, id)
    if not teacher:
        return jsonify({"error": "Not found"}), 404
    db.session.delete(teacher)
    db.session.commit()
    return '', 204