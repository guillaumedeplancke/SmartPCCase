#include <Filters.h>

float frequency = 50;
float statsSec = 40.0 / frequency;

// voltage measurement variables
RunningStatistics voltageStats;
float last_voltage;
float intercept = -0.04;
float slope = 0.036;
int sensor = 0;

// current measurement variables
float last_current;
float accuracy = 0.1;
float max_current_measurement = 0;
float current_measurement_counter = 0;

void setup() {
  voltageStats.setWindowSecs(statsSec);

  pinMode(13, INPUT);

  Serial.begin(9600);
  Serial.setTimeout(10);
}

void loop() {
  // voltage measurement
  sensor = analogRead(A0);
  voltageStats.input(sensor);

  last_voltage = intercept + slope * voltageStats.sigma();
  last_voltage = last_voltage * (40.3231);


  // current measurement
  float current_sensor_reading = analogRead(A2);
  current_sensor_reading = current_sensor_reading * 5.0 / 1024.0;
  current_sensor_reading = current_sensor_reading - 2.5;
  current_sensor_reading = current_sensor_reading * 1000;

  float current = current_sensor_reading / 0.1 / 1000;

  max_current_measurement = max(current, max_current_measurement);

  if (current_measurement_counter > 100) {
    last_current = max_current_measurement;

    current_measurement_counter = 0;
    max_current_measurement = 0;
  }


  // serial output
  if (digitalRead(13)) {
    Serial.println("V " + String(last_voltage) + " A " + String(last_current));
  }
  
  /*Serial.print("V: ");
    Serial.print(last_voltage);
    Serial.print(" A: ");
    Serial.println(last_current);*/

  // other code
  current_measurement_counter++;
}
