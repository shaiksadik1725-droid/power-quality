import numpy as np
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SAVE_PATH = os.path.join(BASE_DIR, "..", "dataset")

SAMPLES_PER_CLASS = 1000
WINDOW_SIZE = 128

CLASSES = ["Normal","Sag","Swell","Interruption","Transient","Harmonics","Flicker","Notching"]

os.makedirs(SAVE_PATH, exist_ok=True)

def generate_signal(label):
    t = np.linspace(0, 1, WINDOW_SIZE)

    v = 230 + 10*np.sin(2*np.pi*50*t)
    i = 0.1*np.sin(2*np.pi*50*t)

    if label == "Sag":
        i *= 0.3
    elif label == "Swell":
        i *= 2
    elif label == "Interruption":
        i *= 0.01
    elif label == "Transient":
        spike = np.zeros(WINDOW_SIZE)
        spike[np.random.randint(10, 100)] = 5
        i += spike
    elif label == "Harmonics":
        i += 0.05*np.sin(2*np.pi*150*t)
    elif label == "Flicker":
        i *= (1 + 0.5*np.sin(2*np.pi*5*t))
    elif label == "Notching":
        for k in range(10, WINDOW_SIZE, 20):
            i[k:k+3] -= 0.2

    noise = np.random.normal(0, 0.01, WINDOW_SIZE)
    i += noise

    return np.column_stack((v, i))

for idx, label in enumerate(CLASSES):
    X = []
    y = []

    for _ in range(SAMPLES_PER_CLASS):
        X.append(generate_signal(label))
        y.append(idx)

    file_path = os.path.join(SAVE_PATH, f"{label}.npz")
    np.savez(file_path, X=np.array(X), y=np.array(y))

print("Dataset Generated at:", SAVE_PATH)