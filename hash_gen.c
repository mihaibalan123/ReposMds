#define OPENSSL_SUPPRESS_DEPRECATED
#include <stdio.h>
#include <stdlib.h>
#include <pthread.h>
#include <openssl/sha.h>

#define ITERS 2000000

char** file_list;
int file_count;
_Atomic int current_file = 0;

unsigned long stretch_hash(const char* path) {
    FILE* f = fopen(path, "r");
    if(!f) return 0;
    fseek(f, 0, SEEK_END);
    long sz = ftell(f);
    fseek(f, 0, SEEK_SET);
    unsigned char* buf = malloc(sz);
    fread(buf, 1, sz, f);
    fclose(f);

    unsigned char digest[32];
    SHA256_CTX ctx;
    SHA256_Init(&ctx);
    SHA256_Update(&ctx, buf, sz);
    SHA256_Final(digest, &ctx);
    free(buf);

    for (int i = 0; i < ITERS; i++) {
        SHA256_Init(&ctx);
        SHA256_Update(&ctx, digest, 32);
        SHA256_Final(digest, &ctx);
    }

    unsigned long sum = 0;
    for (int i = 0; i < 32; i++) sum += digest[i];
    return sum;
}

void* worker(void* arg) {
    while (1) {
        int idx = current_file++; 
        if (idx >= file_count) break;
        unsigned long res = stretch_hash(file_list[idx]);
        printf("Hash pentru %s: %lu\n", file_list[idx], res);
    }
    return NULL;
}

int main(int argc, char** argv) {
    if (argc < 3) {
        printf("Utilizare: %s <nr_threads> <fisier1> <fisier2> ...\n", argv[0]);
        return 1;
    }
    
    int num_threads = atoi(argv[1]);
    file_list = &argv[2];
    file_count = argc - 2;

    pthread_t* threads = malloc(num_threads * sizeof(pthread_t));
    for (int i = 0; i < num_threads; i++) pthread_create(&threads[i], NULL, worker, NULL);
    for (int i = 0; i < num_threads; i++) pthread_join(threads[i], NULL);
    
    free(threads);
    return 0;
}
