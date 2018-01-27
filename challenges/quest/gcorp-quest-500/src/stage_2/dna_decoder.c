//~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
//    file: dna_decoder.c
//    date: 2017-09-06
//  author: paul.dautry
// purpose:
//      G-Corp Stage 2 - DNA Encoding API
//      Using this vulnerable API user is supposed to be able to take full
//      control over the machine through arbitrary command execution
//      allowed by a .BSS overflow vulnerability.
//
//      A as 00, C as 01, G as 10, and T as 11 taken from
//
//              Computer Security, Privacy, and DNA Sequencing:
//    Compromising Computers with Synthesized DNA, Privacy Leaks, and More
//      Peter Ney, Karl Koscher, Lee Organick, Luis Ceze, Tadayoshi Kohno
//                          University of Washington
//          {neyp,supersat,leeorg,luisceze,yoshi}@cs.washington.edu
// license:
//      GPLv3
//~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
//==============================================================================
// INCLUDES
//==============================================================================
#include <unistd.h>
#include <stdlib.h>
#include <string.h>
#include <stdio.h>
//==============================================================================
// CONFIGURATION
//==============================================================================
#define BYTE_SZ     4
#define MAX_CMD     64
#define MAX_ODAT    128
#define MAX_IDAT    8*MAX_ODAT /* it should be 4*MAX_ODAT for safe buffer use */
//==============================================================================
// MACROS
//==============================================================================
#define ABRT(action)                                                           \
    {                                                                          \
        action                                                                 \
        exit(1);                                                               \
    }
//==============================================================================
// TYPES
//==============================================================================
typedef unsigned char uchar;
//==============================================================================
// GLOBALS
//==============================================================================
static uchar godat[MAX_ODAT];
static char gcmd[MAX_CMD];
static uchar gidat[MAX_IDAT];
//==============================================================================
// FUNCTIONS
//==============================================================================
//------------------------------------------------------------------------------
// d2b
//------------------------------------------------------------------------------
int d2b(const char dna[BYTE_SZ], uchar *o)
{
    int i;
    uchar lo=0x00;
    for(i=0; i<BYTE_SZ; i++) {
        switch(dna[i]) {
            case 'A': break;
            case 'C': lo|=1<<(2*(BYTE_SZ-1-i)); break;
            case 'G': lo|=2<<(2*(BYTE_SZ-1-i)); break;
            case 'T': lo|=3<<(2*(BYTE_SZ-1-i)); break;
            default:
                printf("unknown: %c\n", dna[i]);
                return -1;
        }
    }
    (*o)=lo;
    return 0;
}
//------------------------------------------------------------------------------
// dna_to_bin
//------------------------------------------------------------------------------
int dna_to_bin(int sz)
{
    int i;
    if(sz%BYTE_SZ!=0) {
        printf("DNA data size should be a multiple of 4!\n");
        return -1;
    }
    for(i=0; i<sz/BYTE_SZ; ++i) {
        if(d2b(gidat+i*BYTE_SZ, godat+i)!=0) {
            printf("DNA data contains a unknown character!\n");
            return -1;
        }
    }
    return sz/BYTE_SZ;
}
//==============================================================================
// MAIN / ENTRY POINT
//==============================================================================
//------------------------------------------------------------------------------
// main
//------------------------------------------------------------------------------
int main(int argc, char **argv)
{
    int isz, osz;
    memset(gcmd, 0, MAX_CMD);
    strcat(gcmd, "echo $(date) > /tmp/dna.log");
    /* read input data */
    isz=read(STDIN_FILENO, gidat, MAX_IDAT);
    if(gidat[isz-1]=='\n') {
        isz--;
    }
    /* convert input data */
    if((osz=dna_to_bin(isz))<0) {
        printf("failed to convert DNA to binary!\n");
        exit(1);
    }
#ifdef DEBUG
    printf("\ncmd: %s\n", gcmd);
#endif
    /* update log */
    system(gcmd); /* VULN here */
    /* write output data */
    write(STDOUT_FILENO, godat, osz);
    exit(0);
}
