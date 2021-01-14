import random as r
import cmath as math


class Neuron:

    def __init__(self, entriesSize):
        self.weights = [r.random().real for i in range(entriesSize)]
        self.bias = 1

    def get(self, entries):
        return 1 / (1 + math.exp((-1 * self.getSomme(entries)))).real

    def getSomme(self, entries):
        somme = 0
        for i in range(len(entries) - 1):
            try:
                somme += entries[i] * self.weights[i]
            except IndexError:
                print("Entries : {}, nb poids  {}".format(entries, len(self.weights)))
        somme += self.bias
        return somme.real

    def setWeight(self, index, newvalue):
        self.weights[index] = newvalue

    def getWeight(self, index):
        return self.weights[index]

    def learn(self, entries, result, showWeights, learning_rate):
        df = lambda x: math.exp(-x) / (1 + 2 * math.exp(-x) + math.exp(-2 * x))
        y = self.get(entries)
        e1 = df(self.getSomme(entries)) * (y - result)

        for i in range(len(entries)):
            self.weights[i] -= learning_rate * e1 * entries[i]

        #  print("Résultat attendu : {}, Résultat obtenu : {}, Après correction : {}".format(result, y, self.get(entries)))

    def getError(self, entries, next_errors=tuple(), next_weights=tuple(), final_result=0,
                 right_result=0, column=0):
        df = lambda x: math.exp(-x) / (1 + 2 * math.exp(-x) + math.exp(-2 * x))
        if column == 0:
            return df(self.getSomme(entries)) * (final_result - right_result)
        else:
            column += 1  # ?
            errors_weighted = 0
            for i in range(len(next_errors)):
                errors_weighted += next_errors[i] * next_weights[i]
            return df(self.getSomme(entries)) * errors_weighted
