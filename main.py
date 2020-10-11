import random
import neuralnetwork as nn
import tkinter as tk


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


def displayNetwork(canvas, nen):
    canvas.delete("all")
    global nb
    nb += 1
    x = 100
    y = 100
    y_i = 100
    key = getRandomKey(training)
    results = nen.learn(key, training.get(key), False)
    canvas.create_text(150, 50,
                       text="Entrées : {}, Sortie attendue : {} \n Entrée n°{}".format(key, training.get(key), nb))
    print("Entrées : {}, Sortie attendue : {}, Sortie obtenue : {}".format(key, training.get(key),
                                                                           nen.getFinalResult(key)))

    for i in range(nen.getNumberOfColumns()):  # pour chaque colonne
        for n in range(nen.getNumberOfNeuronsOfColumn(i)):  # pour chaque neurone de la colonne
            weights = ""
            neuron = nen.getNeuron(i, n)
            for w in neuron.weights:
                weights += "{} \n".format(w)
            canvas.create_oval(x, y, x + 50, y + 50, outline="black", width=1)
            canvas.create_text(x - 40, y + 25, text=weights)
            canvas.create_text(x + 100, y + 20, text=str(results[i][n]))
            y += 100
        x += 300
        y = y_i + 25
        y_i = y


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

fenetre = tk.Tk()
canv = tk.Canvas(fenetre, bg="white", height=720, width=1080)

network = nn.NeuralNetwork([4, 2, 1], 2)

displayNetwork(canv, network)
tk.Button(fenetre, text="Changer les poids", fg="black", bg="grey",
          command=lambda: displayNetwork(canv, network)).pack()
canv.pack()
fenetre.mainloop()
