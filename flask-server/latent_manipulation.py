import json

import sys
sys.path.insert(0, "/content/stylegan3")
import pickle
import os
import numpy as np
import PIL.Image
from IPython.display import Image
import matplotlib.pyplot as plt
import IPython.display
import torch
import dnnlib
import legacy
import time
import random

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


############## note book ######

def seed2vec(G, seed):
  return np.random.RandomState(seed).randn(1, G.z_dim)

def display_image(image):
  plt.axis('off')
  plt.imshow(image)
  plt.show()

def generate_image(G, z, truncation_psi):
    # render imgs
    Gs_kwargs = {
        'output_transform': dict(func=tflib.convert_images_to_uint8,
        nchw_to_nhwc=True),
        'randomize_noise': False
    }
    if truncation_psi is not None:
        Gs_kwargs['truncation_psi'] = truncation_psi

    label = np.zeros([1] + G.input_shapes[1][1:])

    images = G.run(z, label, **G_kwargs)
    return images[0]

def get_label(G, device, class_idx):
  label = torch.zeros([1, G.c_dim], device=device)
  if G.c_dim != 0:
      if class_idx is None:
          ctx.fail('Must specify class label with --class'\
                   'when using a conditional network')
      label[:, class_idx] = 1
  else:
      if class_idx is not None:
          print ('warn: --class=lbl ignored when running '\
            'on an unconditional network')
  return label

def generate_image(device, G, z, truncation_psi=1.0,
                   noise_mode='const', class_idx=None):
  z = torch.from_numpy(z).to(device)
  label = get_label(G, device, class_idx)
  img = G(z, label, truncation_psi=truncation_psi,
          noise_mode=noise_mode)
  img = (img.permute(0, 2, 3, 1) * 127.5 + 128)\
    .clamp(0, 255).to(torch.uint8)
  return PIL.Image.fromarray(img[0].cpu().numpy(), 'RGB')

########### LOAD MODEL ###############
MODEL_PATH = "/content/drive/My Drive/MA/model/network-snapshot-005000.pkl"


print(f'Loading networks from" {MODEL_PATH}"...' )
device = torch.device('cuda')

with open(MODEL_PATH, 'rb') as f:
    G = legacy.load_network_pkl(f)['G_ema']\
      .requires_grad_(False).to(device)
      
      
############## Generate Image ##############

random_seed = random.randint(0,10000)
START_SEED_RANDOM = random.randint(0,random_seed)
START_SEED_MANUAL = 3479

print(START_SEED_RANDOM)

current = seed2vec(G, START_SEED_RANDOM)

img = generate_image(device, G, current)
SCALE = 0.5
display_image(img)
      
if __name__ == "__main__":
    print_ratings()