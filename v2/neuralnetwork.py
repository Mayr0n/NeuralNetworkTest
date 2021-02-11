from random import randint
from tkinter import *

from math import exp

from sympy import ln

from v2.errors import SizeError
from v2.layer import Layer
from v2.matrix import Matrix


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
            self.last_results = Matrix.list_to_matrix(results)
            print(self.last_results)
            return Matrix.list_to_matrix(w_entries), Matrix.list_to_matrix(results)
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
    def dcost(index, nb, expected_results):
        return 2 * (nb - expected_results.get((0, index)))

    def learn(self, entries, res):
        taux = 0.1
        m_entries = entries
        m_results = res
        if type(m_entries) != Matrix:
            m_entries = Matrix.list_to_matrix(entries)
        if type(m_results) != Matrix:
            m_results = Matrix.list_to_matrix(res)

        w_feed_entries = self.feed_forward(m_entries)[0]
        w_feed_results = self.feed_forward(m_entries)[1]

        for L in range(1, len(self.layers)):
            # -L sera utilisé pour parcourir les couches à l'envers
            # ainsi, -L + 1 correspond à la couche avant
            layer = self.layers[-L]
            for i in range(len(layer.get_neurons())):
                neuron = layer.get_neurons()[i]
                delta = NeuralNetwork.dsigmoid(w_feed_entries.get((-L, i))) * NeuralNetwork.dcost(i, w_feed_results.get(
                    (-L, i)), m_results)
                errors = Matrix.list_to_matrix(
                    [delta * w_feed_results.get((-L + 1), j) for j in range(w_feed_results.get_len_lines())])
                neuron.weights = neuron.weights + taux * errors

        # delta = dsigmoid(w_ent[i])*dcost(res[i])

    def display(self):
        tk = Tk()
        tk.geometry("1280x720")

        back_frame = Frame(tk, width=1280, height=720)
        canv_frame = Frame(back_frame, width=1280, height=675)
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
                nfr = self.get_neuron_frame(frame, neuron, (240, 120))
                nfr.grid(row=n, column=L)
        return frame

    @staticmethod
    def get_neuron_frame(parent, neuron, size, entry=None, result=None):
        frame = Frame(parent, highlightbackground="black", highlightthickness=1, width=size[0], height=size[1])
        labels = [Label(frame, text=neuron.get_weights()[w]) for w in range(neuron.get_weights().get_len_lines())]
        for i in range(len(labels)):
            frame.rowconfigure(i, weight=1)
            labels[i].grid(row=i, column=0)
        canv = Canvas(frame)
        canv.create_oval(0, 0, 50, 50)
        canv.grid(rowspan=len(labels), column=2)
        if entry is not None and result is not None:
            Label(frame, text=entry).grid(row=0, column=1)
            Label(frame, text=entry).grid(row=0, column=3)
        return frame

    def draw_feed(self, canv):
        self.feed_forward((randint(-5, 5), randint(-5, 5)))
        self.redraw_weights(canv)

    def draw_learning(self, canv):
        pattern = [([0, 1], [0]),
                   ([1, 1], [1]),
                   ([0, 0], [1]),
                   ([1, 0], [0])]
        pat = pattern[randint(0, 5)]
        self.learn(pat[0], pat[1])
        self.redraw_weights(canv)

    def random_weights(self, canv):
        self.layers = []
        for i in range(len(self.size)):
            if i == 0:
                self.layers.append(Layer(self.size[i], self.len_entries))
            else:
                self.layers.append(Layer(self.size[i], self.layers[i - 1].length()))
        self.redraw_weights(canv)
