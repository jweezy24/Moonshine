#include "numutils.h"

#include <stdio.h>

int main(int argc, char* argv[]) {
    for (int i=0; i < 16; i++)
        printf("i=%d, 2^i=%ld\n", i, pow2(i));

    char* data[] = { "1", "10", "11", "100", "101", "110", "111", "000000", "11111", "1111111", "00000000", "20002" };

    char *hex_data[] = { "0", "10", "100", "101", "1000", "F", "FF", "A", "AA", "AG" };

    char *dec_data[] = { "10", "123", "1113", "1234", "1234A" };

    for (int i=0; i < sizeof(data) / sizeof(char*); i++) {
        int status;
        long value = binary_string_to_long(data[i], &status);
        if (status < 0)
            printf("Cannot convert %s\n", data[i]);
        else
            printf("%s = %ld\n", data[i], value);
    }

    for (int i=0; i < sizeof(hex_data) / sizeof(char*); i++) {
        int status;
        long value = any_string_to_long(hex_data[i], 16, &status);
        if (status < 0)
            printf("Cannot convert %s to base 16\n", hex_data[i]);
        else
            printf("%s = %ld\n", hex_data[i], value);
    }

    for (int i=0; i < sizeof(dec_data) / sizeof(char*); i++) {
        int status;
        long value = any_string_to_long(dec_data[i], 10, &status);
        if (status < 0)
            printf("Cannot convert %s to base 16\n", dec_data[i]);
        else
            printf("%s = %ld\n", dec_data[i], value);
    }
}
