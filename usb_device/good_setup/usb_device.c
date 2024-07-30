#include <stdio.h>
#include <stdlib.h>
#include "pico/stdlib.h"
#include "hardware/uart.h"
#include "mbedtls/rsa.h"
#include "mbedtls/pk.h"
#include "tusb.h"

// Public key for encryption
const char *public_key_pem = "-----BEGIN PUBLIC KEY-----\n"
                             "YOUR_PUBLIC_KEY_HERE"
                             "-----END PUBLIC KEY-----\n";

// Function to initialize the RSA context
void init_rsa_context(mbedtls_pk_context *pk) {
    mbedtls_pk_init(pk);
    if (mbedtls_pk_parse_public_key(pk, (const unsigned char *)public_key_pem, strlen(public_key_pem) + 1) != 0) {
        printf("Failed to parse public key\n");
        while (1) tight_loop_contents();
    }
}

// Function to encrypt data using the public key
int rsa_encrypt(mbedtls_pk_context *pk, const unsigned char *input, size_t input_len, unsigned char *output) {
    return mbedtls_pk_encrypt(pk, input, input_len, output, &input_len, sizeof(output), mbedtls_ctr_drbg_random, NULL);
}

// Function to send encrypted message
void send_encrypted_message(const char *message, mbedtls_pk_context *pk) {
    unsigned char encrypted[256];
    if (rsa_encrypt(pk, (unsigned char *)message, strlen(message), encrypted) != 0) {
        printf("Failed to encrypt message\n");
        return;
    }
    uart_write_blocking(uart0, encrypted, sizeof(encrypted));
}

int main() {
    // Initialize USB
    tusb_init();
   
    // Initialize UART for communication
    uart_init(uart0, 115200);
    gpio_set_function(0, GPIO_FUNC_UART);
    gpio_set_function(1, GPIO_FUNC_UART);

    // Initialize RSA context
    mbedtls_pk_context pk;
    init_rsa_context(&pk);

    // Send authentication key
    const char *auth_key = "AUTHENTICATION_KEY";
    send_encrypted_message(auth_key, &pk);

    while (true) {
        // Wait for keypress
        if (tud_hid_ready()) {
            if (tud_hid_keyboard_keycode[0] != 0) {
                // Send encrypted message
                const char *message = "KEYPRESS_DETECTED";
                send_encrypted_message(message, &pk);
            }
        }
        sleep_ms(100);
    }

    mbedtls_pk_free(&pk);
    return 0;
}
