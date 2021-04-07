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

#include <stdio.h>

#include <string.h>
#include <stdlib.h>
//#include "simulated_input.h"


typedef struct dict{
    char* string;
    int iter;
}dict;


typedef struct cmd_args{
    char* filepath;
    char* outfile;
    int bl;
    int sl;
    int discard;
}cmd;

void find_highest_half(int total_after_mapping, int total_before_mapping,  dict* all_numbers);

int str_to_int(char* number);

long pow_jack(int a, int b);

cmd* parse_commandline(int argc, char** argv);

char* create_bits_arr(char* filepath);

long bin_to_int(char* bin);

void apply_discard(char* bits, int len, int bin_len, int discard);

void print_stream(char* bits, int len);

void form_histogram(char* bits, int len, int bin_len, int* histo_before, int* ordering_list, int histo_len);

void drop_highest_half(int* histo_before, int len1, int len2);

void new_mapping(int* histo_before, int len1, int* ordering_list_before, int* ordering_list_after, int* judges_list);

char* int_to_bin(int bin, int size);

void write_to_file(char* bin, char* path);

void translate_new_mappings(int* ordering_list, int len, int sl, char* bits, int len2, char* path);