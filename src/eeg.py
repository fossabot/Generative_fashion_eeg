import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import random

# Simulation params
n_channels = 8
sampling_rate = 250
duration = 1.0
n_timepoints = int(duration * sampling_rate)
time = np.linspace(0, duration, n_timepoints)

# ERP
def generate_erp_component(time, peak_time=0.3, amplitude=5.0, width=0.05):
    return amplitude * np.exp(-0.5 * ((time - peak_time) / width) ** 2)

# Dummy-data simulation
def create_fake_dataset(n_trials=30):
    data = []
    labels = []
    for _ in range(n_trials):
        label = random.choice(["cat", "dog", "car"])
        trial = []
        for _ in range(n_channels):
            noise = np.random.normal(0, 1, n_timepoints)
            erp = generate_erp_component(time) if random.random() > 0.5 else 0
            signal = noise + erp
            trial.append(signal)
        data.append(np.array(trial))
        labels.append(label)
    return data, labels

# Daten laden
erp_data, labels = create_fake_dataset()

