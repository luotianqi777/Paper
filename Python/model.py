import numpy as np
import pandas as pd
from baseClass import BaseClass


# more great design
class BaseModel(BaseClass):

    def __init__(self, name):
        super().__init__(name)
        # line label
        self.keys = ['易感人群', '确诊人群',
                     '康复人群', '携带未患病', '死亡人数', '']
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

    def run(self, loop_times=60):
        # save result
        self.data = np.asarray([self.integrate(t) for t in range(loop_times)])
        count = self.data.shape[1]
        self.keys = self.keys[:count]
        self.data = pd.DataFrame(self.data)
        self.data.columns = self.keys
        self.drawLine()

    def integrate(self, t):
        # a2b is probability rate of a to b
        self.s2e = 0.5 - 0.005*t
        self.e2i = 0.8
        self.s2i = self.s2e
        self.e2r = 0.002 * t
        self.i2r = 0.005 * t
        self.i2d = 0.01


class SIR(BaseModel):

    def __init__(self):
        super().__init__('SIR')

    def integrate(self, t):
        super().integrate(t)
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
        super().integrate(t)
        s2e = self.s * self.s2e * (self.e + self.i)
        e2i = self.e * self.e2i
        i2r = self.i * self.i2r
        self.s += -s2e
        self.i += e2i - i2r
        self.r += i2r
        self.e += s2e - e2i
        return [self.s, self.i, self.r, self.e]


class SEIRD(BaseModel):

    def __init__(self, name='SEIRD'):
        super().__init__(name)

    def integrate(self, t):
        super().integrate(t)
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


class SEIRD_(SEIRD):

    def __init__(self):
        super().__init__('SEIRD_变化')

    def setLineData(self):
        self.data -= self.data.shift(1)


def saveAllImage():
    SIR().run()
    SEIR().run()
    SEIRD().run()
    SEIRD_().run()


if __name__ == "__main__":
    SEIRD_().run()
