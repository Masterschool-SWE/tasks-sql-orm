from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# SQLite Database Configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///kanban.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Define the Task Model
class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(100), nullable=False)
    status = db.Column(db.String(20), nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'text': self.text,
            'status': self.status
        }

# Create the database if it doesn't exist
with app.app_context():
    db.create_all()

@app.route('/', methods=['GET'])
def home():
    return "<h2>Welcome to the Kanban backend server</h2>"

@app.route('/tasks', methods=['GET'])
def get_tasks():
    tasks = Task.query.all()
    return jsonify([task.to_dict() for task in tasks])

@app.route('/tasks/<int:id>', methods=['GET'])
def get_task(id):
    task = Task.query.get(id)
    if task:
        return jsonify(task.to_dict())
    else:
        return jsonify({"error": "Task not found"}), 404

@app.route('/tasks', methods=['POST'])
def create_task():
    data = request.json
    new_task = Task(text=data['text'], status=data['status'])
    db.session.add(new_task)
    db.session.commit()
    return jsonify(new_task.to_dict()), 201

@app.route('/tasks/<int:id>', methods=['PUT'])
def update_task(id):
    task = Task.query.get(id)
    if task:
        data = request.json
        task.text = data.get('text', task.text)
        task.status = data.get('status', task.status)
        db.session.commit()
        return jsonify(task.to_dict())
    else:
        return jsonify({"error": "Task not found"}), 404

@app.route('/tasks/<int:id>', methods=['PATCH'])
def patch_task(id):
    task = Task.query.get(id)
    if task:
        data = request.json
        if 'text' in data:
            task.text = data['text']
        if 'status' in data:
            task.status = data['status']
        db.session.commit()
        return jsonify(task.to_dict())
    else:
        return jsonify({"error": "Task not found"}), 404

@app.route('/tasks/<int:id>', methods=['DELETE'])
def delete_task(id):
    task = Task.query.get(id)
    if task:
        db.session.delete(task)
        db.session.commit()
        return jsonify({"message": "Task deleted"}), 200
    else:
        return jsonify({"error": "Task not found"}), 404

if __name__ == "__main__":
    app.run(port=os.getenv('PORT'), debug=True, host="0.0.0.0")
