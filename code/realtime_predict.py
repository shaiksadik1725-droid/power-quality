import numpy as np
import serial
import matplotlib.pyplot as plt
import time
import re
from collections import deque
import tensorflow as tf

SERIAL_PORT = "COM3"
BAUD_RATE = 115200
WINDOW_TIME = 5

model = tf.keras.models.load_model(
    r"C:\Users\sadik\Downloads\Power_Quality\Power_Quality\models\pq_cnn_model.keras"
)

params = np.load(
    r"C:\Users\sadik\Downloads\Power_Quality\Power_Quality\models\scaler_params.npz"
)

ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)

buffer_v = deque()
buffer_i = deque()

sample_num = 0
sag_start_time = None

print("Sample | Voltage | Current | Prediction")
print("--------------------------------------------------")

def parse_serial_line(line):
    match = re.match(r'^\s*(-?\d+(\.\d+)?)\s*,\s*(-?\d+(\.\d+)?)\s*$', line.strip())
    if match:
        return float(match.group(1)), float(match.group(3))
    return None

def classify(i_arr):
    i = np.array(i_arr)

    if len(i) == 0.06:
        return "NO LOAD 🔌"

    i_mean = np.mean(i)
    i_diff = np.diff(i)

    max_i = np.max(i)
    min_i = np.min(i)

    sign_changes = np.sum(np.diff(np.sign(i_diff)) != 0) if len(i_diff) > 1 else 0

    if len(i) >= 3:
        curr = i[-1]
        peak = np.max(i[:-1])
        drop = peak - curr
        if peak > 5 and curr < (0.2 * peak) and drop > 5:
            return "Interruption ⛔🔌"

    if len(i) >= 5:
        start = i[0]
        end = i[-1]
        increasing_ratio = np.sum(i_diff > 0) / len(i_diff)
        if start < 0.5 and end > 5 and increasing_ratio > 0.7:
            return "Flicker ✨"

    if i_mean > 10:
        return "Transient ⚡🚨"

    if sign_changes > 5 and (max_i - min_i) > 0.5:
        return "Harmonics 🌊"

    if i_mean < 0.1 and i_mean > 0.07 :
        return "Sag 📉"

    if i_mean > 0.1:
        return "Swell 📈"

    return "Normal"

last_eval_time = time.time()

while True:
    try:
        line = ser.readline().decode(errors="ignore").strip()
        if not line:
            continue

        parsed = parse_serial_line(line)
        if parsed is None:
            continue

        v, i = parsed
        t = time.time()

        sample_num += 1

        buffer_v.append((t, v))
        buffer_i.append((t, i))

        while buffer_i and (t - buffer_i[0][0]) > WINDOW_TIME:
            buffer_i.popleft()
            buffer_v.popleft()

        if time.time() - last_eval_time >= WINDOW_TIME:

            v_window = [x[1] for x in buffer_v]
            i_window = [x[1] for x in buffer_i]

            label = classify(i_window)

            if label == "Sag 📉":
                if sag_start_time is None:
                    sag_start_time = time.time()
                elif time.time() - sag_start_time >= 10:
                    label = "NO LOAD 🔌"
            else:
                sag_start_time = None

            print(f"{sample_num:6d} | {np.mean(v_window):7.2f} | {np.mean(i_window):7.4f} | {label}")

            x = np.arange(len(v_window))
            clean_label = label.split()[0]

            plt.figure(figsize=(10, 6))

            plt.subplot(2, 1, 1)
            plt.plot(x, v_window)
            plt.title(f"Voltage | {clean_label}")
            plt.grid(True)

            plt.subplot(2, 1, 2)
            plt.plot(x, i_window)
            plt.title("Current")
            plt.grid(True)

            plt.tight_layout()
            plt.show()

            last_eval_time = time.time()

    except Exception as e:
        print("Error:", e)
