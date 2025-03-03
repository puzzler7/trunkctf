#include <stdio.h>
#include <stdlib.h>

char buffer[64];

int main() {
    printf("Enter flag: ");
    scanf("%64s", buffer);
    if (!strcmp(buffer, "tctf{string_cheese_is_tasty_but_not_very_secure_9d67c343}")) {
        printf("Correct!\n");
    } else {
        printf("Nope...\n");
    }
}