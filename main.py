import neuron as ne
import random
import neuralnetwork as nn


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

network = nn.NeuralNetwork([2, 1])

for i in range(1):
    key = getRandomKey(results)
    network.getResult(key)
