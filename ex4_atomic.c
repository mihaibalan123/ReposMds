#include <stdio.h>
#include <pthread.h>

_Atomic int counter = 0;

void* add(void* arg) {
    for (int i = 0; i < 100000; i++) counter++;
    return NULL;
}

int main() {
    pthread_t t1, t2;
    pthread_create(&t1, NULL, add, NULL);
    pthread_create(&t2, NULL, add, NULL);
    pthread_join(t1, NULL);
    pthread_join(t2, NULL);
    printf("Ex 4: %d\n", counter);
    return 0;
}
