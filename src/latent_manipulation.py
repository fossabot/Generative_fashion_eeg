# -*- coding: utf-8 -*-

# HIDE OUTPUT
#!git clone https://github.com/NVlabs/stylegan3.git
#!pip install ninja


import sys
#add real stylegan3 path
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

def seed2vec(G, seed):
  return np.random.RandomState(seed).randn(1, G.z_dim)

def display_image(image):
  plt.axis('off')
  plt.imshow(image)
  plt.show()

def generate_image(G, z, truncation_psi):
    # Render images for dlatents initialized from random seeds.
    Gs_kwargs = {
        'output_transform': dict(func=tflib.convert_images_to_uint8,
        nchw_to_nhwc=True),
        'randomize_noise': False
    }
    if truncation_psi is not None:
        Gs_kwargs['truncation_psi'] = truncation_psi

    label = np.zeros([1] + G.input_shapes[1][1:])
    # [minibatch, height, width, channel]
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

"""Next, we load the NVIDIA FFHQ (faces) GAN.  We could use any StyleGAN pretrained GAN network here."""

# HIDE CODE

MODEL_PATH ="/Users/fionalau/Desktop/Masterthesis_Code/model/network-snapshot-005000.pkl"

print(f'Loading networks from" {MODEL_PATH}"...' )
device = torch.device('cuda')
# The file object 'f' should be passed to load_network_pkl
# instead of the BytesIO object 'fp'.
with open(MODEL_PATH, 'rb') as f:  # Open in binary read mode ('rb')
    G = legacy.load_network_pkl(f)['G_ema']\
      .requires_grad_(False).to(device)

"""## Generate and View GANS from Seeds

We will begin by generating a few seeds to evaluate potential starting points for our fine-tuning. Try out different seeds ranges until you have a seed that looks close to what you wish to fine-tune.
"""

# HIDE OUTPUT 1
# Choose your own starting and ending seed.
SEED_FROM = 4020
SEED_TO = 4023

# Generate the images for the seeds.
for i in range(SEED_FROM, SEED_TO):
  print(f"Seed {i}")
  z = seed2vec(G, i)
  img = generate_image(device, G, z)
  display_image(img)

"""## Fine-tune an Image

If you find a seed you like, you can fine-tune it by directly adjusting the latent vector.  First, choose the seed to fine-tune.
"""

START_SEED = 3070

current = seed2vec(G, START_SEED)

"""Next, generate and display the current vector. You will return to this point for each iteration of the finetuning."""

img = generate_image(device, G, current)

SCALE = 0.5
display_image(img)

"""Choose an explore size; this is the number of different potential images chosen by moving in 10 different directions.  Run this code once and then again anytime you wish to change the ten directions you are exploring.  You might change the ten directions if you are no longer seeing improvements."""

EXPLORE_SIZE = 25

explore = []
for i in range(EXPLORE_SIZE):
  explore.append( np.random.rand(1, 512) - 0.5 )

"""Each image displayed from running this code shows a potential direction that we can move in the latent vector.  Choose one image that you like and change MOVE_DIRECTION to indicate this decision.  Once you rerun the code, the code will give you a new set of potential directions.  Continue this process until you have a latent vector that you like."""

# HIDE OUTPUT 1
# Choose the direction to move.  Choose -1 for the initial iteration.
MOVE_DIRECTION = -1
SCALE = 0.5

if MOVE_DIRECTION >=0:
  current = current + explore[MOVE_DIRECTION]

for i, mv in enumerate(explore):
  print(f"Direction {i}")
  z = current + mv
  img = generate_image(device, G, z)
  display_image(img)

# HIDE OUTPUT 1
# Choose the direction to move.  Choose -1 for the initial iteration.
MOVE_DIRECTION = -1
SCALE = 0.5

if MOVE_DIRECTION >= 0:
  current = current + explore[MOVE_DIRECTION]

# Calculate grid dimensions
num_images = len(explore)
cols = 5  # Number of columns in the grid
rows = (num_images + cols - 1) // cols  # Number of rows, calculated to fit all images

# Create a figure and axes for the grid
fig, axes = plt.subplots(rows, cols, figsize=(cols * 3, rows * 3))  # Adjust figsize as needed

# Iterate and display images in the grid
for i, mv in enumerate(explore):
  z = current + mv
  img = generate_image(device, G, z)

  # Calculate row and column index for the current image
  row_idx = i // cols
  col_idx = i % cols

  # Display the image on the corresponding subplot
  ax = axes[row_idx, col_idx] if rows > 1 else axes[col_idx]  # Handle single row case
  ax.imshow(np.array(img))  # Convert PIL Image to NumPy array for imshow
  ax.axis('off')

# Adjust spacing between subplots
plt.tight_layout()
plt.show()