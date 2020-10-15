import random as r
import cmath as math


class Neuron:

    def __init__(self, entriesSize):
        self.bias_value = 1
        self.weights = list()
        self.bias = {self.bias_value: r.random()*2}  # /!\
        for i in range(entriesSize):
            self.weights.append(r.random())

    def get(self, entries):
        return 1 / (1 + math.exp((-1 * self.getSomme(entries)))).real

    def getSomme(self, entries):
        somme = 0
        for i in range(len(entries)):
            somme += entries[i] * self.weights[i]
        somme += self.bias.get(self.bias_value)
        return somme.real

    def getBiasWeight(self):
        return self.bias.get(self.bias_value)

    def setBiasWeight(self, weight):
        self.bias[self.bias_value] = weight

    def setWeight(self, index, newvalue):
        self.weights[index] = newvalue

    def getWeight(self, index):
        return self.weights[index]

    def learn(self, entries, result, showWeights):
        # error e1 = f'(somme)*(y-t) ; f'(x) = math.exp(-x)/(1+2*math.exp(-x)+math.exp(-2*x))
        df = lambda x: math.exp(-x) / (1 + 2 * math.exp(-x) + math.exp(-2 * x))
        y = self.get(entries)
        e1 = df(self.getSomme(entries)) * (y - result)

        for i in range(len(entries)):
            self.weights[i] -= 10 * e1 * entries[i]
        self.setBiasWeight(self.getBiasWeight() - 10 * e1 * 1)

        print("Résultat attendu : {}, Résultat obtenu : {}, Après correction : {}".format(result, y, self.get(entries)))
        if showWeights:
            for i in range(len(entries)):
                print("{}".format(self.weights[i].real))

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