from flask import Flask, request, jsonify
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity, unset_jwt_cookies

from pymongo import MongoClient
from werkzeug.security import generate_password_hash, check_password_hash
import datetime

from Predictor import predictMarks

app = Flask(__name__)
app.config['SECRET_KEY'] = '22e2ea1408a8454eb96aa303d3e29424'
app.config['JWT_TOKEN_LOCATION'] = ['headers', 'cookies']
app.config['JWT_COOKIE_CSRF_PROTECT'] = False  # Disable CSRF protection for cookies

# Replace the following with your MongoDB Atlas connection string
MONGODB_URI = "mongodb+srv://madushan:6ST-x-XUNJ8D_gk@6sp.b6xvqam.mongodb.net/"

# Create a MongoClient instance
client = MongoClient(MONGODB_URI)

# Access your MongoDB Atlas database
db = client['6SP-database']

# Create a collection for teachers
teachers = db['teachers']
students = db['students']

# Setup Flask-JWT-Extended
jwt = JWTManager(app)

# Teacher model
class Teacher:
    def __init__(self, username, password):
        self.username = username
        self.password = password

# Student model
class Student:
    def __init__(self, name, email, marks, techername):
        self.name = name
        self.email = email
        self.marks = marks
        self.techername = techername

# For testing
@app.route('/api/test', methods=['POST'])
def test():
    data = request.get_json()
    print(data)
    return jsonify({'message': 'For Testing API'})

# Create a signup route
@app.route('/api/signup', methods=['POST'])
def signup():
    data = request.get_json()
    username = data['username']
    password = generate_password_hash(str(data['password']), method='sha256')

    if not username or not password:
        return jsonify({'message': 'Username and password are required'}), 400

    existing_user = teachers.find_one({'username': username})
    if existing_user:
        return jsonify({'message': 'User already exists'}), 400

    new_user = Teacher(username, password)
    teachers.insert_one(new_user.__dict__)
    return jsonify({'message': 'User created successfully'}), 201

# Create a login route
@app.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data['username']
    password = data['password']

    user = teachers.find_one({'username': username})
    if not user or not check_password_hash(user['password'], str(password)):
        return jsonify({'message': 'Invalid username or password'}), 401

    # Create a JWT token
    access_token = create_access_token(identity=user['username'], expires_delta=datetime.timedelta(hours=1))
    
    # Set JWT token as a cookie and return it in the response
    response = jsonify({'message': 'Login successful'})
    response.set_cookie('access_token_cookie', access_token, httponly=True)
    return response, 200

# Create a logout route
@app.route('/api/logout', methods=['POST'])
def logout():
    # Unset the JWT token cookie
    response = jsonify({'message': 'Logout successful'})
    unset_jwt_cookies(response)
    return response, 200

# Create a protected route
@app.route('/api/protected', methods=['GET'])
@jwt_required()
def protected():
    username = get_jwt_identity()
    return jsonify({'message': f'Protected route accessed by {username}'}), 200

# Create a predict route
@app.route('/api/predict', methods=['POST'])
def predict():
    data = request.get_json()
    doc = data['doc']

    try:
        prediction = predictMarks(doc)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

    response = jsonify({'prediction': prediction})
    return response, 200

# Create a addStudent route
@app.route('/api/addStudent', methods=['POST'])
def addStudent():
    data = request.get_json()
    name = data['name']
    email = data['email']
    marks = data['marks']
    techername = data['techername']

    if not name or not email or not marks:
        return jsonify({'message': 'Studnet name, email and marks are required'}), 400

    existing_user = students.find_one({'name': name})
    if existing_user:
        students.update_one({'name': name}, {'$set': {'marks': marks}})
        return jsonify({'message': f'{name} marks updated!'}), 400

    new_user = Student(name, email, marks, techername)
    students.insert_one(new_user.__dict__)
    return jsonify({'message': f'Student-{name} created successfully'}), 201

# Create a getStudents route
@app.route('/api/getStudents', methods=['POST'])
def getStudents():
    data = request.get_json()
    teachername = data['teachername'] 
    student_list = students.find()
    result = []
    
    for item in student_list:
        item['_id'] = str(item['_id'])
        result.append(item)
    
    return jsonify({f'{teachername} - students': result}), 200

if __name__ == '__main__':
    app.run(debug=True)
