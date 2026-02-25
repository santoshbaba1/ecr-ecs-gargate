# app.py - Simple Todo API
from flask import Flask, jsonify, request
import os
import time

app = Flask(__name__)

# In-memory storage (for demo)
todos = [
    {"id": 1, "title": "Learn Docker", "completed": True},
    {"id": 2, "title": "Learn ECS", "completed": False}
]

@app.route('/health')
def health():
    return jsonify({"status": "healthy", "timestamp": int(time.time())}), 200

@app.route('/api/todos', methods=['GET'])
def get_todos():
    return jsonify({
        "todos": todos,
        "count": len(todos),
        "environment": os.getenv('ENVIRONMENT', 'development'),
        "container_id": os.getenv('HOSTNAME', 'unknown')
    })

@app.route('/api/todos', methods=['POST'])
def create_todo():
    data = request.get_json()
    new_todo = {
        "id": len(todos) + 1,
        "title": data.get('title', 'Untitled'),
        "completed": False
    }
    todos.append(new_todo)
    return jsonify(new_todo), 201

@app.route('/api/todos/<int:todo_id>', methods=['PATCH'])
def update_todo(todo_id):
    todo = next((t for t in todos if t['id'] == todo_id), None)
    if not todo:
        return jsonify({"error": "Todo not found"}), 404
    
    data = request.get_json()
    todo['completed'] = data.get('completed', todo['completed'])
    return jsonify(todo)

if __name__ == '__main__':
    print(f"Starting Todo API in {os.getenv('ENVIRONMENT', 'development')} mode")
    app.run(host='0.0.0.0', port=8080, debug=False)