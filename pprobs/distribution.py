import numpy as np
import pandas as pd
from scipy import integrate

class Joint:
    def __init__(self, prob, space_1, space_2, discrete=True):
        self.domains = []
        self.prob = prob
        self.discrete = discrete
        if not callable(prob):
            raise Exception("prob should be function")  
        for space in [space_1, space_2]:
            if discrete:
                if not hasattr(space, '__iter__'):
                    raise Exception('domain should be [a, b] and a < b')
                self.domains.append(set(space))
            else:
                if type(space) != list or len(space) != 2 or space[0] >= space[1]:
                    raise Exception('domain should be [a, b] and a < b')
                self.domains.append(space)
    
    def probability_table(self, force=10):
        spaces = []
        for domain in self.domains:
            if self.discrete:
                spaces.append(domain)
            else:
                spaces.append(np.linspace(domain[0], domain[1], 10 * force))
        prob_matrix = [[self.prob(i, j) for j in spaces[1]] for i in spaces[0]]
        prob_table = pd.DataFrame(prob_matrix)
        prob_table.index = map(lambda x: f"X={x}", spaces[0])
        prob_table.columns = map(lambda y: f"Y={y}", spaces[1])
        return prob_table
    
    def get_prob(self, x, y):
        if self.discrete:
            if hasattr(x, '__iter__') and type(y) in [int, float]:
                return sum([self.prob(x_i, y) for x_i in self.domains[0]])
            elif hasattr(y, '__iter__') and type(x) in [int, float]:
                return sum([self.prob(x, y_i) for y_i in self.domains[1]])
            elif hasattr(x, '__iter__') and hasattr(y, '__iter__'):
                return sum([self.prob(x_i, y_i) for x_i in self.domains[0] for y_i in self.domains[1]])
            else:
                return self.prob(x, y)
        else:
            if hasattr(x, '__iter__') and type(y) in [int, float]:
                up, down = integrate.dblquad(self.prob, x[0], x[1], lambda val: y, lambda val: y + 0.0001)
                return up - down
            elif hasattr(y, '__iter__') and type(x) in [int, float]:
                up, down = integrate.dblquad(self.prob, x, x + 0.0001, lambda val: y[0], lambda val: y[1])
                return up - down
            elif hasattr(x, '__iter__') and hasattr(y, '__iter__'):
                up, down = integrate.dblquad(self.prob, x[0], x[1], lambda val: y[0], lambda val: y[1])
                return up - down
            else:
                return self.prob(x, y)


class Discrete:
    def __init__(self, pmf, space):
        if not callable(pmf):
            raise Exception('pmf should be a function')
        if not hasattr(space, '__iter__'):
            raise Exception('space should be iterable object')
        self.pmf = pmf
        self.space = space
    
    def generate(self, size):
        rand_data = self.space
        prob_data = [self.pmf(x) for x in rand_data]
        total_prob = sum(prob_data)
        mix_data = [(x, prob) for x, prob in zip(rand_data, prob_data)]
        mix_data.sort(key=lambda item: item[1], reverse=True)
        generated_data = []
        for x, prob in mix_data:
            for _ in range(int(size * (prob / total_prob))):
                if np.random.rand() > 0.1:
                    generated_data.append(x)
        while len(generated_data) < size:
            generated_data.append(np.random.choice(rand_data))
        np.random.shuffle(generated_data)
        return generated_data
    
    def get_prob(self, x):
        return self.pmf(x)


class Continuous:
    def __init__(self, pdf, space):
        if not callable(pdf):
            raise Exception('pdf should be a function')
        if type(space) != list or len(space) != 2 or space[0] >= space[1]:
            raise Exception('space should be a list like [a, b] which a < b')
        self.pdf = pdf
        self.left = space[0]
        self.right = space[1]
    
    def generate(self, size):
        rand_data = np.linspace(self.left, self.right, size * 2)
        prob_data = [self.pdf(x) for x in rand_data]
        total_prob = sum(prob_data)
        mix_data = [(x, prob) for x, prob in zip(rand_data, prob_data)]
        mix_data.sort(key=lambda item: item[1], reverse=True)
        generated_data = []
        for x, prob in mix_data:
            for _ in range(int(size * (prob / total_prob))):
                if np.random.rand() > 0.1:
                    generated_data.append(x)
        while len(generated_data) < size:
            generated_data.append(np.random.choice(rand_data))
        np.random.shuffle(generated_data)
        return generated_data
    
    def get_prob(self, x):
        return self.pdf(x)
