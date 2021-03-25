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
    def __init__(self, entries, size):
        self.layers = []
        self.len_entries = entries
        self.size = size
        self.last_results = []
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

    @staticmethod
    def recipr_sigmoid(x):
        return -ln((1 / x) - 1)

    @staticmethod
    def dsigmoid(x):
        return exp(-x) / ((exp(-x) + 1) ** 2)

    def cost(self, expected_results):
        elts = self.last_results[self.last_results.get_len_lines() - 1] - expected_results
        sum = 0
        for elt in elts.get_column(0):
            sum += elt ** 2
        return sum * 0.5

    @staticmethod
    def dcost(nb, expected):
        return 1 / 2 * (nb - expected) ** 2

    def learn(self, entries, res):
        taux = 0.1
        m_entries = entries
        m_results = res

        z = self.feed_forward(entries)[0]  # liste des sommes pondérées de chaque couche
        a = self.feed_forward(entries)[1]  # liste des sorties de chaque couche
        # pour a et z, chaque élément est une liste correspondant à une couche l

        errors = []  # il y a une erreur par neurone.
        last_errors = [self.dsigmoid(z[-1][n]) * (a[-1][n] - m_results[n]) for n in
                       range(len(self.layers[-1].get_neurons()))]
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
                layer_errors.append(self.dsigmoid(z[-l][n]) * weighted_errors)
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

        print("Avant : \n{}".format(a[-2]))
        print("Après : \n{}".format(self.feed_forward(m_entries)[1][-1]))
        print("Voulu : \n{}".format(m_results))

    def display(self):
        tk = Tk()
        tk.geometry("720x480")

        back_frame = Frame(tk, width=1280, height=720)
        canv_frame = Frame(back_frame, width=1280, height=675, highlightbackground="red", highlightthickness=1)
        reset_button = Button(back_frame, text="Reset", command=lambda: self.random_weights(canv_frame))
        result_button = Button(back_frame, text="Results", command=lambda: self.draw_feed(canv_frame))
        learn_button = Button(back_frame, text="Learn", command=lambda: self.draw_learning(canv_frame))
        canv_frame.grid(row=0, columnspan=3)
        reset_button.grid(row=1, column=0)
        result_button.grid(row=1, column=1)
        learn_button.grid(row=1, column=2)
        back_frame.pack()
        self.redraw_weights(canv_frame)
        tk.mainloop()

    def redraw_weights(self, frame):
        for child in frame.winfo_children():
            if isinstance(child, Frame):
                child.destroy()
        for L in range(len(self.layers)):
            layer = self.layers[L]
            for n in range(len(layer.get_neurons())):
                neuron = layer.get_neurons()[n]
                nfr = self.get_neuron_frame(frame, neuron)
                nfr.grid(row=n, column=L)
        return frame

    @staticmethod
    def get_neuron_frame(parent, neuron, entry=None, result=None):
        frame = Frame(parent, highlightbackground="blue", highlightthickness=1)
        labels = [Label(frame, text=neuron.get_weights()[w]) for w in range(len(neuron.get_weights()))]
        for i in range(len(labels)):
            labels[i].grid(row=i, column=1)
        canv = Canvas(frame, width=50, height=50)
        canv.create_oval(0, 0, 25, 25)
        canv.grid(row=int(len(labels) / 2), column=2)
        if entry is not None and result is not None:
            Label(frame, text=entry).grid(row=1, column=0)
            Label(frame, text=result).grid(row=0, column=3)
        return frame

    def draw_feed(self, canv):
        self.feed_forward((randint(-5, 5), randint(-5, 5)))
        self.redraw_weights(canv)

    def draw_learning(self, canv):
        pattern = [([0, 1, 0, 1], [0, 0, 0]),
                   ([0, 1, 1, 0], [0, 1, 0]),
                   ([1, 0, 0, 1], [1, 0, 1]),
                   ([0, 0, 0, 0], [0, 0, 0])]

        for i in range(100000):
            pat = pattern[randint(0, 3)]
            self.learn(pat[0], pat[1])

    def random_weights(self, canv):
        self.layers = []
        for i in range(len(self.size)):
            if i == 0:
                self.layers.append(Layer(self.size[i], self.len_entries))
            else:
                self.layers.append(Layer(self.size[i], self.layers[i - 1].length()))
        self.redraw_weights(canv)
