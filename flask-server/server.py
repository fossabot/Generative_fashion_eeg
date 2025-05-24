from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

ratings_list=[]

@app.route("/members")
def members():
    return {
        "members": [
            {"name": "Alice", "age": 30},
            {"name": "Bob", "age": 25},
            {"name": "Charlie", "age": 35}
        ]
    } 
    
@app.route("/ratings", methods=["POST"] )
def ratings():
    new_rating=request.json
    ratings_list.append(new_rating)
    print(ratings_list)
    return jsonify({"new rating": new_rating})

     
    
