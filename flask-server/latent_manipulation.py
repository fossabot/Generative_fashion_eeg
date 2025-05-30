import numpy as np
from PIL import Image
import os
import random

# Verzeichnisse für Bilder 
def ensure_directories():
    server_dir = os.path.dirname(os.path.abspath(__file__))
    images_dir = os.path.join(server_dir, "images")
    os.makedirs(images_dir, exist_ok=True)
    return images_dir

# Generiere neue Bilder für eine neue It
def generate_new_images_for_iteration(user_id, iteration, num_images=4):
   
    server_dir = os.path.dirname(os.path.abspath(__file__))
    images_dir = os.path.join(server_dir, "images")
    vectors_dir = os.path.join(server_dir, "vectors")
    
    # Verzeichnisse 
    os.makedirs(images_dir, exist_ok=True)
    os.makedirs(vectors_dir, exist_ok=True)
    
    # Bilder und Vektoren generieren
    vectors = []
    filenames = []
    colors = ["blue", "red", "green", "white", "lila", "yellow"]
    
    for i in range(num_images):
        # Zufällige Farbe
        color = random.choice(colors)
        
        # Latenten Vektor generieren (800-dimensional, wie in daten dann)
        vector = np.random.randn(800)
        vectors.append(vector)
        
        # Helligkeitswert 
        brightness = round(np.random.uniform(5.0, 7.0), 4)
        
        # Eindeutiger Dateiname
        filename = f"img_{color}_{brightness}.png"
        filepath = os.path.join(images_dir, filename)
        
        # RGB-Farbe aus den ersten 3 Dimensionen des Vektors
        if color == "blue":
            img_color = (0, 0, 255)
        elif color == "red":
            img_color = (255, 0, 0)
        elif color == "green":
            img_color = (0, 255, 0)
        elif color == "white":
            img_color = (255, 255, 255)
        elif color == "lila":
            img_color = (128, 0, 128)
        else:  # yellow
            img_color = (255, 255, 0)
        
        # Dummy-Bild 
        img = Image.new("RGB", (512, 512), img_color)
        img.save(filepath)
        
        filenames.append(filename)
    
    # Vektoren speichern
    vectors_filename = f"user{user_id}_it{iteration}_vectors.npy"
    vectors_filepath = os.path.join(vectors_dir, vectors_filename)
    np.save(vectors_filepath, np.array(vectors))
    
    # Rückgabe mit allen relevanten Informationen
    return {
        "filenames": filenames,
        "vectors": vectors,
        "vectors_file": vectors_filename,
        "iteration": iteration,
        "user_id": user_id
    }

# Wenn direkt ausgeführt, generiere Beispielbilder
if __name__ == "__main__":
    ensure_directories()
    vectors = []
    
    for i in range(10):
        vector = np.random.randn(800)
        vectors.append(vector)
        
        img_array = np.clip((vector[:3] * 255).astype(np.uint8), 0, 255)
        img = Image.new("RGB", (100, 100), tuple(img_array))
        img.save(f"images/img_{i}.png")
    
    np.save("vectors.npy", np.array(vectors))
