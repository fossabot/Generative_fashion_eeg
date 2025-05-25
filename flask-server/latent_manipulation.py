import json


RATINGS_FILE = 'ratings_data.json'

def load_ratings():
    try:
        with open(RATINGS_FILE, 'r') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

def print_ratings():
    ratings = load_ratings()
    if not ratings:
        print("Keine Bewertungen gefunden.")
    else:
        for i, rating in enumerate(ratings):
            print(f"Bewertung {i+1}: {rating}")

if __name__ == "__main__":
    print_ratings()