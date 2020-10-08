import neuron as ne


class SizeError(Exception):
    print("[ERROR] La taille ne peut être ni négative, ni nulle.")
    pass


class NeuralNetwork:
    structure = list()

    def __init__(self, sizes):
        if len(sizes) <= 0:
            raise SizeError()
        for i in range(len(sizes)):
            column = list()
            for s in sizes:
                if s <= 0:
                    raise SizeError()
                column.append(ne.Neuron())
            self.structure.append(column)

    def getResult(self, entries):
        print(str(entries))
        results = list()
        for i in range(len(self.structure)):
            print("Colonne {}".format(i))
            local_results = list()
            for neuron in self.structure[i]:
                print("Neurone colonne {}".format(i))
                if i == 0:
                    local_results.append(neuron.get(entries))
                else:
                    local_results.append(neuron.get(results[i - 1]))
            results.append(local_results)
        print(str(results))
        return results[len(results) - 1]
