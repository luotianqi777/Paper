import json
import numpy as np
import pandas as pd
from dataCrawler import DataCrawler
from scipy.integrate import odeint
from matplotlib import pyplot as plt
from baseClass import DataManager, Drawer, TexTabelBulier
from scipy.optimize import minimize


class Model(Drawer):

    def __init__(self, name, y0: str, args: str):
        super().__init__(name=name)
        self.area = True
        self.trans_rate = 1
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
            'ri': 0.01,
        }
        y0_dict = {
            'i': 100,
            's': 8e4 - 100,
            'e': 0,
            'r': 0,
            'd': 0,
        }
        self.args_key = args.split(',')
        self.args = [arg_dict[key] for key in self.args_key]
        self.y0 = [y0_dict[key] for key in y0]
        self.trueData = self.getTrueData()

    def getDays(self):
        return self.trueData.shape[0]

    def getTrueData(self):
        return DataCrawler().getData()

    def diff(self, y, t, args):
        pass

    def getIntData(self, args):
        data = odeint(func=self.diff,
                      y0=self.y0,
                      t=range(self.getDays()),
                      args=(args,)
                      )
        data = pd.DataFrame(data)
        data.columns = self.keys
        data['日期'] = pd.date_range(
            start=self.trueData.index[0], periods=self.getDays())
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
        trans_index = int(self.trans_rate*self.getDays()//1)
        res = self.trueData[keys] - data[keys]
        res = res.iloc[:trans_index]
        res = res ** 2
        res = np.mean(res)
        res = np.sum(res)
        return res

    def optimize(self):
        res = minimize(self.lose,
                       self.args,
                       bounds=[(0, 1) for i in range(len(self.args))],
                       method='L-BFGS-B')
        print(self.name+' 拟合完成')
        print(res)
        tex = TexTabelBulier(name=self.name, title=self.args_key)
        tex.addData(res.x)
        tex.saveData()
        self.args = res.x
        return self

    def run(self):
        keys = [self.translator[k] for k in self.keys if not k == '易感人群']
        self.data = pd.concat(
            [self.getIntData(self.args), self.trueData[keys]], axis=1)
        self.drawLine(self.keys[1:]+keys)

    # 分段拟合
    def AF(self):
        date = '2020-02-12'
        _name = self.name + '_隔离前'
        name_ = self.name + '_隔离后'
        _data = self.trueData.loc[:date]
        data_ = self.trueData.loc[date:]
        # 拟合整体
        self.optimize().run()
        # 拟合前半段
        self.name = _name
        self.trueData = _data
        self.optimize().run()
        # 拟合后半段
        self.name = name_
        self.y0 = self.getIntData(self.args).loc[date]
        self.trueData = data_
        self.optimize().run()


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
    def __init__(self):
        super().__init__(name='SEIRD',
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


class SEIRS(Model):
    def __init__(self):
        super().__init__(name='SEIRS',
                         y0='seird',
                         args='se,ei,ir,id,ri')
        self.keys = ['易感人群', '携带未患病', '确诊人群', '康复人群', '死亡人数']

    def diff(self, y, t, args):
        s, e, i, r, d = y
        sep, eip,  irp, idp, rip = args
        s2e = sep * s * (i + e) / self.N
        e2i = eip * e
        i2r = irp * i
        i2d = idp * i
        r2i = rip * r
        ds = -s2e
        de = s2e - e2i
        di = e2i - i2r - i2d + r2i
        dr = i2r - r2i
        dd = i2d
        return [ds, de, di, dr, dd]


def saveAllImage():
    SIR().run()
    SEIR().run()
    SEIRD().run()
    SEIRS().run()


def optiAllModel():
    SIR().AF()
    SEIR().AF()
    SEIRD().AF()
    SEIRS().AF()


if __name__ == "__main__":
    SIR().AF()
