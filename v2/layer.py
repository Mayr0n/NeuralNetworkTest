from v2.matrix import Matrix
from v2.neuron import Neuron


class Layer:
    def __init__(self, size, number_entries):
        self.neurons = [Neuron(number_entries) for i in range(size)]

    def __repr__(self):
        S = ""
        for neuron in self.neurons:
            S += "1 "
        return S

    def length(self):
        return len(self.neurons)

    def get_neurons(self):
        return self.neurons

    def feed_forward(self, entries):  # entries est une matrix
        results = Matrix(size=(len(self.neurons), 1))
        sums = Matrix(size=(len(self.neurons), 1))
        for i in range(len(self.neurons)):
            result = self.neurons[i].feed_forward(entries)[0]
            sum = self.neurons[i].feed_forward(entries)[1]
            results.set((i, 0), result)
            sums.set((i, 0), sum)
        return results, sums
