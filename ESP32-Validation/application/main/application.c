/*
 * SPDX-FileCopyrightText: 2022 Espressif Systems (Shanghai) CO LTD
 *
 * SPDX-License-Identifier: Unlicense OR CC0-1.0
 */
/* i2c - Example

   For other examples please check:
   https://github.com/espressif/esp-idf/tree/master/examples

   See README.md file to get detailed usage of this example.

   This example code is in the Public Domain (or CC0 licensed, at your option.)

   Unless required by applicable law or agreed to in writing, this
   software is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR
   CONDITIONS OF ANY KIND, either express or implied.
*/
#include <stdio.h>

#include "config.h"
#include "driver/ledc.h"
#include "esp_adc/adc_oneshot.h"
#include "esp_log.h"
#include "freertos/FreeRTOS.h"
#include "freertos/semphr.h"
#include "freertos/task.h"
#include "led_strip.h"
#include "sdkconfig.h"


static led_strip_handle_t led_strip;

static void
ledc_init(void) {
	led_strip_config_t strip_config = {
	    .strip_gpio_num = 8,
	    .max_leds       = 1,  // at least one LED on board
	};
	led_strip_rmt_config_t rmt_config = {
	    .resolution_hz = 10 * 1000 * 1000,  // 10MHz
	};
	ESP_ERROR_CHECK(
	    led_strip_new_rmt_device(&strip_config, &rmt_config, &led_strip));
	/* Set all LED off to clear all pixels */
	led_strip_clear(led_strip);
}

void
set_ledc(int on) {
	/* If the addressable LED is enabled */
	if (on == 1) {
		led_strip_set_pixel(led_strip, 0, 255, 255, 255);
		led_strip_refresh(led_strip);
	} else if (on == 2) {
		led_strip_set_pixel(led_strip, 0, 0, 255, 255);
		led_strip_refresh(led_strip);
	} else {
		led_strip_clear(led_strip);
	}
}

#ifdef DEVICE_ALEXA
static void
task_alexa(void *arg) {
	int motion, temperature, AC = 0, in_house = 0;
	int prev_motion = -1, prev_temperature = -1;
	printf("Alexa task started\n");

	gpio_config_t io_conf = {};
	io_conf.intr_type     = GPIO_INTR_DISABLE;
	io_conf.mode          = GPIO_MODE_OUTPUT;
	io_conf.pin_bit_mask  = (1ULL << PIN_GPIO_OUT);
	io_conf.pull_down_en  = 0;
	io_conf.pull_up_en    = 0;
	gpio_config(&io_conf);

	io_conf.pin_bit_mask =
	    (1ULL << PIN_GPIO_MOTION) | (1ULL << PIN_GPIO_TEMPERATURE);
	io_conf.mode         = GPIO_MODE_INPUT;
	io_conf.pull_down_en = 0;
	io_conf.pull_up_en   = 0;
	gpio_config(&io_conf);

	gpio_set_level(PIN_GPIO_OUT, 0);
	ledc_init();

	while (1) {
		motion      = gpio_get_level(PIN_GPIO_MOTION);
		temperature = gpio_get_level(PIN_GPIO_TEMPERATURE);
		if (prev_motion == 0 && motion == 1) {
			in_house = !in_house;
			if (AC == 0 && in_house == 1 && temperature == 1) {
				printf("AC turned on!\n");
				AC = 1;
				gpio_set_level(PIN_GPIO_OUT, AC);
				set_ledc(2);
				vTaskDelay(pdMS_TO_TICKS(500));
				set_ledc(0);
			}
		}
		if (prev_temperature == 0 && temperature == 1) {
			if (AC == 0 && in_house == 1) {
				printf("AC turned on!\n");
				AC = 1;
				gpio_set_level(PIN_GPIO_OUT, AC);
				set_ledc(2);
				vTaskDelay(pdMS_TO_TICKS(500));
				set_ledc(0);
			}
		}
		if (AC == 1 && in_house == 0) {
			printf("AC turned off!\n");
			AC = 0;
			gpio_set_level(PIN_GPIO_OUT, AC);
			set_ledc(2);
			vTaskDelay(pdMS_TO_TICKS(500));
			set_ledc(0);
		}
		if (AC == 1 && prev_temperature == 1 && temperature == 0) {
			printf("AC turned off!\n");
			AC = 0;
			gpio_set_level(PIN_GPIO_OUT, AC);
			set_ledc(2);
			vTaskDelay(pdMS_TO_TICKS(500));
			set_ledc(0);
		}

		prev_motion      = motion;
		prev_temperature = temperature;

		vTaskDelay(pdMS_TO_TICKS(100));
	}

	vTaskDelete(NULL);
}
#endif

#ifdef DEVICE_TEMPERATURE
static void
task_temperature(void *arg) {
	int input_temperature_raw;
	int temperature, overtemp, prev_overtemp = -1;
	printf("Temperature task started\n");

	gpio_config_t io_conf = {};
	io_conf.intr_type     = GPIO_INTR_DISABLE;
	io_conf.mode          = GPIO_MODE_OUTPUT;
	io_conf.pin_bit_mask  = (1ULL << PIN_GPIO_OUT);
	io_conf.pull_down_en  = 0;
	io_conf.pull_up_en    = 0;
	gpio_config(&io_conf);
	io_conf.mode          = GPIO_MODE_OUTPUT;
	io_conf.pin_bit_mask  = (1ULL << PIN_TASK_ADC);
	gpio_config(&io_conf);

	adc_oneshot_unit_handle_t adc1_handle;
	adc_oneshot_unit_init_cfg_t init_config1 = {
	    .unit_id = ADC_UNIT_1,
	};
	ESP_ERROR_CHECK(adc_oneshot_new_unit(&init_config1, &adc1_handle));

	adc_oneshot_chan_cfg_t config = {
	    .bitwidth = ADC_BITWIDTH_DEFAULT,
	    .atten    = ADC_ATTEN_DB_11,
	};
	ESP_ERROR_CHECK(
	    adc_oneshot_config_channel(adc1_handle, PIN_ADC_TEMPERATURE, &config));

	float temperature_reading = 0;

	while (1) {

		gpio_set_level(PIN_TASK_ADC, 1);
		for (int i = 0; i < 100; i++) {
		ESP_ERROR_CHECK(adc_oneshot_read(
		    adc1_handle, PIN_ADC_TEMPERATURE, &input_temperature_raw));
		}
		gpio_set_level(PIN_TASK_ADC, 0);

		// printf("Temperature: %d\n", input_temperature_raw);
		temperature_reading =
		    temperature_reading * 0.8 + input_temperature_raw * 0.2;
		overtemp = temperature_reading >= 2048;

		if (prev_overtemp == 0 && overtemp == 1) {
			printf("Overtemp active\n");
			gpio_set_level(PIN_GPIO_OUT, 1);
		} else if (prev_overtemp == 1 && overtemp == 0) {
			printf("Overtemp inactive\n");
			gpio_set_level(PIN_GPIO_OUT, 0);
		}

		vTaskDelay(pdMS_TO_TICKS(100));
		prev_overtemp = overtemp;
	}

	vTaskDelete(NULL);
}
#endif

#ifdef DEVICE_MOTION
static void
task_motion(void *arg) {
	int motion, prev_motion = -1;
	printf("Motion task started\n");
	// ledc_stop(0, 0, 0);
	gpio_config_t io_conf = {};
	io_conf.intr_type     = GPIO_INTR_DISABLE;
	io_conf.mode          = GPIO_MODE_OUTPUT;
	io_conf.pin_bit_mask  = (1ULL << PIN_GPIO_OUT);
	io_conf.pull_down_en  = 0;
	io_conf.pull_up_en    = 0;
	gpio_config(&io_conf);

	io_conf.pin_bit_mask = (1ULL << PIN_GPIO_MOTION);
	io_conf.mode         = GPIO_MODE_INPUT;
	io_conf.pull_down_en = 0;
	io_conf.pull_up_en   = 1;
	gpio_config(&io_conf);

	while (1) {
		motion = gpio_get_level(PIN_GPIO_MOTION);

		if (prev_motion == 0 && motion == 1) {
			printf("Motion activated\n");
			gpio_set_level(PIN_GPIO_OUT, 1);
		} else if (prev_motion == 1 && motion == 0) {
			printf("Motion inactivated\n");
			gpio_set_level(PIN_GPIO_OUT, 0);
		}
		prev_motion = motion;

		vTaskDelay(pdMS_TO_TICKS(100));
	}

	vTaskDelete(NULL);
}
#endif

#ifdef DEVICE_AC
static void
task_ac(void *arg) {
	int alexa_input;
	printf("AC task started\n");

	gpio_config_t io_conf = {};
	io_conf.intr_type     = GPIO_INTR_DISABLE;
	io_conf.mode          = GPIO_MODE_INPUT;
	io_conf.pin_bit_mask  = (1ULL << PIN_GPIO_ALEXA);
	io_conf.pull_down_en  = 0;
	io_conf.pull_up_en    = 0;
	gpio_config(&io_conf);

	io_conf.intr_type    = GPIO_INTR_DISABLE;
	io_conf.mode         = GPIO_MODE_OUTPUT;
	io_conf.pin_bit_mask = (1ULL << PIN_GPIO_OUT);
	io_conf.pull_down_en = 0;
	io_conf.pull_up_en   = 0;
	gpio_config(&io_conf);

	ledc_init();
	gpio_set_level(PIN_GPIO_OUT, 0);

	while (1) {
		alexa_input = gpio_get_level(PIN_GPIO_ALEXA);
		vTaskDelay(pdMS_TO_TICKS(50));
		if (alexa_input == 1) {
			set_ledc(1);
			gpio_set_level(PIN_GPIO_OUT, 1);
		} else {
			set_ledc(0);
			gpio_set_level(PIN_GPIO_OUT, 0);
		}

		vTaskDelay(pdMS_TO_TICKS(100));
	}

	vTaskDelete(NULL);
}
#endif

void
app_main(void) {
#ifdef DEVICE_AC
	xTaskCreate(task_ac, "", 1024 * 2, (void *) 1, 10, NULL);
#endif
#ifdef DEVICE_TEMPERATURE
	xTaskCreate(task_temperature, "", 1024 * 2, (void *) 1, 10, NULL);
#endif
#ifdef DEVICE_MOTION
	xTaskCreate(task_motion, "", 1024 * 2, (void *) 1, 10, NULL);
#endif
#ifdef DEVICE_ALEXA
	xTaskCreate(task_alexa, "", 1024 * 2, (void *) 1, 10, NULL);
#endif
}
