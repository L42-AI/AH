from main import main
from collections import Counter
import matplotlib.pyplot as plt
from tqdm import tqdm


class Baseline():
    def __init__(self, iters=2):
        self.costs = {}
        self.run(iters)
        self.plot()

    def run(self, iters):
        costs = []
        for _ in tqdm(range(iters)):
            costs.append(main())
        self.costs = Counter(costs)

    def plot(self):

        plt.title('Schedule algorithm baseline (based on random)')
        plt.bar(x = self.costs.keys(), height = self.costs.values(), width=2, edgecolor='black', color='red')
        plt.xlabel('Malus points')
        plt.ylabel('Frequency')
        plt.show()

