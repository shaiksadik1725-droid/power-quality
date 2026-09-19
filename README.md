# AI-Based Power Quality Classification

A power-quality monitoring project that combines voltage/current measurements with machine learning to identify common electrical disturbances.

## Classes
- Normal
- Sag
- Swell
- Interruption
- Transient
- Harmonics
- Flicker
- Notching

## Machine Learning
The repository contains a TensorFlow/Keras 1D CNN trained on voltage-current signal windows, together with preprocessing parameters and real-time monitoring code.

## Technology
Python, TensorFlow/Keras, NumPy, scikit-learn, Matplotlib, serial communication, ESP32/embedded acquisition.

## Structure
```text
power-quality/
├── code/
│   ├── generate_dataset.py
│   ├── train_cnn.py
│   ├── realtime_predict.py
│   └── esp32_power/
├── dataset/
├── models/
├── Components/
└── Result/
```

## Training
```bash
python code/train_cnn.py
```

## Real-Time Monitoring
Update the serial port and model paths in the runtime script, connect the measurement hardware, then run:

```bash
python code/realtime_predict.py
```

## Future Improvements
- Remove machine-specific absolute paths
- Use the trained CNN directly for all live classifications
- Add RMS, THD, frequency, and power-factor features
- Add streaming plots and event logging
- Validate against laboratory power-quality events

## Author
**Sadik Shaik**
