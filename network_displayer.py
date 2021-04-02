from random import randint
from tkinter import *

from layer import Layer


class NetworkDisplayer:
    def __init__(self, nn):
        self.nn = nn

        self.tk = Tk()
        self.tk.geometry("720x480")
        self.back_frame = Frame(self.tk, width=1280, height=720)
        self.canv_frame = Frame(self.back_frame, width=1280, height=675, highlightbackground="red", highlightthickness=1)
        self.reset_button = Button(self.back_frame, text="Reset", command=lambda: self.random_weights(self.canv_frame))
        self.result_button = Button(self.back_frame, text="Results", command=lambda: self.draw_feed(self.canv_frame))
        self.learn_button = Button(self.back_frame, text="Learn", command=lambda: self.draw_learning(self.canv_frame))
        self.canv_frame.grid(row=0, columnspan=3)
        self.reset_button.grid(row=1, column=0)
        self.result_button.grid(row=1, column=1)
        self.learn_button.grid(row=1, column=2)
        self.back_frame.pack()
        self.redraw_weights()
        self.tk.mainloop()

    def redraw_weights(self):
        for child in self.canv_frame.winfo_children():
            if isinstance(child, Frame):
                child.destroy()
        for L in range(len(self.nn.get_layers())):
            layer = self.nn.get_layer(L)
            for n in range(len(layer.get_neurons())):
                neuron = layer.get_neurons()[n]
                nfr = self.get_neuron_frame(self.canv_frame, neuron)
                nfr.grid(row=n, column=L)

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

    def draw_feed(self):
        self.nn.feed_forward((randint(-5, 5), randint(-5, 5)))
        self.redraw_weights()

    def draw_learning(self, canv):
        j = 10000
        for i in range(j):
            pat = self.nn.training_pattern[randint(0, 3)]
            if i <= j * 0.95:
                self.nn.learn(pat[0], pat[1])
            else:
                self.nn.learn(pat[0], pat[1], printer=True)
            print("{}/{}".format(i, j))
        if i % 10 == 0:
            self.redraw_weights()

    def random_weights(self):
        self.nn.layers = []
        for i in range(len(self.size)):
            if i == 0:
                self.nn.layers.append(Layer(self.nn.size[i], self.nn.len_entries))
            else:
                self.nn.layers.append(Layer(self.nn.size[i], self.nn.layers[i - 1].length()))
        self.redraw_weights()
