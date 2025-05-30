
import torch
import numpy as np
import matplotlib.pyplot as plt

###### SIMULATION von CHAT GPT für test und verständnis zwecke ####

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print(f"Verwendetes Gerät: {device}")

# Bewertungen der Nutzer auf die Bilder von 1-100
values=[93,3,17,82]
# multi objective
def multi_objective_bewertungsfunktion(values):
   values.sort()
   return (values[len(values)-2], values[len(values)-1])

print(multi_objective_bewertungsfunktion(values))

import torch
import numpy as np
import matplotlib.pyplot as plt


device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print(f"Verwendetes Gerät: {device}")

latent_dim = 10  # Dimension of lat. vec.
num_vectors = 100 # am of vec in space
# Bewertungen der Nuter auf die Bilder von 1-100
values=[93,40,80,82]
latent_space = torch.randn(num_vectors, latent_dim, device=device)
#print(f"Form des latenten Raums: {latent_space.shape}")

# 2. multi objective
def multi_objective_bewertungsfunktion(values):
   values.sort()
   print(values)
   ziel1=values[len(values)-2]
   ziel2=values[len(values)-1]
   return torch.tensor([ziel1.item(), ziel2.item()], device=values.device)

# 3.bewetrung (now vectors)
bewertungen = torch.stack([multi_objective_bewertungsfunktion(latent_space[i]) for i in range(num_vectors)])
#print(f"Form der initialen Bewertungen: {bewertungen.shape}")
num_ziele = bewertungen.shape[1]

# estimation of Pareto-dominacne
def dominiert(punkt_a, punkt_b):
    besser_oder_gleich = (punkt_a >= punkt_b).all()
    besser_in_mindestens_einem = (punkt_a > punkt_b).any()
    return besser_oder_gleich and besser_in_mindestens_einem

#find front
def finde_pareto_front(bewertungen_np):
    pareto_front_indices = []
    for i, bewertung_a in enumerate(bewertungen_np):
        dominiert_von_irgendwem = False
        for j, bewertung_b in enumerate(bewertungen_np):
            if i != j and dominiert(bewertung_b, bewertung_a):
                dominiert_von_irgendwem = True
                break
        if not dominiert_von_irgendwem:
            pareto_front_indices.append(i)
    return pareto_front_indices

# 4. Bayes-similar selection process over iteratios
num_iterationen = 10
top_k = 40 # make it higher

for iteration in range(num_iterationen):
    #print(f"\n--- Iteration {iteration + 1} ---")

    # a) Finde die aktuelle Pareto-Front
    bewertungen_np = bewertungen.cpu().numpy()
    pareto_indices = finde_pareto_front(bewertungen_np)
    pareto_vektoren = latent_space[pareto_indices]
    pareto_bewertungen = bewertungen[pareto_indices].cpu().numpy()

    if len(pareto_indices) == 0:
        print("Keine Pareto-Vektoren")
        break

    # b) "Bayes-ähnliche" Gewichtung
    wahrscheinlichkeiten = np.ones(len(pareto_indices)) / len(pareto_indices)

    # c) Suche der Eltern-Vektoren
    eltern_indices = np.random.choice(len(pareto_indices), size=num_vectors, replace=True, p=wahrscheinlichkeiten)
    eltern_vektoren = pareto_vektoren[eltern_indices]

    # d) Erzeugung neuer Vektoren (Mutation)
    noise = torch.randn_like(eltern_vektoren) * 0.05
    neue_latent_space = eltern_vektoren + noise
    latent_space = neue_latent_space.to(device)

    # e) Bewertung der neuen Vektoren
    neue_bewertungen = torch.stack([multi_objective_bewertungsfunktion(latent_space[i]) for i in range(num_vectors)])
    bewertungen = neue_bewertungen

    # Visualisierung (nur für 2 Ziele)
    if num_ziele == 2:
        plt.figure(figsize=(8, 6))
        plt.scatter(bewertungen_np[:, 0], bewertungen_np[:, 1], label='Alle Vektoren')
        plt.scatter(pareto_bewertungen[:, 0], pareto_bewertungen[:, 1], color='red', label='Pareto-Front')
        plt.xlabel('Ziel 1')
        plt.ylabel('Ziel 2')
        plt.title(f'Pareto-Front - Iteration {iteration + 1}')
        plt.legend()
        plt.grid(True)
        plt.show()
    elif num_ziele > 2:
        print("Visualisierung ist nur für 2 Ziele implementiert.")

# Nach den Iterationen die finale Pareto-Front finden und visualisieren
finale_bewertungen_np = bewertungen.cpu().numpy()
finale_pareto_indices = finde_pareto_front(finale_bewertungen_np)
beste_finale_pareto_bewertungen = finale_bewertungen_np[finale_pareto_indices]
beste_finale_pareto_vektoren = latent_space[finale_pareto_indices].cpu().numpy()

# Finale Visualisierung (nur für 2 Ziele)
if num_ziele == 2:
    plt.figure(figsize=(8, 6))
    plt.scatter(finale_bewertungen_np[:, 0], finale_bewertungen_np[:, 1], label='Alle finalen Vektoren')
    plt.scatter(beste_finale_pareto_bewertungen[:, 0], beste_finale_pareto_bewertungen[:, 1], color='red', label='Finale Pareto-Front')
    plt.xlabel('Ziel 1')
    plt.ylabel('Ziel 2')
    plt.title('Finale Pareto-Front')
    plt.legend()
    plt.grid(True)
    plt.show()
elif num_ziele > 2:
    print("Finale Visualisierung ist nur für 2 Ziele implementiert.")