from flask import Flask, request, jsonify
from notion_client import Client
import os

notion = Client(auth=os.getenv('NOTION_API_KEY'))

app = Flask(__name__)

@app.route('/tasks', methods=['GET'])
def get_tasks():
    # Notion API code to retrieve tasks
    return jsonify({"tasks": "tasks list here"})

@app.route('/task', methods=['POST'])
def create_task():
    # Notion API code to create a task
    return jsonify({"success": True, "message": "Task created"})

@app.route('/task/<task_id>', methods=['PUT'])
def update_task(task_id):
    # Notion API code to update a task
    return jsonify({"success": True, "message": "Task updated"})

if __name__ == '__main__':
    app.run(debug=True)
