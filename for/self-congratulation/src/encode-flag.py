#!/usr/bin/env python
from PIL import Image

class SequenceCreator:
    def __init__(self):
        self.flag = "xIU8t4Zs"

    def get_ascii(self):
        # recup l'ascii de chaque lettre et met tout dans liste
        return [ord(c) for c in self.flag]

    def get_bytes(self):
        # a partir de ça récupère la valeur en binaire
        raw_bytes = [bin(l) for l in self.get_ascii()]
        # puis retourne les 0 et 1 concaténés (7 bits par lettre)
        return ''.join([line[2:] for line in raw_bytes])

    def get_bools(self):
        bools = []
        for i in self.get_bytes():
            if (i == '1'):
                bools.append(True)
            elif (i == '0'):
                bools.append(False)
            else:
                print("jsuis fou")
        return bools

if __name__ == "__main__":
    seq = SequenceCreator()
    boolsFlag = seq.get_bools()

    imgBase = Image.open('brutSansFond.png')
    pixelsBase = imgBase.load()

    lengthFlag = len(boolsFlag)
    premierX = 218
    premierY = 110

    # on dessine une sorte de code barre / qr-code des bits
    # carré 5x5 pour dire 1, couleur non modifiée pour 2
    taille = 5
    seuil = 50
    currentX = premierX
    currentY = premierY
    for currentBool in boolsFlag:
        if currentBool:
            for i in range(currentX, currentX+taille):
                for j in range(currentY, currentY+taille):
                    pixelsBase[i,j] = (0,0,0)
        else:
            for i in range(currentX, currentX+taille):
                for j in range(currentY, currentY+taille):
                    pixelsBase[i,j] = (255,255,255)
        currentX += taille
        # après un certain seuil on descend faire une nouvelle ligne
        if currentX > premierX + seuil:
            currentX = premierX
            currentY += 5

#        for j in range(premierY,premierY+5):
#            if boolsFlag[compteur]:
#                pixelsBase[i,j] = (0,0,0,255)
#        compteur += 1

    imgBase.save('logo_inshack_2018.png')

