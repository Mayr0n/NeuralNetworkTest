from v2.matrix import Matrix
from v2.neuralnetwork import NeuralNetwork

NN = NeuralNetwork(3, [2, 4, 2, 1])

entries = Matrix(size=[3, 1])
entries.set_column(0, [2, 1, 1])

res = Matrix()
res.set_column(0, [1])

results = NN.learn(entries, res)
