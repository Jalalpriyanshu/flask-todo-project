from flask import Flask, render_template, jsonify, request
from pymongo import MongoClient
from datetime import datetime

app = Flask(__name__)

# MongoDB connection
try:
    client = MongoClient('mongodb://localhost:27017/')
    db = client['todo_database']
    collection = db['todo_items']
    print("MongoDB connected successfully!")
except Exception as e:
    print(f"MongoDB connection error: {e}")

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/api')
def api():
    import json
    with open('data.json', 'r') as f:
        data = json.load(f)
    return jsonify(data)

@app.route('/submittodoitem', methods=['POST'])
def submit_todo_item():
    try:
        data = request.get_json()
        item_name = data.get('itemName')
        item_description = data.get('itemDescription')
        
        if not item_name or not item_description:
            return jsonify({
                'success': False,
                'message': 'Item name and description are required'
            }), 400
        
        todo_item = {
            'itemName': item_name,
            'itemDescription': item_description,
            'createdAt': datetime.now()
        }
        
        result = collection.insert_one(todo_item)
        
        return jsonify({
            'success': True,
            'message': 'Todo item added successfully',
            'id': str(result.inserted_id)
        }), 201
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500

if __name__ == '__main__':
    app.run(debug=True)