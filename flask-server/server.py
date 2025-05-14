from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)


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
    ratings=[]
    ratings.append(new_rating)
    print(ratings)
    return jsonify({"message": "Member added successfully", "member": new_rating})

     
    
if __name__ == "__main__":  
    app.run(host='0.0.0.0', port=5000, debug=True)
