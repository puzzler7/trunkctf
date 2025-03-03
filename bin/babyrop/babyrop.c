#include <stdio.h>
#include <stdlib.h>


int main() {
    char name[64];

    printf("What's your name? ");
    fgets(name, 128, stdin);
    printf("Nice to meet you, %s", name);
}

void flag() {
    setbuf(stdout, NULL);
    setbuf(stdin, NULL);
    
    char flag_buf[128];
    FILE* file = fopen("./flag.txt", "r");
    fscanf(file, "%s", flag_buf);
    printf("Well done! %s\n", flag_buf);
    exit(0);
}