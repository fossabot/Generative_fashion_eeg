#!/bin/bash
#SBATCH --job-name=train
#SBATCH --output=train%j.out
#SBATCH --error=train%j.err
#SBATCH --mem=32G
#SBATCH -p Abaki
#SBATCH --time=1-00:00:00

# Activate venv
source /venv/bin/activate

#navigate to stylegan
cd Generative_fashion_eeg/stylegan3


PYTHON=python3
TARGET_IMAGE_SIZE=1024
GAMMA=$(python3 -c "import numpy as np; print(0.5 * np.power(4, np.log2(${TARGET_IMAGE_SIZE}/128)))")

# Training
$PYTHON stylegan3/train.py \
  --outdir=./training-runs \
  --cfg=stylegan3-t \
  --data=./datasets/ffhq-${TARGET_IMAGE_SIZE}x${TARGET_IMAGE_SIZE}.zip \
  --gpus=2 \
  --batch=32 \
  --batch-gpu=16 \
  --gamma=$GAMMA \
  --mirror=1 \
  --kimg=5000 \
  --snap=5 \
  --metrics=none \
  --resume="/home/l/lauf/thesis/Generative_fashion_eeg/model/network-snapshot-005000.pkl"
