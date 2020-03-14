import matplotlib.pyplot as plt
import numpy as np
import os


class BaseMode(object):

    def __init__(self):
        self.save_path = '../LaTeX/figure'
        self.save_name = 'infect'
        self.all_people = 1.1e7
        self.infectious_people = 8
        self.susceptible_people = self.all_people - self.infectious_people

    def run(self, loop_times=70):
        # save result
        date = []
        for i in range(loop_times):
            date.append(self.integrate())
        date = np.asarray(date)
        # draw image
        self.draw(date)
        plt.legend()
        plt.xlim((15, loop_times))
        plt.xlabel('time(day)')
        plt.ylabel('people')
        plt.title(self.save_name)
        self.save_name = 'infect_' + self.save_name + '.eps'
        plt.savefig(os.path.join(self.save_path, self.save_name), format='eps')
        plt.show()

    @staticmethod
    def draw(date):
        pass

    def integrate(self):
        pass


class SI(BaseMode):

    def __init__(self):
        super().__init__()
        self.save_name = 'SI'
        # susceptible->infectious(exposed in SEIR)_P
        self.alpha = 0.7/self.all_people
        # susceptible people
        self.S = self.susceptible_people
        # infectious people
        self.II = self.infectious_people

    def integrate(self):
        s = self.S
        ii = self.II
        temp = self.alpha * s * ii
        self.S += -temp
        self.II += temp
        return [self.S, self.II]

    @staticmethod
    def draw(date):
        plt.plot(date[:, 0], color='g', label='susceptible')
        plt.plot(date[:, 1], color='r', linestyle='--', label='infectious')


class SIS(SI):

    def __init__(self):
        super().__init__()
        self.save_name = 'SIS'
        # infectious->recovered_P
        self.gamma = 0.1

    def integrate(self):
        s = self.S
        ii = self.II
        temp = self.alpha * s * ii - self.gamma * ii
        self.S += -temp
        self.II += temp
        return [self.S, self.II]


class SIR(SIS):

    def __init__(self):
        super().__init__()
        self.save_name = 'SIR'
        # recovered people
        self.R = 0

    def integrate(self):
        s = self.S
        ii = self.II
        temp = self.alpha * s * ii
        self.R += self.gamma * self.II
        self.S += -temp
        self.II += temp - self.gamma * self.II
        return [self.S, self.II, self.R]

    @staticmethod
    def draw(date):
        SIS.draw(date)
        plt.plot(date[:, 2], color="c", linestyle='-.', label='recovered')


class SIRS(SIR):

    def __init__(self):
        super().__init__()
        self.save_name = 'SIRS'
        # infectious->susceptible_P(exposed->infect_P in SEIR)
        self.beta = 0.1

    def integrate(self):
        r = self.R
        s = self.S
        ii = self.II
        temp = self.alpha * s * ii
        self.R += self.gamma * ii - self.beta * r
        self.S += -temp + self.beta * r
        self.II += temp - self.gamma * ii
        return [self.S, self.II, self.R]


class SEIR(SIRS):

    def __init__(self):
        super().__init__()
        self.save_name = 'SEIR'
        # exposed people
        self.E = 0
        # exposed->recovered_P
        self.gamma_2 = 0.2

    def integrate(self):
        r = self.R
        s = self.S
        e = self.E
        ii = self.II
        temp = self.alpha * s * (ii + e)
        self.S += -temp
        self.E += temp - (self.beta + self.gamma_2) * e
        self.II += self.beta * e - self.gamma * ii
        self.R += self.gamma_2 * e + self.gamma * ii
        return [self.S, self.II, self.R, self.E]

    @staticmethod
    def draw(date):
        SIRS.draw(date)
        plt.plot(date[:, 3], color='grey', linestyle=':', label='exposed')


class SEIRD(SEIR):

    def __init__(self):
        super().__init__()
        self.save_name = 'SEIRD'
        # death people
        self.D = 0
        # infectious->death_P
        self.beta_2 = 0.03

    def integrate(self):
        r = self.R
        s = self.S
        e = self.E
        d = self.D
        ii = self.II
        temp = self.alpha * s * (ii + e)
        self.S += -temp
        self.E += temp - (self.beta + self.gamma_2) * e
        self.II += self.beta * e - (self.gamma + self.beta_2) * ii
        self.R += self.gamma_2 * e + self.gamma * ii
        self.D += self.beta_2 * ii
        return [self.S, self.II, self.R, self.E, self.D]

    @staticmethod
    def draw(date):
        SEIR.draw(date)
        plt.plot(date[:, 4], color='k', label='death')
