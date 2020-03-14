import numpy as np
import matplotlib.pyplot as plt

if __name__ == '__main__':
    R = []
    X = []
    for r in np.arange(0, 4, 0.01):
        x = 0.1
        for i in range(500):
            x = r * x * (1 - x)
            if i > 400:
                R.append(r)
                X.append(x)
    plt.scatter(R, X, c='c', s=1)
    plt.grid(True)
    plt.show()
