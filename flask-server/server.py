from flask import Flask, request, jsonify
from flask_cors import CORS
import json
import os

app = Flask(__name__)
CORS(app)

# Dateien
USER_RATINGS_PREFIX = 'user'
USER_RATINGS_SUFFIX = '.json'

# Dateinamen
def get_user_ratings_file(user_id):
    # Absoluter Pfad
    server_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(server_dir, f"{USER_RATINGS_PREFIX}{user_id}{USER_RATINGS_SUFFIX}")

#  Laden der Bewertungen, für einen bestimmten Benutzer
def load_user_ratings(user_id):
    ratings_file = get_user_ratings_file(user_id)
    if os.path.exists(ratings_file):
        with open(ratings_file, 'r') as f:
            try:
                data = json.load(f)
                
                #  Strukturcheck
                if not data:
                    data = {}
                return data
            except json.JSONDecodeError:
                print(f"Fehler beim Laden der JSON-Datei für User {user_id}, erstelle neue Struktur")
                return {}
    else:
        print(f"Datei {ratings_file} existiert nicht, erstelle neue")
        # Datei mit Grundstruktur
        data = {}
        with open(ratings_file, 'w') as f:
            json.dump(data, f, indent=2)
        return data

# Speichern der Bewertungen für bestimmten Benutzer
def save_user_ratings(user_id, ratings):
    ratings_file = get_user_ratings_file(user_id)
    with open(ratings_file, 'w') as f:
        json.dump(ratings, f, indent=2)

@app.route("/members")
def members():
    return {
        "members": [
            {"name": "Alice", "age": 30},
            {"name": "Bob", "age": 25},
            {"name": "Charlie", "age": 35}
        ]
    } 

# Endpoint - neuer Benutzer
@app.route("/create_user", methods=["POST"])
def create_user():
    # Neue Datei + nächst höhere ID 
    
    # Alle vorhandenen Benutzer 
    server_dir = os.path.dirname(os.path.abspath(__file__))
    print(f"Server-Verzeichnis: {server_dir}")
    all_user_files = [f for f in os.listdir(server_dir) if f.startswith(USER_RATINGS_PREFIX) and f.endswith(USER_RATINGS_SUFFIX)]
    print(f"Vorhandene Dateien: {all_user_files}")
    existing_user_ids = []
    
    for file in all_user_files:
        try:
            user_id = int(file.replace(USER_RATINGS_PREFIX, '').replace(USER_RATINGS_SUFFIX, ''))
            existing_user_ids.append(user_id)
        except ValueError:
            pass
    
    print(f"Vorhandene User-IDs: {existing_user_ids}")
    
    # Nächste User-ID
    if existing_user_ids:
        # Höchste ID + 1 verwenden 
        user_id = max(existing_user_ids) + 1
    else:
        # Wenn kein Nutzer, beginne mit 1
        user_id = 1
    
    print(f"Erstelle neue User-ID: {user_id}")
    
    # Neue leere Datei
    ratings_file = get_user_ratings_file(user_id)
    print(f"Ratings-Datei-Pfad: {ratings_file}")
    
    # Initialisiere Datei -> ersten Iteration
    with open(ratings_file, 'w') as f:
        # Start It 0
        initial_data = {
            "it0": {
                "index": [],
                "vector": [],
                "rating": []
            }
        }
        json.dump(initial_data, f, indent=2)
    print(f"Neue Datei erstellt: {ratings_file} mit Iteration 0 für Benutzer {user_id}")
    
    return jsonify({"userId": user_id, "message": f"User {user_id} wurde erstellt"})
    
@app.route("/ratings", methods=["POST"])
def ratings():
    new_rating = request.json
    
    # Benutzer-ID extrahieren
    user_id = new_rating.get("userId", 1)
    
    # Bestehenden Bewertungen laden
    user_ratings = load_user_ratings(user_id)
    
    # Speicherung nach Iterationen !!!
    iteration = new_rating.get("iteration", 0)
    image_index = new_rating.get("imageIndex", 0)
    rating_value = new_rating.get("rating", 0)
    
    # It. als String für JSON-Key
    iteration_key = f"it{iteration}"
    
    print(f"Verarbeite Bewertung für User {user_id}, {iteration_key}, Bild {image_index}, Wert {rating_value}")
    
    #  Bild in dieser It bereits bewertet??
    already_rated = False
    if iteration_key in user_ratings and "index" in user_ratings[iteration_key]:
        for i, idx in enumerate(user_ratings[iteration_key]["index"]):
            if idx == image_index:
                already_rated = True
                print(f"Bild {image_index} wurde bereits in Iteration {iteration} von User {user_id} bewertet.")
                break
    
    if already_rated:
        return jsonify({"message": "Bild wurde bereits bewertet", "already_rated": True, "userId": user_id})
    
    # Neue Struktur für diese Iteration, falls sie nicht da
    if iteration_key not in user_ratings:
        user_ratings[iteration_key] = {
            "index": [],
            "vector": [],
            "rating": []
        }
    
    # Aktualisiere die Daten
    user_ratings[iteration_key]["index"].append(image_index)
    
    # Konvertiere NaN zu null für JSON-Kompatibilität -> vllt einfach direkt 0?
    if rating_value == "NaN":
        json_rating = None
    else:
        try:
            json_rating = int(rating_value)
        except (ValueError, TypeError):
            json_rating = None
    
    user_ratings[iteration_key]["rating"].append(json_rating)
    
    # Platzhalter für den Vektor 
    #  für jede Bewertung einen Vektor 
    user_ratings[iteration_key]["vector"].append([0.0, 0.0, 0.0])
    
    # 4 Bewertungen in der aktuellen Iteration?
    # Wenn ja, erstelle eine neue Iteration 
    if len(user_ratings[iteration_key]["index"]) >= 4:
        print(f"4 Bewertungen in Iteration {iteration} erreicht - Erstelle Iteration {iteration + 1}")
        next_iteration_key = f"it{iteration + 1}"
        if next_iteration_key not in user_ratings:
            user_ratings[next_iteration_key] = {
                "index": [],
                "vector": [],
                "rating": []
            }
    
    # Speichere Bewertungen nach jeder neuen
    save_user_ratings(user_id, user_ratings)
    
    print(f"Neue Bewertung in Iteration {iteration} für User {user_id} gespeichert")
    return jsonify({"message": "Bewertung gespeichert", "userId": user_id, "iteration": iteration})

# Endpoint der Bewertungen, für best. Benutzer
@app.route("/ratings/<int:user_id>", methods=["GET"])
def get_user_ratings(user_id):
    user_ratings = load_user_ratings(user_id)
    return jsonify(user_ratings)

@app.route("/ratings", methods=["GET"])
def get_all_ratings():
    # Alle Benutzer-Dateien
    server_dir = os.path.dirname(os.path.abspath(__file__))
    all_user_files = [f for f in os.listdir(server_dir) if f.startswith(USER_RATINGS_PREFIX) and f.endswith(USER_RATINGS_SUFFIX)]
    
    # Extrahiere Benutzer-IDs & sort 
    user_ids = []
    for file in all_user_files:
        try:
            user_id = int(file.replace(USER_RATINGS_PREFIX, '').replace(USER_RATINGS_SUFFIX, ''))
            user_ids.append(user_id)
        except ValueError:
            pass
    
    user_ids.sort()
    
    # Zusammenfassung der Benutzer-Dateien
    summary = {
        "userIds": user_ids,
        "userCount": len(user_ids),
        "files": all_user_files
    }
    
    return jsonify(summary)

if __name__ == "__main__":
    app.run(debug=True)


