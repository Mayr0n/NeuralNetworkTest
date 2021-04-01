from math import exp
from random import randint

from network_displayer import NetworkDisplayer
from neuralnetwork import NeuralNetwork

# on va créer un système de training.
# prenons l'équation du plan x+y+z=0

pattern = []
for i in range(20):
    x = randint(0, 5)
    y = randint(0, 5)
    pattern.append(([x, y], [x**2+y]))

nn = NeuralNetwork(2, (3, 2, 1), trainingPattern=pattern,
                   last_function=lambda x: 30 / (1 + exp(-x)), last_df=lambda x: 30*exp(-x) / ((exp(-x) + 1) ** 2))

displayer = NetworkDisplayer(nn)
