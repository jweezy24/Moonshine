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
