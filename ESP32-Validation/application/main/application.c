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
#include "driver/ledc.h"
#include "freertos/FreeRTOS.h"
#include "freertos/task.h"
#include "freertos/semphr.h"
#include "esp_log.h"
#include "esp_adc/adc_oneshot.h"
#include "sdkconfig.h"
#include "config.h"

#ifdef DEVICE_ALEXA
static void
task_alexa(void *arg) {
    int motion, temperature;
    int prev_motion = -1, prev_temperature = -1;
    printf("Alexa task started\n");

    gpio_config_t io_conf = {};
    io_conf.intr_type = GPIO_INTR_DISABLE;
    io_conf.mode = GPIO_MODE_OUTPUT;
    io_conf.pin_bit_mask = (1ULL<<PIN_GPIO_OUT);
    io_conf.pull_down_en = 0;
    io_conf.pull_up_en = 0;
    gpio_config(&io_conf);

    io_conf.pin_bit_mask = (1ULL<<PIN_GPIO_MOTION) | (1ULL<<PIN_GPIO_TEMPERATURE);
    io_conf.mode = GPIO_MODE_INPUT;
    io_conf.pull_down_en = 0;
    io_conf.pull_up_en = 0;
    gpio_config(&io_conf);
    
    gpio_set_level(PIN_GPIO_OUT, 0);

    while (1) {
        motion = gpio_get_level(PIN_GPIO_MOTION);
        temperature = gpio_get_level(PIN_GPIO_TEMPERATURE);
        if (prev_motion == 0 && motion == 1) {
            printf("Motion detected\n");
        }
        if (prev_temperature == 0 && temperature == 1) {
            printf("Temperature detected\n");
            if (motion == 1 && temperature == 1) {
                printf("AC turned on!\n")
            }
        }
        prev_motion = motion;
        prev_temperature = temperature;

		vTaskDelay(pdMS_TO_TICKS(10));
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
    io_conf.intr_type = GPIO_INTR_DISABLE;
    io_conf.mode = GPIO_MODE_OUTPUT;
    io_conf.pin_bit_mask = (1ULL<<PIN_GPIO_OUT);
    io_conf.pull_down_en = 0;
    io_conf.pull_up_en = 0;
    gpio_config(&io_conf);

    adc_oneshot_unit_handle_t adc1_handle;
    adc_oneshot_unit_init_cfg_t init_config1 = {
        .unit_id = ADC_UNIT_1,
    };    ESP_ERROR_CHECK(adc_oneshot_new_unit(&init_config1, &adc1_handle));

    adc_oneshot_chan_cfg_t config = {
        .bitwidth = ADC_BITWIDTH_DEFAULT,
        .atten = ADC_ATTEN_DB_11,
    };
    ESP_ERROR_CHECK(adc_oneshot_config_channel(adc1_handle, PIN_ADC_TEMPERATURE, &config));

    while (1) {
        ESP_ERROR_CHECK(adc_oneshot_read(adc1_handle, PIN_ADC_TEMPERATURE, &input_temperature_raw));
        
        // printf("Temperature: %d\n", input_temperature_raw);
        overtemp = input_temperature_raw >= 2048;

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
    io_conf.intr_type = GPIO_INTR_DISABLE;
    io_conf.mode = GPIO_MODE_OUTPUT;
    io_conf.pin_bit_mask = (1ULL<<PIN_GPIO_OUT);
    io_conf.pull_down_en = 0;
    io_conf.pull_up_en = 0;
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
    printf("AC task started\n");

    gpio_config_t io_conf = {};
    io_conf.intr_type = GPIO_INTR_DISABLE;
    io_conf.mode = GPIO_MODE_OUTPUT;
    io_conf.pin_bit_mask = (1ULL<<PIN_GPIO_ALEXA);
    io_conf.pull_down_en = 0;
    io_conf.pull_up_en = 0;
    gpio_config(&io_conf);
    
    while (1) {

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
