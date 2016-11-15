String sample;
int bpm;
long emg;

void setup() {
  Serial.begin(115200);
  while (!Serial) {
    // Esperamos a que se conecte el puerto serial
  }

  randomSeed(analogRead(0));
}

void loop() {
  // Good signal should oscillates between 0 and 65535.
  // Valid heart rate must be between 150 and 200.
  sample = "{";
  bpm = random(75, 200);
  sample += "\"bpm\":" + String(bpm) + ",";
  emg = random(0, 65536);
  sample += "\"emg\":" + String(emg) + ",";
  sample += "\"chksum\":" + String(bpm + emg) + "}";

  Serial.println(sample);
}
