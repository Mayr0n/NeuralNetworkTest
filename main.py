import random
import neuralnetwork as nn
import tkinter as tk


def getRandomKey(dict):
    r = random.randint(0, len(dict))
    i = 0
    key = tuple([])
    for k in results.keys():
        if i == r:
            return k
        else:
            i += 1
            key = k
    return key

results = {
    tuple([0, 1]): 0.5,
    tuple([1, 1]): 1,
    tuple([0, 0]): 0,
    tuple([1, 0]): 0.5
}

print("???????????")
network = nn.NeuralNetwork([4, 3, 1], 2)
print("???????????2")

result = 0

for i in range(1):
    key = getRandomKey(results)
    result = network.getResult(key)[0]
    print("Résultat donné par le système neuronal : {}".format(result))

fenetre = tk.Tk()
canv = tk.Canvas(fenetre, bg="white", height=720, width=1080)
x = 100
y = 100
y_i = 100
for i in range(network.getNumberOfColumns()):  # pour chaque colonne
    for n in range(network.getNumberOfNeuronsOfColumn(i)):  # pour chaque neurone de la colonne
        canv.create_oval(x, y, x+50, y+50, outline="black", width=1)
        weights = ""
        neuron = network.getNeuron(i, n)
        for w in neuron.weights:
            weights += "{} \n".format(w)
        canv.create_text(x - 40, y + 25, text=weights)
        y += 100
    x += 200
    y = y_i+25
    y_i = y

canv.create_text(750, 250, text=result)
canv.pack()
fenetre.mainloop()
