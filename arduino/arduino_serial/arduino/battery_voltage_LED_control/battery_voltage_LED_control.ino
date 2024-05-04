#include <FastLED.h>

// led config
#define NUM_LEDS 100
#define LED_DATA_PIN 3
#define NUM_STEPS 40

// ADC config
#define NUM_SAMPLES 50
#define ANALOG_IN A0
#define VOLTAGE_SCALE_FACTOR 4.6 //calculate this from voltage divider values (R1+R2)/R2
#define SAMPLE_TIME_PERIOD 5000 //ms

//globals
CRGB ledStrip[NUM_LEDS];
byte values[5];
int RGBT[4] = {0, 0, 0, 0};

bool led_state = false;
unsigned long voltage_start_time = 0;
unsigned long led_start_time = 0;

float readVoltage()
{
  float voltage = 0;
  unsigned long sum = 0;

  for (int i = 0; i < NUM_SAMPLES; i++)
  {
    sum += analogRead(ANALOG_IN);
  }

  voltage = (((float)sum / (float)NUM_SAMPLES) * 5.015) / 1024.0;
  return voltage * VOLTAGE_SCALE_FACTOR;
}


void writeValues(int R, int G, int B, int timePeriod) {
  timePeriod /= 2;
  if (timePeriod == 0) {
    fill_solid( ledStrip, NUM_LEDS, CRGB(R, G, B) );
    FastLED.show();
  }
  else
  {
    float finalColor[3] = {(float)R, (float)G, (float)B};
    float currentColor[3] = {0.0, 0.0, 0.0};

    for (int i = 0; i < NUM_STEPS; i++) {
      for (int j = 0; j < 3; j++) {
        currentColor[j] += finalColor[j] / NUM_STEPS;
      }
      fill_solid( ledStrip, NUM_LEDS, CRGB((int)currentColor[0],
                                           (int)currentColor[1],
                                           (int)currentColor[2]) );
      FastLED.show();
      delay((int)timePeriod / NUM_STEPS);
    }

    for (int i = 0; i < NUM_STEPS; i++) {
      for (int j = 0; j < 3; j++) {
        currentColor[j] -= finalColor[j] / NUM_STEPS;
      }
      fill_solid( ledStrip, NUM_LEDS, CRGB((int)currentColor[0],
                                           (int)currentColor[1],
                                           (int)currentColor[2]) );
      FastLED.show();
      delay((int)timePeriod / NUM_STEPS);
    }
  }
}

void setup() {
  FastLED.addLeds<WS2812B, LED_DATA_PIN, GRB>(ledStrip, NUM_LEDS);
  Serial.begin(9600);
  Serial.setTimeout(500);
  while (!Serial);
  writeValues(0, 0, 0, 0);
}


void loop() {

  while (Serial.available())
  {
    if (Serial.read() == '#')
    {

      size_t messageLength = Serial.readBytesUntil('\n', values, 5);
      if (messageLength == 5)
      {
        for (int i = 0; i < 3; i++)
        {
          RGBT[i] = (int)values[i];
        }
        RGBT[3] = values[3] << 8 | values[4];
        writeValues(RGBT[0], RGBT[1], RGBT[2], 0);
        led_state = true;
      }
    }
  }

  if (millis() - voltage_start_time > SAMPLE_TIME_PERIOD)
  {
    Serial.println(readVoltage());
    voltage_start_time = millis();
  }

  if (millis() - led_start_time > RGBT[3] / 2 && RGBT[3] != 0)
  {
    if (led_state)
    {
      writeValues(0, 0, 0, 0);
      led_state = false;
    }
    else
    {
      writeValues(RGBT[0], RGBT[1], RGBT[2], 0);
      led_state = true;
    }
    led_start_time = millis();
  }

}
