#include <stdio.h>

long pow2(int n) {
    if (n < 0) return 0;
    return 1 << n;
}

long  binary_string_to_long(char* bstring, int *status) {
    char* p;
    long result = 0;
    *status = 0; /* success assumed until proven otherwise */
    for (p=bstring; *p; p++) {
        switch(*p) {
        case '0':
            result = (result << 1) | 0x0;
            break;
        case '1':
            result = (result << 1) | 0x1;
            break;
        default:
            *status = -1;
            break;
        }
    }
    return result;
}

/* generalizes the binary string to long above */
long  any_string_to_long(char* any_string, int base, int *status) {
    char* p;
    long result = 0;
    *status = 0; /* success assumed until proven otherwise */
    if (base > 36) {
        *status = -1;
        return 0;
    }

    for (p=any_string; *p; p++) {
        int digit_value;
        if (*p >= '0' && *p <= '9')
            digit_value = *p - '0';
        else if (*p >= 'A' && *p <= 'Z')
            digit_value = *p - 'A' + 10;
        if (digit_value >= base) {
            *status = -1;
            return 0;
        }
        result = (result * base) + digit_value;
    }
    return result;
}

int main(int argc, char* argv[]) {
    for (int i=0; i < 16; i++)
        printf("i=%d, 2^i=%ld\n", i, pow2(i));

    char* data[] = { "1", "10", "11", "100", "101", "110", "111", "000000", "11111", "1111111", "00000000", "20002" };

    char *hex_data[] = { "0", "10", "100", "101", "1000", "F", "FF", "A", "AA" };

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
}
