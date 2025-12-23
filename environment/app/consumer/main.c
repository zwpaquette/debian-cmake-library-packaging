#include <stdio.h>
#include <calc.h>

int main() {
    int a = 10;
    int b = 5;
    
    printf("Using libcalc:\n");
    printf("%d + %d = %d\n", a, b, add(a, b));
    printf("%d * %d = %d\n", a, b, multiply(a, b));
    printf("Library verification successful!\n");
    
    return 0;
}
