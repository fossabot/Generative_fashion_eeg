from flask import Flask
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
    
if __name__ == "__main__":  
    app.run(debug=True)
