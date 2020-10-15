import random
import neuralnetwork as nn
from tkinter import *
from networkdisplayer import *


# ----------------------------------------------------------------
# Les fonctions
# ----------------------------------------------------------------

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


def learn():
    key = getRandomKey(training)
    results = network.learn(key, training.get(key), False)
    print("Entrées : {}, Sortie attendue : {}, Sortie obtenue : {}".format(key, training.get(key),
                                                                           network.getFinalResult(key)))
    return results


def displayNetwork(network, window, results=list()):
    for c in range(len(network.getColumns())):  # pour chaque colonne
        for j in range(len(network.getColumns()[c])):  # pour chaque neurone de la colonne
            weights = ""
            neuron = network.getNeuron(c, j)
            for w in neuron.weights:
                weights += "{} \n".format(w)
            weights_label = Label(window, text=weights)
            c_circle = Canvas(window, bg="black", height=50, width=50)
            c_circle.create_oval(0, 0, 50, 50)
            weights_label.grid(column=3 * c, row=j, padx=5, pady=5)
            c_circle.grid(column=3 * c + 1, row=j, padx=5, pady=5)
            if len(results) != 0:
                results_label = Label(window, text=results[c][j])
                results_label.grid(column=3 * c + 2, row=j, padx=5, pady=5)


def display():
    displayNetwork(network, fenetre, learn())

# ----------------------------------------------------------------
# Corps
# ----------------------------------------------------------------

nb = 0

training = {
    tuple([0, 1]): 0.5,
    tuple([1, 1]): 1,
    tuple([0, 0]): 0,
    tuple([1, 0]): 0.5
}

fenetre = Tk()

network = nn.NeuralNetwork([4, 2, 1], 2)
displayer = NetworkDisplayer(network, fenetre)


Button(fenetre, text="Changer les poids", fg="black", bg="grey",
       command=lambda: display()).grid(column=4, row=15, padx=15, pady=15)

display()

#for i in range(1000):
#    fenetre.after(1000, lambda: display())

fenetre.mainloop()
