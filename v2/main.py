from v2.matrix import Matrix
from v2.neuralnetwork import NeuralNetwork

nn = NeuralNetwork(4, (4, 2, 3, 1))
results = nn.feed_forward((1, 2, 4, 5))
