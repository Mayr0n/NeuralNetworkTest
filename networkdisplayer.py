from tkinter import *
from PIL import Image, ImageTk


class NetworkDisplayer:
    def __init__(self, network, window):
        self.columns_weights = list()  # liste de listes de labels correspondants aux weights
        self.columns_results = list()  # liste correspondant aux résultats
        self.network = network
        self.window = window
        self.refresh()

    def refresh(self, results=list()):
        for i in range(self.network.getNumberOfColumns()):  # pour chaque colonne
            column_labels = list()
            for n in range(self.network.getNumberOfNeuronsOfColumn(i)):  # pour chaque neurone de la colonne
                weights = ""
                neuron = self.network.getNeuron(i, n)
                for w in neuron.weights:
                    weights += "{} \n".format(w)
                weights_label = Label(self.window, text=weights)
                column_labels.append(weights_label)
            self.columns_weights.append(column_labels)

            if len(results) != 0:
                self.columns_results = results

    def display(self):
        for i in range(len(self.columns_weights) - 1):  # pour chaque colonne
            for j in range(len(self.columns_weights[i]) - 1):  # pour chaque neurone
                c_circle = Canvas(self.window, height=50, width=50)
                c_circle.create_oval(0, 0, 50, 50)
                img = ImageTk.PhotoImg(Image.open("equa.png"))
                c_circle.create_image((10, 10), anchor=NW, image=img)
                self.columns_weights[i].grid(column=3 * i, row=j, padx=5, pady=5)
                c_circle.grid(column=3 * i + 1, row=j, padx=5, pady=5)
                self.columns_weights[i][j].grid(column=3 * i + 2, row=j, padx=5, pady=5)
