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

#include "esp_log.h"
#include "sdkconfig.h"
#include "config.h"

static void
task_ac(void *arg) {
    printf("AC task started\n");
    while (1) {

    }

    vTaskDelete(NULL);
}

static void
task_temperature(void *arg) {
    printf("Temperature task started\n");
    while (1) {

    }

    vTaskDelete(NULL);
}

static void
task_motion(void *arg) {
    printf("Motion task started\n");
    while (1) {

    }

    vTaskDelete(NULL);
}

static void
task_alexa(void *arg) {
    printf("Alexa task started\n");
    while (1) {

    }

    vTaskDelete(NULL);
}

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
