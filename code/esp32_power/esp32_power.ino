#define VOLTAGE_PIN 34
#define CURRENT_PIN 35

float voltage_scale = 0.50;   // adjust after calibration
float current_scale = 0.008;

void setup() {
  Serial.begin(115200);
}

float readVoltage() {
  int samples = 200;
  float sum = 0;
  float mean = 0;

  for (int i = 0; i < samples; i++) {
    float val = analogRead(VOLTAGE_PIN);
    mean += val;
    delayMicroseconds(200);
  }

  mean /= samples;

  for (int i = 0; i < samples; i++) {
    float val = analogRead(VOLTAGE_PIN) - mean;
    sum += val * val;
    delayMicroseconds(200);
  }

  float rms = sqrt(sum / samples);

  return (rms * voltage_scale) / 1.414;   // FIX: convert peak → RMS
}

float readCurrent() {
  int samples = 200;
  float sum = 0;
  float mean = 0;

  for (int i = 0; i < samples; i++) {
    float val = analogRead(CURRENT_PIN);
    mean += val;
    delayMicroseconds(200);
  }

  mean /= samples;

  for (int i = 0; i < samples; i++) {
    float val = analogRead(CURRENT_PIN) - mean;
    sum += val * val;
    delayMicroseconds(200);
  }

  float rms = sqrt(sum / samples);

  return rms * current_scale;
}

void loop() {
  float voltage = readVoltage();
  float current = readCurrent();

  Serial.print(voltage, 2);
  Serial.print(",");
  Serial.println(current, 3);

  delay(10);
}