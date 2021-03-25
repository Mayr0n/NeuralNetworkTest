import random

from errors import SizeError


class Matrix:
    def __init__(self, size=(1, 1), alea=False, set_column=False, fill=None):
        # size est un tuple (x,y) ; x = nombre de lignes, y = nombre de colonnes, remplissage = liste de listes
        if fill is not None:
            self.matrix = fill
        else:
            if set_column:
                self.matrix = [[0.0 if not alea and x != 0 else random.random() for x in range(size[1])] for y in
                               range(size[0])]
            else:
                self.matrix = [[0.0 if not alea else random.random() for x in range(size[1])] for y in range(size[0])]

    def get_len_columns(self):
        return len(self.matrix[0])

    @staticmethod
    def list_to_matrix(list):
        if type(list[0]) == tuple or type(list[0]) == list:
            return Matrix(fill=list)
        else:
            m = Matrix(size=(len(list), 1))
            for element in list:
                m.set_line(list.index(element), [element])
            return m

    @staticmethod
    def matrix_to_list(matrix):
        return matrix.get_column(0)

    def get_len_lines(self):
        return len(self.matrix)

    def get(self, location):
        # location = (x, y) où x = index ligne, y = index colonne
        return self.matrix[location[0]][location[1]]

    def set(self, location, value):
        # location = (x, y) où x = index ligne, y = index colonne
        self.matrix[location[0]][location[1]] = value
        return self.matrix

    def set_line(self, index, values):
        self.matrix[index] = values
        return self.matrix

    def set_column(self, index, values):
        lines = self.get_lines()
        for i in range(self.get_len_lines()):
            lines[i][index] = values[i]
        self.matrix = lines
        return self.matrix

    def get_column(self, index):
        column = []
        for line in self.matrix:
            column.append(line[index])
        return column

    def get_line(self, index):
        return self.matrix[index]

    def get_lines(self):
        return self.matrix

    def get_columns(self):
        columns = []
        for i in range(self.get_len_columns()):
            columns.append(self.get_column(i))
        return columns

    def complete_sum(self):
        sum = 0
        for j in range(self.get_len_lines()):
            sum += self.get((j, 0))
        return sum

    def __repr__(self):
        s = ""
        for l in range(len(self.matrix)):
            s += "["
            for c in range(len(self.matrix[l])):
                s += "{},".format(self.matrix[l][c])
            s = s[0:len(s) - 1]
            s += "]\n"
        s = s[0:len(s) - 1]
        s += "]\n"
        return s

    def sum(self, list):
        s = 0
        for i in list:
            s += i
        return s

    def __mul__(self, m2):  # m1 et m2 sont des Matrix
        if type(m2) == Matrix:
            if self.get_len_columns() == m2.get_len_lines():
                m3 = Matrix(size=(self.get_len_lines(), m2.get_len_columns()))
                for line in self.get_lines():
                    m3_line = []
                    for j in m2.get_columns():
                        m3_element_line = sum([line[e] * j[e] for e in range(m2.get_len_columns())])
                        m3_line.append(m3_element_line)
                    m3.set_line(self.get_lines().index(line), m3_line)
            elif self.get_len_columns() == m2.get_len_columns() and self.get_len_columns() == 1:
                m3 = Matrix(size=(self.get_len_lines(), 1))
                c1 = self.get_column(0)
                c2 = m2.get_column(0)
                m3.set_column(0, [c1[e] * c2[e] for e in range(m2.get_len_lines())])
                return m3
            else:
                raise SizeError("La taille des colonnes de la première matrice "
                                "ne correspond pas au nombre de lignes de la seconde !")
        else:
            m3 = Matrix(size=(self.get_len_lines(), self.get_len_columns()))
            for i in range(self.get_len_lines()):
                m3.set_line(i, [self.get_line(i)[j] + m2 for j in range(len(self.get_line(i)))])
        return m3

    def __add__(self, m2):
        m3 = Matrix(size=(self.get_len_lines(), self.get_len_columns()))
        for i in range(self.get_len_lines()):
            m3.set_line(i, [self.get_line(i)[j] + m2.get_line(i)[j] for j in range(len(self.get_line(i)))])
        return m3

    def __sub__(self, m2):
        m3 = Matrix(size=(self.get_len_lines(), self.get_len_columns()))
        for i in range(self.get_len_lines()):
            m3.set_line(i, [self.get_line(i)[j] - m2.get_line(i)[j] for j in range(len(self.get_line(i)))])
        return m3

    def __getitem__(self, item):
        return self.get([item, 0])

    def __len__(self):
        if self.get_len_lines() == 1:
            return len(self.get_columns())
        elif self.get_len_columns() == 1:
            return len(self.get_lines())
