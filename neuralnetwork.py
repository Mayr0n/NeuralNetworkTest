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

    def learn(self, entries, result, showWeights):
        results = self.getResults(entries)
        df = lambda x: math.exp(-x) / (1 + 2 * math.exp(-x) + math.exp(-2 * x))
        i = len(self.structure) - 1  # nombre de colonnes
        errors = list()

        while i >= 0:
            print(i)
            column = self.structure[i]
            if len(errors) == 0:
                neuron = column[0]
                y = self.getFinalResult(entries)
                e = df(neuron.getSomme(results[i - 1])) * (y - result)
                e = e.real
                errors.append([e])
                for i in range(len(neuron.weights)):
                    print("i = {}".format(i))
                    print("Résultats colonne : {}".format(str(results[i - 1])))
                    print("Résultats précis : {}".format(str(results[i - 1][i])))
                    neuron.weights[i] -= (self.learning_rate * e * results[i - 1][i]).real
                neuron.setBiasWeight(neuron.getBiasWeight() - self.learning_rate * e * neuron.bias_value)
            else:
                column_errors = list()
                for n in range(len(column)):  # pour chaque neurone de la colonne
                    neuron = column[n]
                    next_errors = errors[i - 1]  # récupère les erreurs de la colonne d'après, enregistrées avant dans le tableau
                    previous_column = self.structure[i - 1]  # récupère la colonne d'après (inversé dans le while)
                    weighted_errors = 0
                    for n2 in range(len(previous_column)):  # pour chaque neurone de la colonne d'après
                        weighted_errors += previous_column[n2].weights[n]*next_errors[n2]  # somme pondérée erreurs
                    e = df(neuron.getSomme(entries if i == 0 else results[i - 1])) * weighted_errors
                    e = e.real
                    column_errors.append(e)
                    for i in range(len(neuron.weights)):
                        neuron.weights[i] -= (self.learning_rate * e * results[i - 1][i]).real
                    neuron.setBiasWeight(neuron.getBiasWeight() - self.learning_rate * e * neuron.bias_value)
                errors.append(column_errors)
            i -= 1
        return self.getResults(entries)
