from flask import Flask, request, jsonify
import jwt
from pymongo import MongoClient
from werkzeug.security import generate_password_hash, check_password_hash
import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = '22e2ea1408a8454eb96aa303d3e29424'

# Replace the following with your MongoDB Atlas connection string
MONGODB_URI = "mongodb+srv://madushan:6ST-x-XUNJ8D_gk@6sp.b6xvqam.mongodb.net/"

# Create a MongoClient instance
client = MongoClient(MONGODB_URI)

# Access your MongoDB Atlas database
db = client['6SP-database']

# Create a collection for users
users = db['user-details']

# User model
class User:
    def __init__(self, username, password):
        self.username = username
        self.password = password

#For testing
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

    existing_user = users.find_one({'username': username})
    if existing_user:
        return jsonify({'message': 'User already exists'}), 400

    new_user = User(username, password)
    users.insert_one(new_user.__dict__)
    return jsonify({'message': 'User created successfully'}), 201

# Create a login route
@app.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data['username']
    password = data['password']

    user = users.find_one({'username': username})
    if not user or not check_password_hash(user['password'], password):
        return jsonify({'message': 'Invalid username or password'}), 401

    # Create a JWT token
    token = jwt.encode({'username': user['username'], 'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=1)}, app.config['SECRET_KEY'], algorithm='HS256')
    return jsonify({'token': token.decode('UTF-8')})

# Create a protected route
@app.route('/api/protected', methods=['GET'])
def protected():
    token = request.headers.get('Authorization')

    if not token:
        return jsonify({'message': 'Token is missing'}), 401

    try:
        # Decode the JWT token
        decoded_token = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
        username = decoded_token['username']
        return jsonify({'message': f'Protected route accessed by {username}'}), 200
    except jwt.ExpiredSignatureError:
        return jsonify({'message': 'Token has expired'}), 401
    except jwt.InvalidTokenError:
        return jsonify({'message': 'Invalid token'}), 401

if __name__ == '__main__':
    app.run(debug=True)