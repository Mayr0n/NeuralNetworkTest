import random
from tkinter import *
from sympy import *

import neuralnetwork as nn

training = {
    tuple([0, 1]): 1,
    tuple([1, 1]): 0,
    tuple([0, 0]): 0,
    tuple([1, 0]): 1
}


def getRandomKey(dict):
    r = random.randint(0, len(dict))
    i = 0
    key = tuple([])
    for k in training.keys():
        if i == r:
            return k
        else:
            i += 1
            key = k
    return key


def getRandomNetwork():
    return nn.NeuralNetwork([4, 2, 1], 2)


def learn(network, times):
    for i in range(times):
        key = getRandomKey(training)
        network.learn(key, training.get(key))
    return network.getResults(getRandomKey(training))


def displayNetwork(network, window, results=list()):
    for c in range(len(network.getColumns())):  # pour chaque colonne
        for j in range(len(network.getColumns()[c])):  # pour chaque neurone de la colonne
            weights = ""
            neuron = network.getNeuron(c, j)
            for w in neuron.weights:
                weights += "{} \n".format(w)
            weights_label = Label(window, text=weights)
            c_circle = Canvas(window, bg="white", height=50, width=50)
            c_circle.create_oval(0, 0, 50, 50)
            # im = Image.open(getLatex(5))
            # img = PIL.ImageTk.PhotoImage(im)
            # c_circle.img = img
            # c_circle.create_image((0, 0), anchor=NW, image=img)
            weights_label.grid(column=3 * c, row=j, padx=5, pady=5)
            c_circle.grid(column=3 * c + 1, row=j, padx=5, pady=5)
            if len(results) != 0:
                results_label = Label(window, text=results[c][j])
                results_label.grid(column=3 * c + 2, row=j, padx=5, pady=5)


def display(network, fenetre):
    key = getRandomKey(training)
    displayNetwork(network, fenetre, network.learn(key, training.get(key)))

def display_nul(network, fenetre):
    key = getRandomKey(training)
    displayNetwork(network, fenetre, network.getResults(key))

def getLatex(entry):
    f = symbols("f", cls=Function)
    f = 1 / (1 + exp(-entry))
    return preview(f, viewer='file', filename='equa.png', euler=False)
