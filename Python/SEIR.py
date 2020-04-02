import matplotlib.pyplot as plt
import numpy as np


# more great design
class BaseModel(object):

    def __init__(self, name):
        # model name
        self.name = name
        # line color
        self.color = ['b', 'r', 'g', 'pink', 'grey', '']
        # line label
        self.label = ['susceptible', 'infectious', 'recovered', 'exposed', 'death', '']
        # line style
        self.style = ['-', ':', '-.', '--', '-', '']
        # all people
        self.a = 1
        # susceptible people
        self.s = 0.99
        # exposed people
        self.e = 0
        # infectious people
        self.i = self.a - self.s
        # recovered people
        self.r = 0
        # death people
        self.d = 0
        # a2b is probability of a to b
        self.s2e = 0.5
        self.e2i = 0.2
        self.s2i = self.s2e
        self.e2r = 0.2
        self.i2r = 0.1
        self.i2d = 0.01

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
        plt.savefig('../LaTeX/figure/' + self.name + '.eps', format='eps')
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
        s2e = self.s * self.s2e * (self.e + self.i)
        e2i = self.e * self.e2i
        i2r = self.i * self.i2r
        self.s += -s2e
        self.i += e2i - i2r
        self.r += i2r
        self.e += s2e - e2i
        return [self.s, self.i, self.r, self.e]


class SEIRD(BaseModel):

    def __init__(self):
        super().__init__('SEIRD')

    def integrate(self, t):
        s2e = self.s2e * self.s * (self.i + self.e)
        e2i = self.e2i * self.e
        e2r = self.e2r * self.e
        i2r = self.i2r * self.i
        i2d = self.i2d * self.i
        self.s += -s2e
        self.e += s2e - e2i - e2r
        self.i += e2i - i2r - i2d
        self.r += e2r + i2r
        self.d += i2d
        return [self.s, self.i, self.r, self.e, self.d]
        # Derivative
        # return [s2e, e2i, e2r+i2r, s2e, i2d]


class SEIRC(BaseModel):

    def __init__(self):
        super().__init__('SEIRC')

    def integrate(self, t):
        pass


if __name__ == '__main__':
    model = SEIRD()
    model.run(70)
    # model = SEIR()
    # model.run(100)
