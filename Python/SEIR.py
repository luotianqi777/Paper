import matplotlib.pyplot as plt
import numpy as np


# more great design
class BaseModel(object):

    def __init__(self, name):
        # model name
        self.name = name
        # line color
        self.color = ['b', 'r', 'g', 'pink', 'grey']
        # line label
        self.label = ['susceptible', 'infectious', 'recovered', 'exposed', 'death']
        # line style
        self.style = ['-', ':', '-.', '--', '-']
        # all people
        self.a = 1e3
        # susceptible people
        self.s = self.a - 10
        # exposed people
        self.e = 0
        # infectious people
        self.i = self.a - self.s
        # recovered people
        self.r = 0
        # death people
        self.d = 0
        # a2b is probability of a to b
        self.s2e = 0.3/self.a
        self.e2i = 0.1
        self.s2i = self.s2e*self.e2i/self.a
        self.e2r = 0.2
        self.i2r = 0.1
        self.i2d = 0.1

    def run(self, loop_times=30):
        # save result
        data = np.asarray([self.integrate(t) for t in range(loop_times)])
        # draw lines
        for raw in range(data.shape[1]):
            plt.plot(data[:, raw], color=self.color[raw], linestyle=self.style[raw], label=self.label[raw])
        # set axis label
        plt.xlabel('time')
        plt.ylabel('people')
        # set label
        plt.legend()
        # set title
        plt.title(self.name)
        # save figure
        plt.savefig('../LaTeX/figure/'+self.name+'.eps', format='eps')
        # clear and show figure
        plt.show()

    def integrate(self, t):
        pass


class SIR(BaseModel):

    def __init__(self):
        super().__init__('SIR')

    def integrate(self, t):
        s2i = self.i * self.s * self.s2i
        i2r = self.i * self.i2r
        self.s += -s2i
        self.i += s2i - i2r
        self.r += i2r
        return [self.s, self.i, self.r]


class SEIR(BaseModel):

    def __init__(self):
        super().__init__('SEIR')

    def integrate(self, t):
        s2e = self.s * self.s2e * (self.e+self.i)
        e2i = self.e * self.e2i
        i2r = self.i * self.i2r
        self.s += -s2e
        self.i += e2i - i2r
        self.r += i2r
        self.e += s2e - e2i
        return [self.s, self.i, self.r, self.e]


if __name__ == '__main__':
    model = SEIR()
    model.run(100)
