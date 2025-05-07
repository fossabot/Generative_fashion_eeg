
import sys
sys.path.insert(0, "/home/l/lauf/thesis/Generative_fashion_eeg/stylegan3")
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


MODEL_PATH = "Generative_fashion_eeg/model/network-snapshot-005000.pkl"

print(f'Loading networks from" {MODEL_PATH}"...' )
device = torch.device('cuda')

with open(MODEL_PATH, 'rb') as f:
    G = legacy.load_network_pkl(f)['G_ema']\
      .requires_grad_(False).to(device)

import random
random_seed = random.randint(0,10000)
START_SEED_RANDOM = random.randint(0,random_seed)
START_SEED_MANUAL = 3479

print(START_SEED_RANDOM)

current = seed2vec(G, START_SEED_RANDOM)

img = generate_image(device, G, current)
SCALE = 0.5
display_image(img)

EXPLORE_SIZE = 30

explore_random = []
explore_controlled = []


initial_latent_vector = current
current_vector = initial_latent_vector.copy()  #latent vector

for i in range(EXPLORE_SIZE):
  explore_random.append(np.random.rand(1, 512) - 0.5 )

for i in range(EXPLORE_SIZE):
  current_vector = np.add(current_vector, 0.2) # add 0.2
  explore_controlled.append(current_vector.copy())

#hier müsste dann bayes weiter machen I guess
