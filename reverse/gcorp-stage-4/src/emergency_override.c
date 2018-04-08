//~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
//    file: emergency_override.c
//    date: 2017-08-30
//  author: paul.dautry
// purpose:
//      G-Corp Stage 4 - Emergency Override (running on 12042)
// license:
//      GPLv3
//
//
//      _____      _     _              _            _
//     / ____|    | |   (_)            | |          | |
//    | |    _   _| |__  _  ___    __ _| | __ _  ___| |__  _ __ __ _
//    | |   | | | | '_ \| |/ __|  / _` | |/ _` |/ _ \ '_ \| '__/ _` |
//    | |___| |_| | |_) | | (__  | (_| | | (_| |  __/ |_) | | | (_| |
//     \_____\__,_|_.__/|_|\___|  \__,_|_|\__, |\___|_.__/|_|  \__,_|
//                                         __/ |
//                                        |___/
//
//    info: partial illustration w/ EO_SZ = 3 below
//
//                                  T
//                                  |
//                                  v
//                             ___ ___ ___
//                            /18_/19_/20_/|
//                           /_9_/10_/11_/||
//                          /___/___/__ /|/|
//                         | 0 | 1 | 2 | /|| <--------- S
//                         |___|___|___|/|/|
//                         | 3 | 4 | 5 | /||
//                         |___|___|___|/|/
//                         | 6 | 7 | 8 | /
//                         |___|___|___|/
//
//                               ^
//                               |
//                               F
//
//
//~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
// INCLUDES
//------------------------------------------------------------------------------
#include <stdlib.h>
#include <unistd.h>
#include <stdio.h>
#include <string.h>
#include <errno.h>
//------------------------------------------------------------------------------
// CONFIGURATION
//------------------------------------------------------------------------------
#define EO_SZ           4
#define EO_KEY_SZ       EO_SZ*EO_SZ*EO_SZ
#define EO_FACE_SZ      EO_SZ*EO_SZ
#define EO_RESULT_SZ    3*EO_SZ
#define EO_RESULT \
{ \
    0x52,0xb4,0x7c,0xca, /* FT */ \
    0x54,0xb6,0xfa,0x48, /* FS */ \
    0x74,0x8e,0x4e,0xfc, /* TS */ \
}
//------------------------------------------------------------------------------
// MACROS
//------------------------------------------------------------------------------
#define ERASE(buf, sz) memset(buf, 0x00, sz)
//------------------------------------------------------------------------------
// TYPES
//------------------------------------------------------------------------------
typedef unsigned char uchar;
//------------------------------------------------------------------------------
// GLOBALS
//------------------------------------------------------------------------------
static const uchar gRESULT[EO_RESULT_SZ]=EO_RESULT; /* FT + FS + TS */
static uchar gCOMPUT[EO_RESULT_SZ]; /* FT + FS + TS */
static uchar gKEY[EO_KEY_SZ];
static uchar gF[EO_FACE_SZ];
static uchar gS[EO_FACE_SZ];
static uchar gT[EO_FACE_SZ];
//------------------------------------------------------------------------------
// FUNCTIONS
//------------------------------------------------------------------------------
void usage(const char *prog)
{
    printf("usage: %s (compute|check)\n", prog);
    exit(1);
}

void compute_F(void)
{
    int i, j;
    for(i=0; i<EO_FACE_SZ; i++) { /* iterate over face */
        for(j=0; j<EO_SZ; j++) { /* iteratre over layers */
            gF[i] += gKEY[i+j*EO_FACE_SZ];
        }
    }
}

void compute_S(void)
{
    int i, j;
    for(i=0; i<EO_FACE_SZ; i++) { /* iterate over face */
        for(j=0; j<EO_SZ; j++) { /* iteratre over layers */
            gS[i] += gKEY[j+(i%EO_SZ)*EO_FACE_SZ+(i/EO_SZ)*EO_SZ];
        }
    }
}

void compute_T(void)
{
    int i, j;
    for(i=0; i<EO_FACE_SZ; i++) { /* iterate over face */
        for(j=0; j<EO_SZ; j++) { /* iteratre over layers */
            gT[i] += gKEY[i+j*EO_SZ+(i/EO_SZ)*(EO_FACE_SZ-EO_SZ)];
        }
    }
}

void compute(void)
{
    int i, j, idxFT, idxFS;
    ERASE(gF, EO_FACE_SZ);
    ERASE(gS, EO_FACE_SZ);
    ERASE(gT, EO_FACE_SZ);
    ERASE(gCOMPUT, EO_RESULT_SZ);
    compute_F();
    compute_S();
    compute_T();
    for(i=0; i<EO_SZ; ++i) {
        for (j=0; j<EO_SZ; ++j){
            idxFT = i+j*EO_SZ;
            idxFS = i*EO_SZ+j;
  /* FT */  gCOMPUT[i] += gF[idxFT] + gT[idxFT];
  /* FS */  gCOMPUT[i+EO_SZ] += gF[idxFS] + gS[idxFS];
  /* TS */  gCOMPUT[i+2*EO_SZ] += gT[idxFS] + gS[idxFT];
        }
    }
}

void print_result(void)
{
    int i, j;
    printf(
"#define EO_RESULT \\\n"
"{ \\\n");
    for(i=0; i<3; i++){
        printf("    ");
        for(j=0; j<EO_SZ; j++){
            printf("0x%02x,", gCOMPUT[i*EO_SZ+j]);
        }
        switch(i) {
            case 0: printf(" /* FT */"); break;
            case 1: printf(" /* FS */"); break;
            case 2: printf(" /* TS */"); break;
        }
        printf(" \\\n");
    }
    printf("}\n");
}

void check_result(void)
{
    if(memcmp(gRESULT, gCOMPUT, EO_RESULT_SZ)==0) {
        printf("OK\n");
    } else {
        printf("KO\n");
    }
}
//------------------------------------------------------------------------------
// MAIN/ENTRY
//------------------------------------------------------------------------------
int main(int argc, char **argv)
{
    if(argc!=2) {
        usage(argv[0]);    
    }
    ssize_t sz;
    if((sz=read(STDIN_FILENO, gKEY, EO_KEY_SZ))<0) {
        perror("failed to read from stdin");
        exit(1);
    }
    if(sz!=EO_KEY_SZ) {
        printf("%s expects to read exactly %d bytes from stdin.\n", argv[0], EO_KEY_SZ);
        exit(1);
    }
    compute();
    if(!strcmp(argv[1], "compute")) {       
        print_result();
    } else if (!strcmp(argv[1], "check")) {
        check_result();
    } else {
        usage(argv[0]);
    }
    exit(0);
}
