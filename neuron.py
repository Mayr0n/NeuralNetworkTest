from math import exp

from matrix import Matrix


class Neuron:
    def __init__(self, number_weights, function=lambda x: 1 / (1 + exp(-x)),
                 dfunction=lambda x: exp(-x) / ((exp(-x) + 1) ** 2)):
        self.weights = Matrix(size=(number_weights, 1), alea=True, set_column=True)
        self.bias = 1
        self.function = function
        self.derivative = dfunction

    def get_weight(self, index):
        return self.weights.get((index, 0))

    def set_weights(self, weights):
        self.weights = weights

    def get_weights(self):
        return self.weights

    def weighted_sum(self, entries):
        weighted_entries = self.weights * entries
        sum = 0
        for item in weighted_entries.get_column(0):
            sum += item
        sum += self.bias
        return sum

    def feed_forward(self, entries):
        return self.weighted_sum(entries), self.function(self.weighted_sum(entries))
        # return z : l'entrée du neurone et a : le résultat de la sigmoide.
