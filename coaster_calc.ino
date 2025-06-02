float a[6] = {-0.28752426, 0.65608465, 0.71259527, 1.34370624, 1.01724109, 0.19113889};
float b[6] = {-1.06839961, 0.29822047, 0.35672293, -0.68326573, 0.68020521, 1.18480771};

float fx(float x, float y) {
  return a[0] + a[1]*x + a[2]*x*x + a[3]*x*y + a[4]*y + a[5]*y*y;
}

float fy(float x, float y) {
  return b[0] + b[1]*x + b[2]*x*x + b[3]*x*y + b[4]*y + b[5]*y*y;
}

float x = 0.05;
float y = 0.05;
const float clampValue = 10000.0;
bool startRequested = false;

void setup() {
  Serial.begin(115200);
  while (!Serial);  // Wait for Serial monitor or Python connection
  Serial.println("READY");
}

void loop() {
  if (Serial.available()) {
    String command = Serial.readStringUntil('\n');
    command.trim();
    if (command == "START") {
      Serial.println("START");
      startRequested = true;
    }
  }

  if (startRequested) {
    for (unsigned long i = 0; i < 1000000; i++) {
      float new_x = fx(x, y);
      float new_y = fy(x, y);

      if (isnan(new_x) || isnan(new_y) || isinf(new_x) || isinf(new_y)) {
        Serial.println("STOP");
        while (1);
      }

      x = constrain(new_x, -clampValue, clampValue);
      y = constrain(new_y, -clampValue, clampValue);

      Serial.print(x, 4);
      Serial.print(",");
      Serial.println(y, 4);
    }

    Serial.println("DONE");
    startRequested = false;
    while (1); // freeze
  }
}
