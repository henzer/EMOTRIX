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
  // An example of poor signal for emg could be one that oscillates between 0 and 3000.
  // An example of invalid heart rate could be one that oscillates between 0 and 145.
  sample = "{";
  bpm = random(0, 145);
  sample += "\"bpm\":" + String(bpm) + ",";
  emg = random(0, 3000);
  sample += "\"emg\":" + String(emg) + ",";
  sample += "\"chksum\":" + String(bpm + emg) + "}";

  Serial.println(sample);
}
