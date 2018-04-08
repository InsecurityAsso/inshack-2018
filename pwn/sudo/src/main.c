#include <stdio.h>
#include <unistd.h>
#include <stdlib.h>
#include <string.h>
#include <openssl/sha.h>
#include <sys/time.h>
#include <sys/resource.h>


void sha256_hash_string (unsigned char hash[SHA256_DIGEST_LENGTH], char outputBuffer[65])
{
    int i = 0;

    for(i = 0; i < SHA256_DIGEST_LENGTH; i++)
    {
        sprintf(outputBuffer + (i * 2), "%02x", hash[i]);
    }

    outputBuffer[64] = 0;
}

int calc_sha256 (char* path, char output[65])
{
    FILE* file = fopen(path, "rb");
    if(!file) return -1;

    unsigned char hash[SHA256_DIGEST_LENGTH];
    SHA256_CTX sha256;
    SHA256_Init(&sha256);
    const int bufSize = 32768;
    char* buffer = malloc(bufSize);
    int bytesRead = 0;
    if(!buffer) return -1;
    while((bytesRead = fread(buffer, 1, bufSize, file)))
    {
        SHA256_Update(&sha256, buffer, bytesRead);
    }
    fclose(file);
    SHA256_Final(hash, &sha256);

    sha256_hash_string(hash, output);
    free(buffer);

    return 0;
}

int main (int argc, char *argv[]) {
    if (argc < 2) {
        printf("Expected one and only one argument: the path to the executable to execute.\n");
        printf("Ex: ./sudo /bin/ls .\n");
        return 1;
    }

    setgid(getegid());
    setuid(geteuid());
    setpriority(PRIO_PROCESS, 0, 15);

    char* arguments[argc];
    for (int i=0 ; i<argc-1 ; i++) {
        arguments[i] = argv[i+1];
    }
    arguments[argc-1] = NULL;

    char calc_hash[65];
    if (calc_sha256(arguments[0], calc_hash) != 0) {
        return 2;
    }

    char* allowed_sha256[] = {"fea4ce7047b56e5e03767eb6dae03676936e56160f5022374a3422fd0c06a8bc", "e5c897bf7d621d9c894588ef7192c0a01f17bab099fa68b124a45aaa7ec838a8"};
    int found = 0;
    for (int i=0 ; i<2 ; i++) {
        if (strcmp(allowed_sha256[i], calc_hash) == 0) {
            found = 1;
            break;
        }
    }
    if (found == 0) {
        return 3;
    }

    if (0 == fork()) {
        if (-1 == execve(arguments[0], arguments, NULL)) {
            return 4;
        }
    }

    return 0;
}
