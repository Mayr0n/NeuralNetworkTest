from random import randint
from tkinter import *

from math import exp

from sympy import ln

from errors import SizeError
from layer import Layer
from matrix import Matrix


def lSum(termes):
    sum = 0
    for i in termes:
        sum += i
    return sum


class NeuralNetwork:
    def __init__(self, entries, size, trainingPattern,
                 last_function=lambda x: 1 / (1 + exp(-x)), last_df=lambda x: exp(-x) / ((exp(-x) + 1) ** 2), weights=None):
        self.layers = []
        self.len_entries = entries
        self.size = size
        self.training_pattern = trainingPattern
        self.last_results = []
        for i in range(len(size)):
            if i == 0:
                self.layers.append(Layer(size[i], entries))
            elif i == len(size) - 1:
                self.layers.append(Layer(size[i], self.layers[i - 1].length(), function=last_function, df=last_df))
            else:
                self.layers.append(Layer(size[i], self.layers[i - 1].length()))

    def get_layers(self):
        return self.layers

    def get_layer(self, index):
        return self.layers[index]

    def __repr__(self):
        S = ""
        for layer in self.layers:
            S += "{}\n".format(layer)
        return S

    def feed_forward(self, entries):
        m_entries = entries
        if type(entries) != Matrix:
            m_entries = Matrix.list_to_matrix(entries)

        results = [m_entries]
        # les entrées font partie des results pour éviter la disjonction de cas lors de la rétropropagation

        if m_entries.get_len_lines() == self.len_entries:
            w_entries = []
            for i in range(1, len(self.layers) + 1):
                layer = self.layers[i - 1]
                w_entries.append(layer.feed_forward(results[i - 1])[0])
                results.append(layer.feed_forward(results[i - 1])[1])
            self.last_results = [results]
            return [w_entries, results[1:]]
            # retourne les sommes pondérées [0] et les résultats après sigmoïde [1]
            # les données sont entrées de la couche 1 à L dans l'ordre croissant.
        raise SizeError("Le nombre d'entrées ne correspond au nombre défini par le système.")

    # def cost(self, expected_results):
    #     elts = self.last_results[self.last_results.get_len_lines() - 1] - expected_results
    #     sum = 0
    #     for elt in elts.get_column(0):
    #         sum += elt ** 2
    #     return sum * 0.5
    #
    # @staticmethod
    # def dcost(nb, expected):
    #     return 1 / 2 * (nb - expected) ** 2

    def learn(self, entries, res, printer=False):
        taux = 0.01
        m_entries = entries
        m_results = res

        z = self.feed_forward(entries)[0]  # liste des sommes pondérées de chaque couche
        a = self.feed_forward(entries)[1]  # liste des sorties de chaque couche
        # pour a et z, chaque élément est une liste correspondant à une couche l

        errors = []  # il y a une erreur par neurone.
        last_errors = []
        for n in range(len(self.layers[-1].get_neurons())):
            neuron = self.layers[-1].get_neuron(n)
            last_errors.append(neuron.derivative(z[-1][n]) * (a[-1][n] - m_results[n]))
        # toutes les erreurs de la dernière colonne.
        errors.append(last_errors)  # Sûr.

        for l in range(2, len(self.layers)+1):  # on démarre à 2 parce que la dernière couche correspond à -1
            layer = self.layers[-l]
            next_layer = self.layers[-l + 1]
            layer_errors = []
            errors.reverse()  # permet d'avoir la liste des erreurs de la couche d'après juste en prenant l'élément 0
            for n in range(len(layer.get_neurons())):
                neuron = layer.get_neuron(n)
                weighted_errors = 0
                for n2 in range(len(next_layer.get_neurons())):
                    neuron2 = next_layer.get_neuron(n2)
                    weighted_errors += errors[0][n2] * neuron2.get_weight(n)
                layer_errors.append(neuron.derivative(z[-l][n]) * weighted_errors)
            errors.reverse()
            errors.append(layer_errors)

        errors.reverse()
        a.append(m_entries)

        for l in range(len(self.layers)):
            layer = self.layers[l]
            for n in range(len(layer.get_neurons())):
                neuron = layer.get_neuron(n)
                new_weights = []
                for w in range(len(neuron.get_weights())):
                    new_weights.append(neuron.get_weight(w) - taux * errors[l][n] * a[l - 1][w])
                neuron.set_weights(Matrix.list_to_matrix(new_weights))

        if printer:
            print("Avant : \n{}".format(a[-2]))
            print("Après : \n{}".format(self.feed_forward(m_entries)[1][-1]))
            print("Voulu : \n{}".format(m_results))
