import neuron as ne
import errors as err
import cmath as math


class NeuralNetwork:
    def __init__(self, sizes, entriesSize):  # sizes = [2, 1]
        self.learning_rate = 10
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

    def learn(self, entries, result, showWeights):
        results = self.getResults(entries)  # list
        df = lambda x: math.exp(-x) / (1 + 2 * math.exp(-x) + math.exp(-2 * x))  # dérivée
        i = len(self.structure) - 1  # nombre de colonnes
        errors = list()

        while i >= 0:
            column = self.structure[i]
            if len(errors) == 0:  # si dernier neurone
                neuron = column[0]
                y = self.getFinalResult(entries)
                e = df(neuron.getSomme(results[i - 1])) * (y - result)
                e = e.real
                errors.append([e])
                for i3 in range(len(neuron.weights)):
                    neuron.weights[i3] -= (self.learning_rate * e * results[i3 - 1][i3]).real
                neuron.setBiasWeight(neuron.getBiasWeight() - self.learning_rate * e * neuron.bias_value)
            else:
                column_errors = list()
                previous_column = self.structure[i + 1]  # récupère la colonne d'après
                previous_errors = errors[i - 1]  # récupère la liste des erreurs de chaque neurone de la colonne d'après
                for n in range(len(column)):  # pour chaque neurone de la colonne
                    neuron = column[n]
                    weighted_errors = 0
                    previous_neuron = previous_column[0]
                    weighted_errors += previous_neuron.getWeight(n) * previous_errors[0]
                    for n2 in range(len(previous_column) - 1):  # pour chaque neurone de la colonne d'avant
                        previous_neuron = previous_column[n2]
                        weighted_errors += previous_neuron.getWeight(n)*previous_errors[n2]  # somme pondérée erreurs
                    e = df(neuron.getSomme(entries if i == 0 else results[i + 1])) * weighted_errors
                    e = e.real
                    column_errors.append(e)
                    for i2 in range(len(neuron.weights)):
                        delta = (self.learning_rate * e * results[i - 1][i]).real
                        neuron.setWeight(i2, neuron.getWeight(i2) - delta)
                    neuron.setBiasWeight(neuron.getBiasWeight() - self.learning_rate * e * neuron.bias_value)
                errors.append(column_errors)
            i -= 1

        return self.getResults(entries)
