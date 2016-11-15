void setup() {
  Serial.begin(9600);
  while (!Serial) {
    // Esperamos a que se conecte el puerto serial
  }
}

void loop() {
  Serial.println("Hola mundo.");
}


