import neuron as ne
import errors as err
import cmath as math


class NeuralNetwork:
    def __init__(self, sizes, entriesSize):  # sizes = [2, 1]
        self.learning_rate = 0.5
        self.structure = list()
        if len(sizes) <= 0:
            raise err.SizeError()
        for i in range(len(sizes)):  # pour chaque colonne
            column = list()
            for s in range(sizes[i]):  # sizes = [2, 1]
                if sizes[i] <= 0:
                    raise err.SizeError()
                if i == 0:
                    column.append(ne.Neuron(entriesSize))
                else:
                    column.append(ne.Neuron(len(self.structure[i - 1])))
            self.structure.append(column)

    def getResults(self, entries):
        results = list()

        for i in range(len(self.structure)):  # pour chaque colonne
            local_results = list()  # résultats donnés par les neurones de la colonne
            for neuron in self.structure[i]:  # pour chaque neuronne de la colonne
                # si première colonne -> utilise les entrées du système neuronal
                # sinon utilise les résultats de la colonne précédente
                local_results.append(neuron.get(entries) if i == 0 else neuron.get(results[i - 1]))
            results.append(local_results)
        return results

    def getFinalResult(self, entries):
        return self.getResults(entries)[len(self.getResults(entries)) - 1][0]

    def getNumberOfColumns(self):
        return len(self.structure)

    def getNumberOfNeurons(self):
        nb = 0
        for column in self.structure:
            for n in column:
                nb += 1
        return nb

    def getNumberOfNeuronsOfColumn(self, index):
        return len(self.structure[index])

    def getNeuron(self, column, row):
        return self.structure[column][row]

    def getColumn(self, column):
        return self.structure[column]

    def getColumns(self):
        return self.structure

    def learn(self, entries, result_expected):
        result = self.getFinalResult(entries)
        results = self.getResults(entries)
        df = lambda x: (math.exp(-x) / (1 + 2 * math.exp(-x) + math.exp(-2 * x))).real  # dérivée

        actual_columns = self.structure

        self.structure.reverse()

        total_errors = []  # liste de listes : une erreur = un neurone

        for c in range(self.getNumberOfColumns()):
            column = self.getColumn(c)
            column_errors = []
            for n in range(len(column)):
                neuron = self.getNeuron(c, n)
                if c == 0:
                    error = df(neuron.getSomme(results[self.getNumberOfColumns() - 1]))*(result - result_expected)
                    column_errors.append(error)
                elif c == self.getNumberOfColumns() - 1:
                    error = df(neuron.getSomme(entries)) * neuron.getSomme(total_errors[c - 1])
                    column_errors.append(error)
                else:
                    error = df(neuron.getSomme(results[self.getNumberOfColumns() - 1])) * neuron.getSomme(total_errors[c - 1])
                    column_errors.append(error)
            total_errors.append(column_errors)

        for c in range(self.getNumberOfColumns()):
            column = self.getColumn(c)
            for n in range(len(column)):
                neuron = self.getNeuron(c, n)
                for w in range(len(neuron.weights)):
                    if c == self.getNumberOfColumns() - 1:
                        try:
                            neuron.setWeight(w, neuron.getWeight(w) - self.learning_rate * total_errors[c][n] * entries[w])
                        except IndexError:
                            print("len total_err = {}, len total_err_c = {}, len res_1_c = {}".format(len(total_errors),
                                                                                                      len(total_errors[
                                                                                                              c]), len(
                                    results[len(results) - 1 - c])))
                            print("w = {}, c = {}, n = {}, len = {}, len - c = {}".format(w, c, n, len(results),
                                                                                          len(results) - 1 - c))
                    else:
                        try:
                            neuron.setWeight(w, neuron.getWeight(w) - self.learning_rate * total_errors[c][n] *
                                             results[len(results) - 1 - c][w])
                        except IndexError:
                            print("len total_err = {}, len total_err_c = {}, len res_1_c = {}".format(len(total_errors),
                                                                                                      len(total_errors[
                                                                                                              c]), len(
                                    results[len(results) - 1 - c])))
                            print("w = {}, c = {}, n = {}, len = {}, len - c = {}".format(w, c, n, len(results),
                                                                                          len(results) - 1 - c))

        total_errors.reverse()
        self.structure.reverse()

        return total_errors
