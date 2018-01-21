#include <stdio.h>

char passwd_3309[] = {
    0x95, 0xB3, 0x15, 0x32, 0xe4, 0xe4, 0x43, 0x6b,
    0x90, 0xbe, 0x1b, 0x31, 0xa7, 0x8b, 0x2d, 0x05
};

int main() {
    char v8;
    char * i=0;
    for ( i = (char *)&passwd_3309; ; *(i - 1) ^= 5u )
    {
        i += 4;
        if ( i == &passwd_3309 + 4)
            break;
        v8 = *(i - 3);
        *(i - 4) ^= 0xA7u;
        *(i - 3) = v8 ^ 0x8B;
        *(i - 2) ^= 0x2Du;
    }
    printf("The key is: %s\n", passwd_3309);
    puts("In hex: ");
    for(int i=0; i < 16;i++) {
        printf("%02x", passwd_3309[i]%0xFF);
    }
    puts("");
}
