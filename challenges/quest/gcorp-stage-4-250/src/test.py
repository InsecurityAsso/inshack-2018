#!/usr/bin/env python3
# -!- encoding:utf8 -!-
EO_SZ=4
EO_FACE_SZ=EO_SZ*EO_SZ

def print_faces():
    print('face F:')
    for i in range(0, EO_FACE_SZ): 
        for j in range(0, EO_SZ): 
            print('f%02d += u%02d' % (i, i+j*EO_FACE_SZ))
    print('face S:')
    for i in range(0, EO_FACE_SZ): 
        for j in range(0, EO_SZ):
            print('s%02d += u%02d' % (i, j+(i%EO_SZ)*EO_FACE_SZ+(i//EO_SZ)*EO_SZ))
    print('face T:')
    for i in range(0, EO_FACE_SZ):
        for j in range(0, EO_SZ):
            print('t%02d += u%02d' % (i, i+j*EO_SZ+(i//EO_SZ)*(EO_FACE_SZ-EO_SZ)))

def print_vectors():
    print('FT vector:')
    for i in range(0, EO_SZ):
        for j in range(0, EO_SZ):
            idxFT = i + j * EO_SZ
            idxFS = i * EO_SZ + j
            print('ft%02d += f%02d + t%02d' % (i, idxFT, idxFT))
    print('FS vector:')
    for i in range(0, EO_SZ):
        for j in range(0, EO_SZ):
            idxFT = i + j * EO_SZ
            idxFS = i * EO_SZ + j
            print('fs%02d += f%02d + s%02d' % (i, idxFS, idxFS))
    print('TS vector:')
    for i in range(0, EO_SZ):
        for j in range(0, EO_SZ):
            idxFT = i + j * EO_SZ
            idxFS = i * EO_SZ + j
            print('ts%02d += t%02d + s%02d' % (i, idxFT, idxFS))

def main():
    print_faces()
    print_vectors()

main()
