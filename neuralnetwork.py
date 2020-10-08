import neuron as ne
import errors as err


class NeuralNetwork:
    def __init__(self, sizes, entriesSize):  # sizes = [2, 1]
        self.structure = list()
        if len(sizes) <= 0:
            raise err.SizeError()
        for i in range(len(sizes)):  # pour chaque colonne
            column = list()
            for s in range(sizes[i]):  # sizes = [2, 1]
                if sizes[i] <= 0:
                    raise err.SizeError()
                column.append(ne.Neuron(entriesSize))
            self.structure.append(column)

    def getResult(self, entries):
        print(str(entries))
        results = list()
        for i in range(len(self.structure)):  # pour chaque colonne
            print("Colonne {}".format(i))
            local_results = list()  # résultats donnés par les neurones de la colonne
            for neuron in self.structure[i]:  # pour chaque neuronne de la colonne
                print("Neurone colonne {}, poids : {}".format(i, neuron.weights))
                # si première colonne -> utilise les entrées du système neuronal
                # sinon utilise les résultats de la colonne précédente
                local_results.append(neuron.get(entries) if i == 0 else neuron.get(results[i - 1]))
            print(str("Résultats locaux : {}".format(local_results)))
            results.append(local_results)
        print(str(results))
        return results[len(results) - 1]

    def getNumberOfColumns(self):
        return len(self.structure)

    def getNumberOfNeurons(self):
        nb = 0
        for column in self.structure:
            nb += 1
        return nb

    def getNumberOfNeuronsOfColumn(self, index):
        return len(self.structure[index])

    def getNeuron(self, column, row):
        return self.structure[column][row]
