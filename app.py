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

class Classroom(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    semester = db.Column(db.String(50), nullable=False)

    def to_dict(self):
        return {"id": self.id, "name": self.name, "semester": self.semester}
    
class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    author = db.Column(db.String(100), nullable=False)
    year = db.Column(db.Integer, nullable=False)

    def to_dict(self):
        return {"id": self.id, "title": self.title, "author": self.author, "year": self.year}

@app.route("/", methods=["GET"])
def default():
    return 'Olá Mundo!'

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

@app.route("/classrooms", methods=["POST"])
def create_classroom():
    """
    Create a new classroom
    ---
    tags:
      - Classrooms
    parameters:
      - in: body
        name: body
        required: true
        schema:
          id: Classroom
          required:
            - name
            - semester
          properties:
            name:
              type: string
              example: Engenharia de Software
            semester:
              type: string
              example: 2025.1
    responses:
      201:
        description: Classroom created
    """
    data = request.get_json()
    classroom = Classroom(name=data["name"], semester=data["semester"])
    db.session.add(classroom)
    db.session.commit()
    return jsonify(classroom.to_dict()), 201

@app.route("/classrooms", methods=["GET"])
def list_classrooms():
    """
    Get all classrooms
    ---
    tags:
      - Classrooms
    responses:
      200:
        description: A list of classrooms
    """
    classrooms = Classroom.query.all()
    return jsonify([c.to_dict() for c in classrooms])

@app.route("/classrooms/<int:id>", methods=["GET"])
def get_classroom(id):
    """
    Get a classroom by ID
    ---
    tags:
      - Classrooms
    parameters:
      - name: id
        in: path
        type: integer
        required: true
    responses:
      200:
        description: A single classroom
      404:
        description: Classroom not found
    """
    classroom = db.session.get(Classroom, id)
    if not classroom:
        return jsonify({"error": "Not found"}), 404
    return jsonify(classroom.to_dict())

@app.route("/classrooms/<int:id>", methods=["PUT"])
def update_classroom(id):
    """
    Update a classroom
    ---
    tags:
      - Classrooms
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
            semester:
              type: string
    responses:
      200:
        description: Classroom updated
      404:
        description: Classroom not found
    """
    classroom = db.session.get(Classroom, id)
    if not classroom:
        return jsonify({"error": "Not found"}), 404
    data = request.get_json()
    classroom.name = data.get("name", classroom.name)
    classroom.semester = data.get("semester", classroom.semester)
    db.session.commit()
    return jsonify(classroom.to_dict())

@app.route("/classrooms/<int:id>", methods=["DELETE"])
def delete_classroom(id):
    """
    Delete a classroom
    ---
    tags:
      - Classrooms
    parameters:
      - name: id
        in: path
        type: integer
        required: true
    responses:
      204:
        description: Classroom deleted
      404:
        description: Classroom not found
    """
    classroom = db.session.get(Classroom, id)
    if not classroom:
        return jsonify({"error": "Not found"}), 404
    db.session.delete(classroom)
    db.session.commit()
    return '', 204

@app.route("/books", methods=["POST"])
def create_book():
    """
    Create a new book
    ---
    tags:
      - Books
    parameters:
      - in: body
        name: body
        required: true
        schema:
          id: Book
          required:
            - title
            - author
            - year
          properties:
            title:
              type: string
              example: Clean Code
            author:
              type: string
              example: Robert C. Martin
            year:
              type: integer
              example: 2008
    responses:
      201:
        description: Book created
    """
    data = request.get_json()
    book = Book(title=data["title"], author=data["author"], year=data["year"])
    db.session.add(book)
    db.session.commit()
    return jsonify(book.to_dict()), 201

@app.route("/books", methods=["GET"])
def list_books():
    """
    Get all books
    ---
    tags:
      - Books
    responses:
      200:
        description: A list of books
    """
    books = Book.query.all()
    return jsonify([b.to_dict() for b in books])

@app.route("/books/<int:id>", methods=["GET"])
def get_book(id):
    """
    Get a book by ID
    ---
    tags:
      - Books
    parameters:
      - name: id
        in: path
        type: integer
        required: true
    responses:
      200:
        description: A single book
      404:
        description: Book not found
    """
    book = db.session.get(Book, id)
    if not book:
        return jsonify({"error": "Not found"}), 404
    return jsonify(book.to_dict())

@app.route("/books/<int:id>", methods=["PUT"])
def update_book(id):
    """
    Update a book
    ---
    tags:
      - Books
    parameters:
      - name: id
        in: path
        type: integer
        required: true
      - in: body
        name: body
        schema:
          properties:
            title:
              type: string
            author:
              type: string
            year:
              type: integer
    responses:
      200:
        description: Book updated
      404:
        description: Book not found
    """
    book = db.session.get(Book, id)
    if not book:
        return jsonify({"error": "Not found"}), 404
    data = request.get_json()
    book.title = data.get("title", book.title)
    book.author = data.get("author", book.author)
    book.year = data.get("year", book.year)
    db.session.commit()
    return jsonify(book.to_dict())

@app.route("/books/<int:id>", methods=["DELETE"])
def delete_book(id):
    """
    Delete a book
    ---
    tags:
      - Books
    parameters:
      - name: id
        in: path
        type: integer
        required: true
    responses:
      204:
        description: Book deleted
      404:
        description: Book not found
    """
    book = db.session.get(Book, id)
    if not book:
        return jsonify({"error": "Not found"}), 404
    db.session.delete(book)
    db.session.commit()
    return '', 204