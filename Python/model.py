import json
import numpy as np
import pandas as pd
from dataCrawler import DataCrawler
from scipy.integrate import odeint
from matplotlib import pyplot as plt
from baseClass import DataManager, Drawer
from scipy.optimize import minimize


class Model(Drawer):

    def __init__(self, name, y0: str, args: str):
        super().__init__(name=name)
        self.keys = ['易感人群', '确诊人群',
                     '康复人群', '携带未患病', '死亡人数', '']
        self.translator = {
            '确诊人群': '确诊',
            '康复人群': '治愈',
            '携带未患病': '疑似',
            '死亡人数': '死亡'
        }
        self.N = 8e4
        arg_dict = {
            'se': 0.45787809,
            'ei': 0.22186872,
            'si': 0.37807416,
            'ir': 0.04682236,
            'id': 0.00101029,
        }
        y0_dict = {
            'i': 100,
            's': 8e4 - 100,
            'e': 0,
            'r': 0,
            'd': 0,
        }
        self.args = [arg_dict[key] for key in args.split(',')]
        self.y0 = [y0_dict[key] for key in y0]
        self.trueData = self.getTrueData()
        self.days = self.trueData.shape[0]

    def getTrueData(self):
        return DataCrawler().getData()

    def diff(self, y, t, args):
        pass

    def getIntData(self, args):
        data = odeint(func=self.diff,
                      y0=self.y0,
                      t=range(self.days),
                      args=(args,)
                      )
        data = pd.DataFrame(data)
        data.columns = self.keys
        data['日期'] = pd.date_range(
            start=self.trueData.index[0], periods=self.days)
        data['日期'] = [x.strftime('%Y-%m-%d') for x in data['日期']]
        data.set_index('日期', inplace=True)
        return data

    def lose(self, args):
        data = self.getIntData(args=args)
        keys = self.keys
        keys = self.keys[1:]
        data = data[keys]
        data.rename(self.translator, axis=1, inplace=True)
        keys = data.columns
        res = self.trueData[keys] - data[keys]
        res = res ** 2
        res = np.mean(res)
        res = np.sum(res)
        return res

    def optimize(self):
        res = minimize(self.lose, self.args, bounds=[
                       (0, 1) for i in range(len(self.args))])
        print(self.name+' 拟合完成')
        print(res)
        self.args = res.x
        return self

    def run(self):
        self.data = self.getIntData(self.args)
        self.drawLine()


class SIR(Model):
    def __init__(self):
        super().__init__(name='SIR',
                         y0='sir',
                         args='si,ir',
                         )
        self.keys = ['易感人群', '确诊人群', '康复人群']

    def diff(self, y, t, args):
        s, i, r = y
        sip, irp = args
        s2i = i * s * sip/self.N
        i2r = i * irp
        ds = -s2i
        di = s2i - i2r
        dr = i2r
        return [ds, di, dr]


class SEIR(Model):
    def __init__(self):
        super().__init__(name='SEIR',
                         y0='seir',
                         args='se,ei,ir')
        self.keys = ['易感人群', '携带未患病', '确诊人群', '康复人群']

    def diff(self, y, t, args):
        s, e, i, r = y
        sep, eip,  irp = args
        s2e = (i+e)*s*sep/self.N
        e2i = e * eip
        i2r = i * irp
        ds = -s2e
        de = s2e - e2i
        di = e2i - i2r
        dr = i2r
        return [ds, de, di, dr]


class SEIRD(Model):
    def __init__(self, name='SEIRD'):
        super().__init__(name=name,
                         y0='seird',
                         args='se,ei,ir,id')
        self.keys = ['易感人群', '携带未患病', '确诊人群', '康复人群', '死亡人数']

    def diff(self, y, t, args):
        s, e, i, r, d = y
        sep, eip,  irp, idp = args
        s2e = sep * s * (i + e) / self.N
        e2i = eip * e
        i2r = irp * i
        i2d = idp * i
        ds = -s2e
        de = s2e - e2i
        di = e2i - i2r - i2d
        dr = i2r
        dd = i2d
        return [ds, de, di, dr, dd]


class SEIRD_A(SEIRD):

    class SEIRD_F(SEIRD):
        def __init__(self):
            super().__init__(name='SEIRD_F')

        def getTrueData(self):
            data = DataCrawler().getData()
            return data.loc[:'2020-02-20']

    def __init__(self):
        super().__init__(name='SEIRD_A')
        F = SEIRD_A.SEIRD_F()
        F.optimize()
        F.run()
        self.y0 = F.getIntData(self.args).loc['2020-02-20']

    def getTrueData(self):
        data = DataCrawler().getData()
        return data.loc['2020-02-20':]


def saveAllImage():
    SIR().run()
    SEIR().run()
    SEIRD().run()
    SEIRD_A().run()


def optiAllModel():
    SIR().optimize().run()
    SEIR().optimize().run()
    SEIRD().optimize().run()
    SEIRD_A().optimize().run()


if __name__ == "__main__":
    SEIRD_B().optimize().run()
