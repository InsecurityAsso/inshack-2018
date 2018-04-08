//~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
//    file: cipher.c
//    date: 2017-09-05
//  author: paul.dautry
// purpose:
//      G-Corp Stage 3 - Encrypted Storage
//      Encrypt & decrypt files using symmetric algorithm XTEA and CBC chaining 
//      mode. 
// license:
//      GPLv3
//~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
// INCLUDES
//==============================================================================
#include <sys/types.h>
#include <sys/stat.h>
#include <fcntl.h>
#include <unistd.h> 
#include <stdlib.h>
#include <stdio.h>
#include <stdint.h>
#include <string.h>
//==============================================================================
// CONFIG
//==============================================================================
#define XTEA_ROUNDS 32
//==============================================================================
// MACROS
//==============================================================================
#define PERR(error) printf(error "\n")
//==============================================================================
// TYPES
//==============================================================================
typedef unsigned char uchar;
typedef unsigned int uint;
//==============================================================================
// GLOBALS
//==============================================================================
static const uint32_t gdelta=0x9E3779B9;
//==============================================================================
// FUNCTIONS
//==============================================================================
//------------------------------------------------------------------------------
// xtea_encrypt
//     taken from https://en.wikipedia.org/wiki/XTEA
//------------------------------------------------------------------------------
void xtea_encrypt(uint rounds, uint32_t v[2], uint32_t const key[4]) 
{
    uint i;
    uint32_t v0=v[0], v1=v[1], sum=0;
    for (i=0; i<rounds; i++) {
        v0 += (((v1 << 4) ^ (v1 >> 5)) + v1) ^ (sum + key[sum & 3]);
        sum += gdelta;
        v1 += (((v0 << 4) ^ (v0 >> 5)) + v0) ^ (sum + key[(sum>>11) & 3]);
    }
    v[0]=v0; v[1]=v1;
}
#ifndef NO_DECRYPTION
//------------------------------------------------------------------------------
// xtea_decrypt
//     taken from https://en.wikipedia.org/wiki/XTEA
//------------------------------------------------------------------------------
void xtea_decrypt(uint rounds, uint32_t v[2], uint32_t const key[4]) 
{
    uint i;
    uint32_t v0=v[0], v1=v[1], sum=gdelta*rounds;
    for (i=0; i<rounds; i++) {
        v1 -= (((v0 << 4) ^ (v0 >> 5)) + v0) ^ (sum + key[(sum>>11) & 3]);
        sum -= gdelta;
        v0 -= (((v1 << 4) ^ (v1 >> 5)) + v1) ^ (sum + key[sum & 3]);
    }
    v[0]=v0; v[1]=v1;
}
#endif /* NO_DECRYPTION */
//------------------------------------------------------------------------------
// read_file_sz
//------------------------------------------------------------------------------
int read_file_sz(const char *fpath)
{
    struct stat s;
    if(stat(fpath, &s)<0) {
        PERR("failed to read file size!");
        return -1;
    }
    return s.st_size;
}
//------------------------------------------------------------------------------
// read_file
//------------------------------------------------------------------------------
int read_file(const char *fpath, uchar *buf, int qsz)
{
    ssize_t esz;
    int fd;
    if((fd=open(fpath, O_RDONLY))<0) {
        PERR("failed to open file for reading!");
        return -1;
    }   
    esz=read(fd, buf, qsz);
    close(fd);
    return esz;
}
//------------------------------------------------------------------------------
// write_file
//------------------------------------------------------------------------------
int write_file(const char *fpath, const uchar *buf, int qsz)
{
    ssize_t esz;
    int fd;
    if((fd=open(fpath, O_WRONLY|O_TRUNC))<0) {
        PERR("failed to open file for writting!");
        return -1;
    }
    esz=write(fd, buf, qsz);
    close(fd);
    return esz;
}
//------------------------------------------------------------------------------
// generate_iv
//------------------------------------------------------------------------------
int generate_iv(uchar iv[8])
{
    if(read_file("/dev/urandom", iv, 8)!=8) {
        PERR("failed to read 8 bytes from /dev/urandom!");
        return -1;
    }
    return 0;
}
//------------------------------------------------------------------------------
// xor
//     in-place XOR operation
//------------------------------------------------------------------------------
void xor(const uchar *m, uchar *d)
{
    int i;
    for(i=0; i<8; ++i) {
        d[i] ^= m[i];    
    }
}
//------------------------------------------------------------------------------
// cbc_encrypt
//------------------------------------------------------------------------------
int cbc_encrypt(const uchar *k, int ksz, uchar *d, int dsz, const char *fpath) 
{
    uchar p, *enc=NULL;
    int i, sz;
    if(ksz!=16) {
        PERR("key size must match 16!");
        return -1;
    }
    p=8-(dsz%8);
    sz=dsz+p;
    enc=(uchar*)calloc(8+sz, sizeof(uchar));
    if(generate_iv(enc)<0) {
        PERR("failed to generate IV!");
        free(enc);
        return -1;
    }
    memcpy(enc+8, d, dsz);
    memset(enc+8+dsz, p, p);
    /* iterate over 8-bytes blocks */
    for(i=0; i<sz/8; ++i) {
        xor(enc+i*8, enc+(i+1)*8);
        xtea_encrypt(XTEA_ROUNDS, (uint32_t*)enc+(i+1)*8, (uint32_t*)k);
    }
    /* overwrite file */
    if(write_file(fpath, enc, sz+8)!=(sz+8)) {
        PERR("failed to overwrite input file. Input file may be corrupted.");
        free(enc);
        return -1;   
    }
    free(enc);
    return 0;
}
#ifndef NO_DECRYPTION
//------------------------------------------------------------------------------
// cbc_decrypt
//------------------------------------------------------------------------------
int cbc_decrypt(const uchar *k, int ksz, uchar *d, int dsz, const char *fpath) 
{
    uchar p;
    int i;
    if(dsz%8!=0||ksz!=16) {
        PERR("data size must be a multiple of 8 & key size must match 16!");
        return -1;
    }
    /* iterate over 8-bytes blocks */
    for(i=(dsz/8)-1; i>0; --i) {
        xtea_decrypt(XTEA_ROUNDS, (uint32_t*)d+i*8, (uint32_t*)k);
        xor(d+(i-1)*8, d+i*8);
    }
    p=d[dsz-1];
    /* overwrite file */
    if(write_file(fpath, d+8, dsz-8-p)!=(dsz-8-p)) {
        PERR("failed to overwrite input file. Input file may be corrupted.");
        return -1;   
    }
    return 0;
}
#endif /* NO_DECRYPTION */
//------------------------------------------------------------------------------
// usage
//------------------------------------------------------------------------------
int usage(const char *prog)
{
    printf("usage: %s (e|d) <keyfile> <datafile>\n", prog);
}
//------------------------------------------------------------------------------
// MAIN / ENTRY POINT
//------------------------------------------------------------------------------
int main(int argc, char **argv)
{
    int ksz, dsz;
    uchar *k=NULL, *d=NULL;
    if(argc!=4) {
        usage(argv[0]);
        PERR("expecting 4 arguments!");
        goto fail;
    }
    /* load key */
    if((ksz=read_file_sz(argv[2]))<0) {
        PERR("failed to read key file size!");
        goto fail;
    }
    k=(uchar*)calloc(ksz, sizeof(uchar));
    if(read_file(argv[2], k, ksz)!=ksz) {
        PERR("failed to read key file!");
        goto fail;
    }
    /* load data */
    if((dsz=read_file_sz(argv[3]))<0) {
        PERR("failed to read data file size!"); 
        goto fail;
    }
    d=(uchar*)calloc(dsz, sizeof(uchar));
    if(read_file(argv[3], d, dsz)!=dsz) {
        PERR("failed to read data file!");
        goto fail;
    }
    switch(argv[1][0]) {
        case 'e':
            printf("encrypting...\n");
            if(cbc_encrypt(k, ksz, d, dsz, argv[3])!=0) {
                PERR("encryption failed!");
                goto fail;
            }
            printf("encryption performed.\n");
            break;
        case 'd':
#ifndef NO_DECRYPTION
            printf("decrypting...\n");
            if(cbc_decrypt(k, ksz, d, dsz, argv[3])!=0) {
                PERR("decryption failed!");
                goto fail;
            }
            printf("decryption performed.\n");
#else
            PERR("decryption not implemented... sorry not sorry.");
            goto fail;
#endif /* NO_DECRYPTION */
            break;
        default:
            usage(argv[0]);
            PERR("expecting 'e' or 'd'!");
            goto fail;
    }
    free(k);
    free(d);
    exit(0);
fail:
    free(k);
    free(d);
    exit(1);
}
