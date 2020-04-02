import SEIR
import data
import matplotlib.pyplot as plt

if __name__ == '__main__':
    data.DayList().run()
    SEIR.SEIRD().run(100)
