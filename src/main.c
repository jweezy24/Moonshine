#include "main.h"




int main(int argc, char *argv[]){
    //Parse command-line arguments
    cmd* vals = parse_commandline(argc, argv);
    int count = vals->bl;
    int bl = vals->bl;
    int sl = vals->sl;
    int discard = vals->discard;
    int total_before_mapping = pow_jack(2,bl);
    int total_after_mapping = pow_jack(2,sl);

    //Initalizing locals based on the command line arguments
    int j;
    int* list_ints_before = malloc(sizeof(int) * total_before_mapping);
    int* list_ints_after = malloc(sizeof(int) * total_after_mapping);
    int* judges_list = malloc(sizeof(int) * total_before_mapping);
    int* ordering_list_before =malloc(sizeof(int) * total_before_mapping);
    int* ordering_list_after =malloc(sizeof(int) * total_after_mapping);
    char *path = vals->filepath;
    char *outfile = vals->outfile; 
    //Locally caching the bit stream from a file
    char* bits = create_bits_arr(path);
    int total_bin_nums = strlen(bits);

    //initalizing arrays
    for(j = 0; j < total_before_mapping; j++){
        list_ints_before[j] = 0;
    }

    for(j = 0; j < total_after_mapping; j++){
        list_ints_after[j] = 0;
    }

    for(j = 0; j < total_before_mapping; j++){
        judges_list[j] = -1;
    }

    for(j = 0; j < total_before_mapping; j++){
        ordering_list_before[j] = -2;
    }

    for(j = 0; j < total_after_mapping; j++){
        ordering_list_after[j] = 0;
    }

   // First thing we do is discard bits in the given stream
    apply_discard(bits, total_bin_nums, bl, discard);
    
    // We then formulate the histogram of all the found values after we have discarded the bits
    form_histogram(bits, total_bin_nums, bl, list_ints_before, ordering_list_before, total_before_mapping);

    //We then drop the highest half of the bits
    drop_highest_half(list_ints_before, total_before_mapping, total_after_mapping);
    
    // We formulate the new mappings based on the ording and remaing values
    new_mapping(list_ints_before, total_before_mapping, ordering_list_before, ordering_list_after, judges_list);

    // We then apply the new mappings we determined prior and generate a new output file. 
    translate_new_mappings(judges_list, total_after_mapping, sl, bits, total_bin_nums, outfile);
}

/*
Self made power function to avoid importing math.h
input:
    a = the base number we want to raise to a power
    b = The exponent of the number a
output:
    a^b as a integer
*/
long pow_jack(int a, int b){
    long tmp_num = 1;
    if (b == 0){
        return 1;
    }
    for(int i = 0; i < b; i++){
        
        tmp_num = tmp_num*a;
    }
    return tmp_num;
}

/*
Method to apply the discard from the command line
input:
    bits = the array of bits as a array of chars
    len = the length of the bits array
    bin_len = the amount of bits we want to use to define a number i.e. if bin_len = 8 then we convert 8 bits into a integer.
    discard = The amount of bits we want to discard

*/
void apply_discard(char* bits, int len, int bin_len, int discard){
    int count = 0;
    if (discard == 0){
        return;
    }
    int just_discarded = 0;
    for (int i =0; i < len;){
        if(i%bin_len == 0 && i > 0 && just_discarded == 0){
            for(int j = 0; j < discard; j++){
                bits[i+j] = -1;
            }
            i+=discard;
            just_discarded = 1;
            continue;
        }
        just_discarded = 0;
        i+=1;

    }
}

/*
Debugging function to print a bit stream bit for bit.
*/
void print_stream(char* bits, int len){
    for(int i =0; i < len; i++){
        printf("%c", bits[i]);
    }
    printf("\n");
}

/*
This method will create a histogram of the occurances of bit sequences.
input:
    bits = given bit stream where each bit is a char
    len = len of the bits array
    bin_len = how many bits used to define a number
    histo_before = This is the histogram of all of the numbers before applying moonshine
    ordering_list = A list that remebers the order of the numbers when they first occur
    histo_len = the length of the histogram list. 
*/
void form_histogram(char* bits, int len, int bin_len, int* histo_before, int* ordering_list, int histo_len){
    char* bin_num = malloc(bin_len+1);
    int count = 0;
    int index = 0;
    for(int i = 0; i < len; i++){
        if(count%bin_len == 0 && i > 0){
            bin_num[count] = 0;
            int num = bin_to_int(bin_num);
            if(histo_before[num] == 0){
                ordering_list[index] = num;
                index+=1;
            }

            histo_before[num] += 1;

            if(bits[i]!= -1){
                count = 1;
                bin_num[0] = bits[i];
            }else{
                count = 0;
            }

        }else{
            if(bits[i] != -1){
                bin_num[count] = bits[i];
                count+=1;
            }
        }
    }
    free(bin_num);
}


/*
This method will drop the highest half of values from the histogram
input:
    histo_before = the hisgram of numbers before applying moonshine
    len1 = length of the histo_before
    len2 = How many sequences we want to drop.
*/
void drop_highest_half(int* histo_before, int len1, int len2){
    int max = 0;
    int index = 0;
    for(int i =0; i < len2; i++){
        max = 0;
        for(int j =0; j < len1; j++){
            if(histo_before[j] > max){
                max = histo_before[j];
                index = j;
            }
        }
        histo_before[index] = -1;
        index = 0;
    }

}

/*
This method applies a new mapping using the old data.
input:
    histo_before = the hisgram of numbers before applying moonshine
    len1 = lenght of histo_before
    ordering_list_before = the order in which the binary sequence originally appeared relative to each number
    ordering_list_after = The new ordering of the remaining half, in other words, the new mapping.
    judges_list = a list containing the mapping locations
*/
void new_mapping(int* histo_before, int len1, int* ordering_list_before, int* ordering_list_after, int* judges_list){
    int index = 0;
    int location = 0;

    for(int i = 0; i < len1; i++){
        index = ordering_list_before[i];

        if(histo_before[index] != -1){
            ordering_list_after[location] = index;
            judges_list[index] = (location+i)%((int)(len1/2));
            location+=1;
        }
    }

}

/*
This method will apply the mapping generated from the method above and write the results to a new file.
input:
    judges_list = a list containing the mapping locations
    len = new length after the mapping
    sl = the new binary power
    bits = the orginal list of bits we started with
    len2 = the total amount of bits
    path = file path where the user wishes to save their results.
*/
void translate_new_mappings(int* judges_list, int len, int sl, char* bits, int len2, char* path){
    char* bin_num = malloc(sl+1);
    int count = 0;
    for(int i = 0; i < len2; i++){
        if(count%(sl+1) == 0 && i > 0){
            bin_num[count] = 0;
            int num = bin_to_int(bin_num);
            
            
            int ind = judges_list[num];
            if(ind != -1){
                char* new_num = int_to_bin(ind,sl);
                write_to_file(new_num, path);
                free(new_num);
            }
                
            

            if(bits[i]!= -1){
                count = 1;
                bin_num[0] = bits[i];
            }else{
                count = 0;
            }

        }else{
            if(bits[i] != -1){
                bin_num[count] = bits[i];
                count+=1;
            }
        }
    }
    free(bin_num);

}

/*
This will translate a binary string to a integer.
input:
    bin = string of a binary number
output:
    integer representation of the binary string.
*/

long bin_to_int(char* bin){
    long ret = 0;
    int len = strlen(bin);
    for(int i = 0; i < len; i++){
        if(bin[i] == '1'){
            ret += pow_jack(2,(len-1)-i);
        }
    }

    return ret;
}

/*
This will translate a integer to a binary string.
input:
    bin = number we want to translate to binary
    size = the amount of bits we would like to use to represent the number
output:
    string representation in binary format of the given number.
*/
char* int_to_bin(int bin, int size){
    char* ret = malloc(size+1);

    int count = 0;
    for(int i = size-1; i >= 0; i--){
        if(bin >= pow_jack(2,i)){
            ret[count] = '1';
            bin -= pow_jack(2,i);
        }else{
            ret[count] = '0';
        }
        count+=1;
    }
    ret[size] = 0;

    return ret;

}
/*
This method will take a string argument where the number is base 10 and convert the string to a integer.
input:
    number = string number in base 10
output:
    integer representation of the given string number
*/
int str_to_int(char* number){
    int count = 0;
    int ret = 0;

    printf("NUMBER = %s\n", number);

    while(number[count] != 0){
        count+=1;    
    }

    int* holder = malloc((count+1) * sizeof(int));

    for(int i =0; i < count; i++){
        holder[i] = number[i]- '0';
    }


    for (int i =0; i < count; i++){
        ret += pow_jack(10, (count)-(i+1)) * holder[i];
       
    }
    

    return ret;

}

/*
This method will parse command-line arguments
input:
    argc = the total amount of command line arguments 
    argv = The actual command-line values
output:
    A arguments structure with the parsed data
*/

cmd* parse_commandline(int argc, char** argv){

    cmd* ret = malloc(sizeof(cmd));

    if( argc > 6 ) {
        printf("Too many arguments supplied.\n");
        exit(0);
    }
    else if (argc < 6){
        printf("Five arguments expected.\n");
        exit(0);
    }

    ret->bl = (int) (str_to_int(argv[1]));
    ret->sl = (int) (str_to_int(argv[2]));
    ret->discard = (int) (str_to_int(argv[3]));

    ret->filepath = malloc(strlen(argv[4])+1);

    for(int i = 0; i < strlen(argv[4]); i++){
        ret->filepath[i] = argv[4][i];
    }
    
    ret->outfile = malloc(strlen(argv[5])+1);

    for(int i = 0; i < strlen(argv[5]); i++){
        ret->outfile[i] = argv[5][i];
    }


    printf("filepath = %s\n", ret->filepath);
    printf("outfile = %s\n", ret->outfile);
    return ret;

}
/*
This method will take a ascii binary file and create a list of bits out of that file
input:
    filepath = path of the file given
output:
    an array of bits gathered from that file
*/
char* create_bits_arr(char* filepath){
    FILE* fpw = fopen(filepath, "r");
    char* bits = malloc(256);
    int count = 0;
    int iter = 1;
    char c = 0;
    while((c = fgetc(fpw)) != EOF){
        if(count%256 ==0 && count > 0){
            iter+=1;
            bits = realloc(bits, 256*iter);
            if(bits == NULL){
                printf("Bad pointer\n");
                exit(0);
            }
        }
        bits[count] = c;
        count+=1;
    }
    return bits;

}
/*
Write a character string to a file
input:
    bin = binary number as a char array
    path = filepath of the file we would like to write to.
*/
void write_to_file(char* bin, char* path){

    FILE* fp = fopen(path, "a");
    fputs(bin, fp);
    fclose(fp);

}