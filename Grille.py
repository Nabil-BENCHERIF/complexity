#from util import *

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


class Grille:
    def __init__(self, filename):
        self.filename = filename
        self.ROWS_CONSTRAINTS, self.COLUMNS_CONSTRAINTS, self.matrix = readFile(filename)

        self.N = len(self.ROWS_CONSTRAINTS)
        self.M = len(self.COLUMNS_CONSTRAINTS)

    def coloration(self):
        LignesAVoir = set([i for i in range(self.N)])
        ColonnesAvoir = set([j for j in range(self.M)])

        while len(LignesAVoir) != 0 or len(ColonnesAvoir) != 0:
            for i in LignesAVoir.copy():
                ok, colored_columns_set = self.coloreLig(i)

                if not ok:
                    return False, np.zeros((self.N, self.M))
                ColonnesAvoir = ColonnesAvoir | colored_columns_set
                LignesAVoir.remove(i)

            for j in ColonnesAvoir.copy():
                ok, colored_rows_set = self.coloreCol(j)
                if not ok:
                    return False, np.zeros((self.N, self.M))
                LignesAVoir = LignesAVoir | colored_rows_set
                ColonnesAvoir.remove(j)
        if self.completely_colored(): return True, self
        return "NeSaitPas", self

    def completely_colored(self):
        return not np.array(self.matrix == INDETERMINE).any()

    def ligne(self, i):
        return self.matrix[i, :]

    def sub_ligne(self, i, j):
        return self.ligne(i)[0: j+1]

    def colonne(self, j):
        return self.matrix[:, j]

    def sub_colonne(self, j, i):
        return self.colonne(j)[0: i+1]


    def row_constraints(self, i):
        return self.ROWS_CONSTRAINTS[i]

    def column_constraints(self, j):
        return self.COLUMNS_CONSTRAINTS[j]


    def t_row(self,i, j, l, row_value_dict):
        if (j, l) not in row_value_dict:
            b = False
            # Cas 1 : l = 0
            if l == 0:
                b = all(np.array(self.sub_ligne(i, j)) != NOIR)

            # Cas 2(a) : l >= 1 and j < s_l - 1
            elif l >= 1 and j < self.ROWS_CONSTRAINTS[i][l - 1] - 1:
                b = False

            # Cas 2(b) : l >= 1 and j = s_l - 1
            elif j == self.ROWS_CONSTRAINTS[i][l - 1] - 1:
                b = l == 1 and all(np.array(self.sub_ligne(i, j)) != BLANC)

            # Cas 2(c) : l >= 1 and j > s_l - 1
            elif self.matrix[i, j] == BLANC:
                b = self.t_row(i, j - 1, l, row_value_dict)

            elif self.matrix[i, j] == NOIR:
                b = self.t_row(i, j - self.ROWS_CONSTRAINTS[i][l - 1] - 1, l - 1, row_value_dict) and \
                               all(np.array(self.sub_ligne(i, j)[-self.ROWS_CONSTRAINTS[i][l - 1]:]) != BLANC) and \
                               self.sub_ligne(i, j)[-self.ROWS_CONSTRAINTS[i][l - 1] - 1] != NOIR

            elif self.matrix[i, j] == INDETERMINE:
                b = self.t_row(i, j - 1, l, row_value_dict) or (self.t_row(i, j - self.ROWS_CONSTRAINTS[i][l - 1] - 1, l - 1, row_value_dict) and
                                                                all(np.array(self.sub_ligne(i, j)[-self.ROWS_CONSTRAINTS[i][l - 1]:]) != BLANC) and \
                                                                self.sub_ligne(i, j)[-self.ROWS_CONSTRAINTS[i][l - 1] - 1] != NOIR)

            row_value_dict[(j, l)] = b
            return b

        return row_value_dict[(j, l)]


    def t_column(self,j, i, l, column_value_dict):
        if (i, l) not in column_value_dict:
            b = False
            # Cas 1 : l = 0
            if l == 0:
                b = all(np.array(self.sub_colonne(j, i)) != NOIR)

            # Cas 2(a) : l >= 1 and i < s_l - 1
            elif l >= 1 and i < self.COLUMNS_CONSTRAINTS[j][l - 1] - 1:
                b = False

            # Cas 2(b) : l >= 1 and i = s_l - 1
            elif i == self.COLUMNS_CONSTRAINTS[j][l - 1] - 1:
                b = l == 1 and all(np.array(self.sub_colonne(j, i)) != BLANC)

            # Cas 2(c) : l >= 1 and i > s_l - 1
            elif self.matrix[i, j] == BLANC:
                b = self.t_column(j, i - 1, l, column_value_dict)

            elif self.matrix[i, j] == NOIR:
                b = self.t_column(j, i - self.COLUMNS_CONSTRAINTS[j][l - 1] - 1, l - 1, column_value_dict) and \
                                  all(np.array(self.sub_colonne(j, i)[-self.COLUMNS_CONSTRAINTS[j][l - 1]:]) != BLANC) and \
                                  self.sub_colonne(j, i)[-self.COLUMNS_CONSTRAINTS[j][l - 1] - 1] != NOIR

            elif self.matrix[i, j] == INDETERMINE:
                b = self.t_column(j, i - 1, l, column_value_dict) or self.t_column(j, i - self.COLUMNS_CONSTRAINTS[j][l - 1] - 1, l - 1, column_value_dict) and \
                                                                            all(np.array(self.sub_colonne(j, i)[-self.COLUMNS_CONSTRAINTS[j][l - 1]:]) != BLANC) and \
                                                                            self.sub_colonne(j, i)[-self.COLUMNS_CONSTRAINTS[j][l - 1] - 1] != NOIR



            column_value_dict[(i, l)] = b
            return b
        return column_value_dict[(i, l)]

    def set_color(self, i, j, color):
        self.matrix[i, j] = color

    def coloreLig(self, i):
        row_i = self.ligne(i)

        colored_columns_set = set()
        for j in range(self.M):
            if row_i[j] == INDETERMINE:
                # Test coloriage en blanc
                row_i[j] = BLANC
                white = self.t_row(i, self.M - 1, len(self.ROWS_CONSTRAINTS[i]), dict())

                # Test coloriage en noir
                row_i[j] = NOIR
                black = self.t_row(i, self.M - 1, len(self.ROWS_CONSTRAINTS[i]), dict())

                if white and not black:
                    row_i[j] = BLANC
                    colored_columns_set.add(j)
                elif black and not white:
                    row_i[j] = NOIR
                    colored_columns_set.add(j)
                elif black and white:
                    row_i[j] = INDETERMINE
                else :
                    return False, set()
        return True, colored_columns_set

    def coloreCol(self, j): # implementation iterative
        column_j = self.colonne(j)

        colored_rows_set = set()
        for i in range(self.N):
            if column_j[i] == INDETERMINE:
                # Test coloriage en blanc
                column_j[i] = BLANC
                white = self.t_column(j, self.N - 1, len(self.COLUMNS_CONSTRAINTS[j]), dict())
                # Test coloriage en noir
                column_j[i] = NOIR
                black = self.t_column(j, self.N - 1, len(self.COLUMNS_CONSTRAINTS[j]), dict())
                if white and not black:
                    column_j[i] = BLANC
                    colored_rows_set.add(i)
                elif black and not white:
                    column_j[i] = NOIR
                    colored_rows_set.add(i)
                elif black and white:
                    column_j[i] = INDETERMINE
                else :
                    return False, set()
        return True, colored_rows_set

    @staticmethod
    def copy_grille(G):
        G_copy = Grille(G.filename)
        G_copy.matrix = G.matrix.copy()
        return G_copy

    @staticmethod
    def enumeration(G):
        ok, G_R = G.coloration()
        if type(ok) is bool:
            if not ok:
                return False,  np.zeros((G.N, G.M))
            return True, G.matrix

        return Grille.enum_rec(G_R, 0, BLANC) or Grille.enum_rec(G_R, 0, NOIR)

    @staticmethod
    def enum_rec(G, k, color):
        if k == G.N * G.M:
            return True, G

        i = k // G.M
        j = k % G.M

        ok, G_R = Grille.colorierEtPropager(G, i, j, color)
        if type(ok) is bool:
            if not ok:
                return False

            return True, G_R

        # colorierEtPropager return NeSaitPas
        k_ = k + 1
        while k_ < G.N * G.M and G_R.matrix[k_ // G_R.M, k_ % G_R.M] != INDETERMINE:
            k_ += 1

        return Grille.enum_rec(G_R, k_, BLANC) or Grille.enum_rec(G_R, k_, NOIR)


    @staticmethod
    def colorierEtPropager(G, i, j, color):
        G_copy = Grille.copy_grille(G)

        G_copy.set_color(i, j, color)
        LignesAVoir = {i}
        ColonnesAvoir = {j}

        while len(LignesAVoir) != 0 or len(ColonnesAvoir) != 0:
            for i_ in LignesAVoir.copy():
                ok, colored_columns_set = G_copy.coloreLig(i_)
                if not ok:
                    return False, np.zeros((G_copy.N, G_copy.M))
                ColonnesAvoir = ColonnesAvoir | colored_columns_set
                LignesAVoir.remove(i_)

            for j_ in ColonnesAvoir.copy():
                ok, colored_rows_set = G_copy.coloreCol(j_)
                if not ok:
                    return False, np.zeros((G_copy.N, G_copy.M))
                LignesAVoir = LignesAVoir | colored_rows_set
                ColonnesAvoir.remove(j_)

        if G_copy.completely_colored():
            return True, G_copy
        return "NeSaitPas", G_copy




if __name__ == "__main__":
    #L:list
    L=list()
    #for num_inst in range(1,11):
         #num_inst = 10
         #G = Grille("instances/{}.txt".format(num_inst))

         #debut = time.time()
         #know, R = G.coloration()
         #L.append(time.time()-debut)
         #print("R : {}\n".format(know), R)
         #plt.imshow(R.matrix, cmap='binary', interpolation='none')
         #plt.savefig("instances_resolues/{}.png".format(num_inst))
     #print(L)

    for num_inst in range(11,17):
        #num_inst = 16
        G = Grille("instances/{}.txt".format(num_inst))
        #debut=time.time()
        know, R = Grille.enumeration(G)
        #L.append(time.time()-debut)
        print("R : {}\n".format(know), R)
        plt.imshow(R.matrix, cmap='binary', interpolation='none')
        plt.savefig("instances_resolues/{}.png".format(num_inst))
    #print(L)
