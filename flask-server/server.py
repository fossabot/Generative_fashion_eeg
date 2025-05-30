from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import json
import os
import latent_manipulation


app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*", "methods": ["GET", "POST", "OPTIONS"], "allow_headers": ["Content-Type"]}})

# Dateien
USER_RATINGS_PREFIX = 'user'
USER_RATINGS_SUFFIX = '.json'
IMAGES_DIR = latent_manipulation.ensure_directories()


################### HELPERS ###################

# gibt directory zurück in Form userX.json
def get_user_ratings_file(user_id):
    
    server_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(server_dir, f"{USER_RATINGS_PREFIX}{user_id}{USER_RATINGS_SUFFIX}")

#  Laden der Bewertungen, für userX
def load_user_ratings(user_id):
    ratings_file = get_user_ratings_file(user_id)
    if os.path.exists(ratings_file):
        with open(ratings_file, 'r') as f:
            try:
                #lese
                data = json.load(f)
                
                #  nicht? dann erstelle Leeres
                if not data:
                    data = {}
                # gebe Daten zurück
                return data
            except json.JSONDecodeError:
                print(f"Fehler beim Laden der JSON-Datei für User {user_id}, erstelle neue Struktur")
                return {}
    else:
        print(f"Datei {ratings_file} existiert nicht, erstelle neue")
        # Datei mit Grundstruktur
        data = {}
        with open(ratings_file, 'w') as f:
            # Leere Struktur als json geschrieben mit zwei Einrückungen für bessere Lesbarkeit
            json.dump(data, f, indent=2)
        return data

# Speicher Bewertungen für UserX
def save_user_ratings(user_id, ratings):
    ratings_file = get_user_ratings_file(user_id)
    with open(ratings_file, 'w') as f:
        json.dump(ratings, f, indent=2)
        

################### ENDPOINTS ###################

# Endpoint - neuer User
@app.route("/create_user", methods=["POST"])
def create_user():
    #Verzeichnis zurückgeben + in absoluten Pfad umwandeln
    server_dir = os.path.dirname(os.path.abspath(__file__))
    print(f"Server-Verzeichnis: {server_dir}")
    all_user_files = [f for f in os.listdir(server_dir) if f.startswith(USER_RATINGS_PREFIX) and f.endswith(USER_RATINGS_SUFFIX)]
    print(f"Vorhandene Dateien: {all_user_files}")
    existing_user_ids = []
    
    # Speichere User IDs in Liste aus Dateinamen
    for file in all_user_files:
        try:
            user_id = int(file.replace(USER_RATINGS_PREFIX, '').replace(USER_RATINGS_SUFFIX, ''))
            existing_user_ids.append(user_id)
        except ValueError:
            pass
        
    #Debug für gefundene User Dateien
    print(f"Vorhandene User-IDs: {existing_user_ids}")
    
  
    if existing_user_ids:
        user_id = max(existing_user_ids) + 1
    else:
        # Wenn kein Nutzer, starte mit 1
        user_id = 1
    
    #Debug neue Nutzer ID
    print(f"Erstelle neue User-ID: {user_id}")
    
    # Neue leere Datei
    ratings_file = get_user_ratings_file(user_id)
    print(f"Ratings-Datei-Pfad: {ratings_file}")
    
   # Generiere Bilder 
    initial_images_info = latent_manipulation.generate_new_images_for_iteration(user_id, 0)
    
    # Initialisiere Dictionary (0) 
    with open(ratings_file, 'w') as f:
        initial_data = {
            "it0": {
                "index": [],
                "rating": [],
                #Initial Images und Datei mit Vektoren, inital images später löschen
                "images": initial_images_info["filenames"],
                "vectors_file": initial_images_info["vectors_file"]
            }
        }
        json.dump(initial_data, f, indent=2)
    print(f"Neue Datei erstellt: {ratings_file} mit Iteration 0 für Benutzer {user_id}")
    
    return jsonify({
        "userId": user_id, 
       
        "images": [] #Leer, weil die ersten Bilder aus dem Frontend kommen aktuell
    })
    
@app.route("/ratings", methods=["POST"])
def ratings():
    # extrahiere Bewertungenung speichere sie
    new_rating = request.json
    
    # Hole Nutzer ID aus json, falls keine standart 1
    user_id = new_rating.get("userId", 1)
    
    # Bewertungen die schon da sind laden
    user_ratings = load_user_ratings(user_id)
    
    # Hole aktuelle Iterationnummer, Index des Bewerteten Bildes,  Bewertungswert
    iteration = new_rating.get("iteration", 0)
    image_index = new_rating.get("imageIndex", 0)
    rating_value = new_rating.get("rating", 0)
    
    # It. nummer als String für JSON
    iteration_key = f"it{iteration}"
    
    #Debug extrahierter Parameter
    print(f"Verarbeite Bewertung für User {user_id}, {iteration_key}, Bild {image_index}, Wert {rating_value}")
    
    #  Bild dieser Iteration bereits bewertet??
    already_rated = False
    if iteration_key in user_ratings and "index" in user_ratings[iteration_key]:
        for i, idx in enumerate(user_ratings[iteration_key]["index"]):
            if idx == image_index:
                already_rated = True
                print(f"Image {image_index} already rated in iteration {iteration} by user {user_id}.")
                break
    
    if already_rated:
        return jsonify({"message": "Image already rated", "already_rated": True, "userId": user_id})
    
    # Falls es noch keine gibt füge Struktur hinzu
    if iteration_key not in user_ratings:
        user_ratings[iteration_key] = {
            "index": [],
            "rating": []
        }
    
    # füge index hinzu
    user_ratings[iteration_key]["index"].append(image_index)
    
    # Konvertiere NaN zu null für JSON-Kompatibilität -> vllt einfach direkt 0?
    if rating_value == "NaN":
        json_rating = None
    else:
        try:
            json_rating = int(rating_value)
        except (ValueError, TypeError):
            json_rating = None
            
    # Bewertung hinzufügen
    user_ratings[iteration_key]["rating"].append(json_rating)
    
    # Falls neue It - zurücksetzen 
    new_images_info = None
    new_iteration_started = False
    
    #schon 4 Bewetungen?
    if len(user_ratings[iteration_key]["index"]) >= 4:
        next_iteration = iteration + 1
        print(f"4 Bewertungen in Iteration {iteration} erreicht - Erstelle Iteration {next_iteration}")
        next_iteration_key = f"it{next_iteration}"
        
        # Generiere Bilder für die nächste Iteration 
        new_images_info = latent_manipulation.generate_new_images_for_iteration(user_id, next_iteration)
        
        # Neue Iteration + generierten Bilddaten initialisieren
        if next_iteration_key not in user_ratings:
            user_ratings[next_iteration_key] = {
                "index": [],
                "rating": [],
                "images": new_images_info["filenames"],
                "vectors_file": new_images_info["vectors_file"]
            }
        
        new_iteration_started = True
    
    # Speichere Bewertungen nach jeder neuen 
    save_user_ratings(user_id, user_ratings)
    
    print(f"Neue Bewertung in Iteration {iteration} für User {user_id} gespeichert")
    
    # Response mit zusätzlichen Informationen, wenn eine neue Iteration begonnen hat
    response_data = {
        "message": "Bewertung gespeichert", 
        "userId": user_id, 
        "iteration": iteration
    }
    
    if new_iteration_started:
        response_data.update({
            "newIteration": next_iteration,
            "newImagesAvailable": True,
            "images": new_images_info["filenames"]
        })
    
    return jsonify(response_data)

# Endpoint der Bewertungen, für best. Benutzer
@app.route("/ratings/<int:user_id>", methods=["GET"])
def get_user_ratings(user_id):
    user_ratings = load_user_ratings(user_id)
    #als Python Dictionary zurückgeben
    return jsonify(user_ratings)

#Lösche alles 
@app.route("/delete_all_userIDs", methods=["POST", "OPTIONS"])
def deleteUserIDs():
    # CORS preflight request
    if request.method == "OPTIONS":
        response = app.make_default_options_response()
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
        return response
    
    try:
        # Server-Verzeichnis ermitteln
        server_dir = os.path.dirname(os.path.abspath(__file__))
        print(f"Server-Verzeichnis für Löschvorgang: {server_dir}")
        
        # Alle JSON-Benutzerdateien finden
        all_user_files = [f for f in os.listdir(server_dir) 
                         if f.startswith(USER_RATINGS_PREFIX) and f.endswith(USER_RATINGS_SUFFIX)]
        
        print(f"Gefundene Benutzerdateien zum Löschen: {all_user_files}")
        
        # Zählen, wie viele Dateien gelöscht werden
        deleted_count = 0
        deleted_files = []
        
        # Alle Benutzerdateien löschen
        for file in all_user_files:
            file_path = os.path.join(server_dir, file)
            try:
                os.remove(file_path)
                deleted_count += 1
                deleted_files.append(file)
                print(f"Gelöschte Datei: {file}")
            except Exception as e:
                print(f"Fehler beim Löschen von {file}: {str(e)}")
        
        # Optional: Auch alle Vektordateien löschen
        vector_files = [f for f in os.listdir(server_dir) if f.startswith(USER_RATINGS_PREFIX) and "_vectors.npy" in f]
        for file in vector_files:
            file_path = os.path.join(server_dir, file)
            try:
                os.remove(file_path)
                deleted_count += 1
                deleted_files.append(file)
                print(f"Gelöschte Vektordatei: {file}")
            except Exception as e:
                print(f"Fehler beim Löschen von {file}: {str(e)}")
        
        # Erfolg melden
        response = jsonify({
            "success": True,
            "message": f"{deleted_count} Benutzerdateien wurden gelöscht",
            "deletedFiles": len(deleted_files),
            "fileNames": deleted_files
        })
        
        # Explizite CORS-Header setzen
        response.headers.add('Access-Control-Allow-Origin', '*')
        return response
    
    except Exception as e:
        print(f"Fehler beim Löschen der Benutzerdateien: {str(e)}")
        response = jsonify({
            "success": False,
            "message": f"Fehler beim Löschen der Dateien: {str(e)}"
        }), 500
        
        # Auch bei Fehlern CORS-Header setzen
        response.headers.add('Access-Control-Allow-Origin', '*')
        return response

@app.route("/ratings", methods=["GET"])
def get_all_ratings():
    # Alle Benutzer-Dateien
    server_dir = os.path.dirname(os.path.abspath(__file__))
    all_user_files = [f for f in os.listdir(server_dir) if f.startswith(USER_RATINGS_PREFIX) and f.endswith(USER_RATINGS_SUFFIX)]
    
    # Extrahiere Benutzer-IDs & sortier 
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

# Bilder aus images abrufen, später nicht mehr gebraucht
@app.route("/images/<path:filename>")
def get_image(filename):
    server_dir = os.path.dirname(os.path.abspath(__file__))
    return send_from_directory(os.path.join(server_dir, "images"), filename)

# Abrufen verfügbarer Bilder für bestimmte It eines UsersX
@app.route("/user_images/<int:user_id>/<int:iteration>", methods=["GET"])
def get_user_iteration_images(user_id, iteration):
    user_ratings = load_user_ratings(user_id)
    iteration_key = f"it{iteration}"
    
    if iteration_key in user_ratings and "images" in user_ratings[iteration_key]:
        return jsonify({
            "images": user_ratings[iteration_key]["images"],
            "userId": user_id,
            "iteration": iteration
        })
    else:
        return jsonify({
            "error": f"Keine Bilder für Benutzer {user_id}, Iteration {iteration} gefunden"
        }), 404

if __name__ == "__main__":
    app.run(debug=True)


