from tkinter import *


class NeuronFrame:
    def __init__(self, parent, size, neuron, entry=None, result=None):
        frame = Frame(parent, size)
        labels = [Label(frame, text=neuron.get_weights(w)) for w in range(len(neuron.get_weights()))]
        for i in range(len(labels)):
            labels[i].grid(row=i, column=0)
        canv = Canvas(frame)
        canv.create_oval(0, 0, 50, 50)
        canv.grid(rowspan=len(labels), column=2)
        if entry is not None and result is not None:
            Label(frame, text=entry).grid(row=0, column=1)
            Label(frame, text=entry).grid(row=0, column=3)
