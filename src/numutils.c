#include "numutils.h"

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
        int digit_value = -1;
        if (*p >= '0' && *p <= '9')
            digit_value = *p - '0';
        else if (*p >= 'A' && *p <= 'Z')
            digit_value = *p - 'A' + 10;
        if (digit_value < 0 || digit_value >= base) {
            *status = -1;
            return 0;
        }
        result = (result * base) + digit_value;
    }
    return result;
}
