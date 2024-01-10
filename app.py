from flask import Flask, request, jsonify
from notion_client import Client
from datetime import datetime, timedelta
import os

app = Flask(__name__)
notion = Client(auth=os.getenv('NOTION_API_KEY'))

@app.route('/')
def home():
    return "Hello, World!"

@app.route('/tasks', methods=['GET'])
def get_tasks():
    database_id = os.getenv('NOTION_PAGE_ID')
    start_of_week = request.args.get('start', (datetime.now() - timedelta(days=datetime.now().weekday())).date().isoformat())
    end_of_week = request.args.get('end', (datetime.now() + timedelta(days=6-datetime.now().weekday())).date().isoformat())
    
    # Define the filter payload for the Notion API
    filter_payload = {
        "filter": {
            "and": [
                {
                    "property": "Due",
                    "date": {
                        "on_or_after": start_of_week,
                    },
                },
                {
                    "property": "Due",
                    "date": {
                        "before": end_of_week,
                    },
                },
            ],
        },
    }
    
    response = notion.databases.query(database_id=database_id, **filter_payload)
    return jsonify(response)

@app.route('/task', methods=['POST'])
def create_task():
    try:
        data = request.json
        database_id = os.getenv('NOTION_PAGE_ID')
        
        # Map the incoming data to the expected Notion properties format
        properties = {
            "Task": {  
                "title": [
                    {
                        "text": {
                            "content": data['title'] 
                        }
                    }
                ]
            },
            "Due": {  
                "date": {
                    "start": data['due']
                }
            },
        }

        if 'priority' in data:
            properties["Priority"] = { 
                "status": {
                    "name": data['priority']
                }
            }

        # Construct the payload for creating a new page in the Notion database
        new_page_payload = {
            "parent": {"database_id": database_id},
            "properties": properties
        }

        # Call the Notion API to create a new task
        response = notion.pages.create(**new_page_payload)
        return jsonify(response), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/task/<task_id>', methods=['PUT'])
def update_task(task_id):
    try:
        data = request.json
        properties = data['properties']
        response = notion.pages.update(page_id=task_id, properties=properties)
        return jsonify(response), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
