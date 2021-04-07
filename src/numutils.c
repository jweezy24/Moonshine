/*
Copyright 2021 Jack West

Permission is hereby granted, free of charge, to any person obtaining a copy of
this software and associated documentation files (the "Software"), to deal in
the Software without restriction, including without limitation the rights to
use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies 
of the Software, and to permit persons to whom the Software is furnished to do
so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies
or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED,
INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A 
PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR 
COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
*/
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
