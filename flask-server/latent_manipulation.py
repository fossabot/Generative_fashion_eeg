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


######### SPÄTER, WENNS MIT GPU GEHT ###################

# ---- Helper ----#

# def seed2vec(G, seed):
#   return np.random.RandomState(seed).randn(1, G.z_dim)

# def display_image(image):
#   plt.axis('off')
#   plt.imshow(image)
#   plt.show()

# def generate_image(G, z, truncation_psi):
#     # render imgs
#     Gs_kwargs = {
#         'output_transform': dict(func=tflib.convert_images_to_uint8,
#         nchw_to_nhwc=True),
#         'randomize_noise': False
#     }
#     if truncation_psi is not None:
#         Gs_kwargs['truncation_psi'] = truncation_psi

#     label = np.zeros([1] + G.input_shapes[1][1:])

#     images = G.run(z, label, **G_kwargs)
#     return images[0]

# def get_label(G, device, class_idx):
#   label = torch.zeros([1, G.c_dim], device=device)
#   if G.c_dim != 0:
#       if class_idx is None:
#           ctx.fail('Must specify class label with --class'\
#                    'when using a conditional network')
#       label[:, class_idx] = 1
#   else:
#       if class_idx is not None:
#           print ('warn: --class=lbl ignored when running '\
#             'on an unconditional network')
#   return label

# def generate_image(device, G, z, truncation_psi=1.0,
#                    noise_mode='const', class_idx=None):
#   z = torch.from_numpy(z).to(device)
#   label = get_label(G, device, class_idx)
#   img = G(z, label, truncation_psi=truncation_psi,
#           noise_mode=noise_mode)
#   img = (img.permute(0, 2, 3, 1) * 127.5 + 128)\
#     .clamp(0, 255).to(torch.uint8)
#   return PIL.Image.fromarray(img[0].cpu().numpy(), 'RGB')

# ########### LOAD MODEL & GENERATE IMAGES ###############
# MODEL_PATH = "/home/l/lauf/thesis/Generative_fashion_eeg/model/network-snapshot-005000.pkl"


# print(f'Loading networks from" {MODEL_PATH}"...' )
# device = torch.device('cuda')

# with open(MODEL_PATH, 'rb') as f:
#     G = legacy.load_network_pkl(f)['G_ema']\
#       .requires_grad_(False).to(device)
      
# def load_ratings():
#     try:
#         with open(RATINGS_FILE, 'r') as f:
#             return json.load(f)
#     except (FileNotFoundError, json.JSONDecodeError):
#         return []

# def print_ratings():
#     ratings = load_ratings()
#     if not ratings:
#         print("Keine Bewertungen gefunden.")
#     else:
#         for i, rating in enumerate(ratings):
#             print(f"Bewertung {i+1}: {rating}")


# ############## note book ######

# def seed2vec(G, seed):
#   return np.random.RandomState(seed).randn(1, G.z_dim)

# def display_image(image):
#   plt.axis('off')
#   plt.imshow(image)
#   plt.show()

# def generate_image(G, z, truncation_psi):
#     # render imgs
#     Gs_kwargs = {
#         'output_transform': dict(func=tflib.convert_images_to_uint8,
#         nchw_to_nhwc=True),
#         'randomize_noise': False
#     }
#     if truncation_psi is not None:
#         Gs_kwargs['truncation_psi'] = truncation_psi

#     label = np.zeros([1] + G.input_shapes[1][1:])

#     images = G.run(z, label, **G_kwargs)
#     return images[0]

# def get_label(G, device, class_idx):
#   label = torch.zeros([1, G.c_dim], device=device)
#   if G.c_dim != 0:
#       if class_idx is None:
#           ctx.fail('Must specify class label with --class'\
#                    'when using a conditional network')
#       label[:, class_idx] = 1
#   else:
#       if class_idx is not None:
#           print ('warn: --class=lbl ignored when running '\
#             'on an unconditional network')
#   return label

# def generate_image(device, G, z, truncation_psi=1.0,
#                    noise_mode='const', class_idx=None):
#   z = torch.from_numpy(z).to(device)
#   label = get_label(G, device, class_idx)
#   img = G(z, label, truncation_psi=truncation_psi,
#           noise_mode=noise_mode)
#   img = (img.permute(0, 2, 3, 1) * 127.5 + 128)\
#     .clamp(0, 255).to(torch.uint8)
#   return PIL.Image.fromarray(img[0].cpu().numpy(), 'RGB')

# ########### LOAD MODEL ###############
# MODEL_PATH = "/home/l/lauf/thesis/Generative_fashion_eeg/model/network-snapshot-005000.pkl"


# print(f'Loading networks from" {MODEL_PATH}"...' )
# device = torch.device('cuda')

# with open(MODEL_PATH, 'rb') as f:
#     G = legacy.load_network_pkl(f)['G_ema']\
#       .requires_grad_(False).to(device)
      
      
# ############## Generate Image ##############

# random_seed = random.randint(0,10000)
# START_SEED_RANDOM = random.randint(0,random_seed)
# START_SEED_MANUAL = 3479

# print(START_SEED_RANDOM)

# current = seed2vec(G, START_SEED_RANDOM)
# print(current)


# img = generate_image(device, G, current)
# SCALE = 0.5
# display_image(img)
# img.save("/home/l/lauf/thesis/Generative_fashion_eeg/new_output_images/generated_image.png")



# if __name__ == "__main__":
#     print_ratings()

      
# ############## Generate Image ##############

# random_seed = random.randint(0,10000)
# START_SEED_RANDOM = random.randint(0,random_seed)
# START_SEED_MANUAL = 3479

# print(START_SEED_RANDOM)

# current = seed2vec(G, START_SEED_RANDOM)
# print(current)


# img = generate_image(device, G, current)
# SCALE = 0.5
# display_image(img)
# img.save("/home/l/lauf/thesis/Generative_fashion_eeg/new_output_images/generated_image.png")



# if __name__ == "__main__":
#     print_ratings()
