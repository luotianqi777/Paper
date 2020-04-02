import SEIR

if __name__ == '__main__':
    # model = predict.SIS()
    # model.run()
    # model = predict.SIR()
    # model.run()
    # model = predict.SIRS()
    # model.run()
    # model = predict.SEIR()
    # model.run()
    # model = predict.SEIRD()
    # model.run()
    model = SEIR.BaseMode()
    model.run(100)
