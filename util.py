
import numpy as np
import matplotlib.pyplot as plt
import time

BLANC = 0
NOIR = 1
INDETERMINE = -1

def readFile(filename):
    """Lis un fichier et retourne la grille et ses contraintes sous la forme d'un triple
    """
    f = open ( filename, "r" )
    M = f.readlines()
    ROWS_CONSTRAINTS = list() #Liste des contraintes de lignes
    COLUMNS_CONSTRAINTS = list() # Liste des contraintes de colonnes
    ligne = 0
    while M[ligne][0] != '#':
        L = M[ligne].split(' ')
        if M[ligne] == '\n':
            L = list()
        else:
            L = [int(n) for n in L] #Conversion et suprression des '\n'
        ROWS_CONSTRAINTS.append(L)
        ligne += 1

    ligne += 1
    while ligne < len(M):
        L = M[ligne].split(' ')
        if M[ligne] == '\n':
            L = list()
        else:
            L = [int(n) for n in L] #Conversion et suprression des '\n'
        COLUMNS_CONSTRAINTS.append(L)
        ligne += 1


    return ROWS_CONSTRAINTS, COLUMNS_CONSTRAINTS, np.ones((len(ROWS_CONSTRAINTS), len(COLUMNS_CONSTRAINTS)))*(INDETERMINE)

