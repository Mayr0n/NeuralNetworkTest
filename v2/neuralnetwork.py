from math import exp

from sympy import ln

from v2.errors import SizeError
from v2.layer import Layer
from v2.matrix import Matrix


class NeuralNetwork:
    def __init__(self, entries, size):
        self.layers = []
        self.len_entries = entries
        for i in range(len(size)):
            if i == 0:
                self.layers.append(Layer(size[i], entries))
            else:
                self.layers.append(Layer(size[i], self.layers[i - 1].length()))

    def __repr__(self):
        S = ""
        for layer in self.layers:
            S += "{}\n".format(layer)
        return S

    def feed_forward(self, entries):
        m_entries = entries
        if type(entries) != Matrix:
            m_entries = Matrix.list_to_matrix(entries)
        if m_entries.get_len_lines() == self.len_entries:
            results = []
            sums = []
            for i in range(len(self.layers)):
                layer = self.layers[i]
                if i == 0:
                    results.append(layer.feed_forward(m_entries)[0])
                    sums.append(layer.feed_forward(m_entries)[1])
                else:
                    results.append(layer.feed_forward(results[i - 1])[0])
                    sums.append(layer.feed_forward(results[i - 1])[1])
            return results, sums
        raise SizeError("Le nombre d'entrée ne correspond au nombre défini par le système.")

    @staticmethod
    def recipr_sigmoid(x):
        return -ln((1 / x) - 1)

    @staticmethod
    def dsigmoid(x):
        return exp(-x) / ((exp(-x) + 1) ** 2)

    def learn(self, entries, res):  # res = matrix
        taux = 0.1
        results = self.feed_forward(entries)[0]  # Liste matrices, une matrice = une colonne de résultats
        sums = self.feed_forward(entries)[1]  # Liste matrices, une matrice = une colonne de sommes
        final_result = results[len(results) - 1]
        final_sum = sums[len(sums) - 1]
        cost = ((final_result - res)[0]) ** 2
        final_error = self.dsigmoid(final_sum[0]) * cost
        errors = []
        mferror = Matrix()
        mferror.set((0, 0), final_error)
        errors.append(mferror)

        for i in range(1, len(self.layers)):
            layer = self.layers[-i]
            layer_error = Matrix(size=(len(layer.get_neurons()), 1))
            for j in range(len(layer.get_neurons())):
                neuron = layer.get_neurons()[j]
                neuron_sum = sums[-i].get((j, 0))

                weighted_errors = 0
                weights = Matrix(size=(len(layer.get_neurons()), 1))
                for n in range(len(layer.get_neurons())):
                    neuron = layer.get_neurons()[n]
                    weights.set((n, 0), neuron.weights.get((n, 0)))
                weighted_errors = errors[-i] * weights
                wse = weighted_errors.complete_sum()

                err = self.dsigmoid(neuron_sum) * wse
                layer_error.set((j, 0), err)
            errors.append(layer_error)

        errors.reverse()
        for l in range(len(self.layers)):
            layer = self.layers[l]
            errs = errors[l]
            for n in range(layer.length()):
                neuron = layer.get_neurons()[n]
                neuron.set_weights(neuron.get_weights() - errs * taux)
