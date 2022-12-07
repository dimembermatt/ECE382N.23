
#include "driver/gpio.h"
#include "esp_adc/adc_oneshot.h"

#define DEVICE_ALEXA
// #define DEVICE_TEMPERATURE
// #define DEVICE_MOTION
// #define DEVICE_AC

#ifdef DEVICE_ALEXA
#define PIN_LED 5
#define PIN_GPIO_TEMPERATURE 0
#define PIN_GPIO_MOTION 1
#define PIN_GPIO_OUT 2
#endif

#ifdef DEVICE_TEMPERATURE
#define PIN_GPIO_OUT 0
#define PIN_ADC_TEMPERATURE ADC_CHANNEL_1  // pin 1
#endif

#ifdef DEVICE_MOTION
#define PIN_GPIO_OUT 0
#define PIN_GPIO_MOTION 1
#endif

#ifdef DEVICE_AC
#define PIN_GPIO_ALEXA 0
#endif