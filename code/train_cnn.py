import numpy as np
import tensorflow as tf
import os
from sklearn.model_selection import train_test_split

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATASET_DIR = os.path.join(BASE_DIR, "..", "dataset")
MODEL_DIR = os.path.join(BASE_DIR, "..", "models")

CLASSES = ["Normal","Sag","Swell","Interruption","Transient","Harmonics","Flicker","Notching"]

os.makedirs(MODEL_DIR, exist_ok=True)

X_all = []
y_all = []

for i, label in enumerate(CLASSES):
    file_path = os.path.join(DATASET_DIR, f"{label}.npz")

    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Missing dataset file: {file_path}")

    data = np.load(file_path)
    X_all.append(data["X"])
    y_all.append(data["y"])

X = np.vstack(X_all)
y = np.hstack(y_all)

print("Dataset loaded:", X.shape, y.shape)

X_mean = X.mean(axis=(0,1))
X_std = X.std(axis=(0,1)) + 1e-6

X = (X - X_mean) / X_std

np.savez(os.path.join(MODEL_DIR, "scaler_params.npz"), X_mean=X_mean, X_std=X_std)

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

model = tf.keras.Sequential([
    tf.keras.layers.Conv1D(32, 3, activation='relu', input_shape=(128,2)),
    tf.keras.layers.MaxPooling1D(2),

    tf.keras.layers.Conv1D(64, 3, activation='relu'),
    tf.keras.layers.MaxPooling1D(2),

    tf.keras.layers.Flatten(),
    tf.keras.layers.Dense(64, activation='relu'),
    tf.keras.layers.Dense(len(CLASSES), activation='softmax')
])

model.compile(
    optimizer='adam',
    loss='sparse_categorical_crossentropy',
    metrics=['accuracy']
)

model.fit(
    X_train, y_train,
    epochs=15,
    batch_size=32,
    validation_data=(X_test, y_test)
)

model.save(os.path.join(MODEL_DIR, "pq_cnn_model.keras"))

loss, acc = model.evaluate(X_test, y_test)
print("Test Accuracy:", acc)