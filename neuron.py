import random as r
import cmath as math


class Neuron:

    def __init__(self, entriesSize):
        self.weights = list()
        self.bias = 1
        for i in range(entriesSize + 2):
            self.weights.append(r.random())

    def get(self, entries):
        return 1 / (1 + math.exp((-1*self.getSomme(entries)))).real

    def getSomme(self, entries):
        somme = 0
        for i in range(len(entries)):
            # print("Weight {} : {}".format(i, self.weights[i]))
            somme += entries[i] * self.weights[i]
        # print("Somme : {}".format(somme))
        somme += self.bias * self.weights[len(self.weights)-1]
        return somme.real

    def learn(self, entries, result, showWeights):
        # error e1 = f'(somme)*(y-t) ; f'(x) = math.exp(-x)/(1+2*math.exp(-x)+math.exp(-2*x))
        df = lambda x: math.exp(-x) / (1 + 2 * math.exp(-x) + math.exp(-2 * x))
        y = self.get(entries)
        e1 = df(self.getSomme(entries)) * (y - result)

        for i in range(len(entries)):
            self.weights[i] -= 10 * e1 * entries[i]
        self.weights[len(entries)+1] -= 10 * e1 * self.bias

        print("Résultat attendu : {}, Résultat obtenu : {}, Après correction : {}".format(result, y, self.get(entries)))
        if showWeights:
            for i in range(len(entries)):
                print("{}".format(self.weights[i].real))
