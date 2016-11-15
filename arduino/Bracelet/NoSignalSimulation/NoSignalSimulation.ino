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
  // Signal with a maximum amplitude of 10, oscillating at the origin is not recognized.
  // If center is 32768, maximum and minimum aplitudes are 32773 and 32763, respectively. 
  sample = "{";
  bpm = random(0, 11);
  sample += "\"bpm\":" + String(bpm) + ",";
  emg = random(32763, 32774);
  sample += "\"emg\":" + String(emg) + ",";
  sample += "\"chksum\":" + String(bpm + emg) + "}";

  Serial.println(sample);
}
