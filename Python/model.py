import numpy as np
import pandas as pd
from dataCrawler import DataCrawler
from scipy.integrate import odeint
from baseClass import Drawer, TexTabelBulier
from scipy.optimize import minimize


class Model(Drawer):

    def __init__(self, name, y0: str, args: str):
        super().__init__(name=name)
        # 绘制面积图
        self.area = True
        # 保存图像
        self.save = True
        # 选择训练数据范围(0~x, x < 1)
        self.trans_rate = 0.7
        # 数据字段与模型字段映射
        self.translator = {
            '预测确诊': '确诊',
            '预测治愈': '治愈',
            '预测疑似': '疑似',
            '预测死亡': '死亡'
        }
        # 总人数
        self.N = 8e4
        # 初始参数
        arg_dict = {
            'se': 0.45,
            'ei': 0.22,
            'si': 0.37,
            'er': 0.05,
            'ir': 0.04,
            'id': 0.01,
            'ri': 0.01,
        }
        # 初始y0
        y0_dict = {
            'i': 260,
            'e': 54,
            'r': 25,
            'd': 6,
            's': 8e4 - 345,
        }
        # 参数字段列表
        self.args_key = args.split(',')
        # 参数
        self.args = [arg_dict[key] for key in self.args_key]
        # y0(初始值)
        self.y0 = [y0_dict[key] for key in y0]
        # 训练数据
        self.trueData = self.getTrueData()
        # 拟合优度
        self.fit = 0

    # 获取天数

    def getDays(self):
        return self.trueData.shape[0]

    # 获取训练数据
    def getTrueData(self):
        return DataCrawler().getData()

    # 积分函数
    def diff(self, y, t, args):
        pass

    # 获取积分结果
    def getIntData(self, args, days=None):
        if days == None:
            days = self.getDays()
        # 积分
        data = odeint(func=self.diff,
                      y0=self.y0,
                      t=range(days),
                      args=(args,)
                      )
        # 转化为DataFrame对象
        data = pd.DataFrame(data)
        # 修改列名
        data.columns = self.keys
        # 添加时间序列
        data['日期'] = pd.date_range(
            start=self.trueData.index[0], periods=days)
        # 时间转字符串
        data['日期'] = [x.strftime('%Y-%m-%d') for x in data['日期']]
        # 设置时间序列为索引
        data.set_index('日期', inplace=True)
        return data

    # 损失函数
    def lose(self, args):
        # 获取积分结果
        data = self.getIntData(args=args)
        # 去除易感者人群
        keys = self.keys[1:]
        # 获取数据
        data = data[keys]
        # 改变列名(统一列名)
        data.rename(self.translator, axis=1, inplace=True)
        keys = data.columns
        # 计算预测值与真实值的差值
        res = self.trueData[keys] - data[keys]
        res = res**2/self.trueData[keys]
        # 截取训练数据
        trans_index = int(self.trans_rate*self.getDays()//1)
        # 计算拟合优度
        fit = res.iloc[trans_index:]
        fit = np.mean(fit)
        fit = np.mean(fit)
        self.fit = fit
        # 取均值
        res = res.iloc[:trans_index]
        res = np.mean(res)
        res = np.mean(res)
        return res

    # 优化模型
    def optimize(self):
        # 优化模型
        res = minimize(self.lose,
                       self.args,
                       bounds=[(0.001, 0.999) for i in range(len(self.args))],
                       method='L-BFGS-B')
        print(self.name+' 拟合完成')
        print(res)
        # 覆盖当前参数
        self.args = res.x
        # 返回损失值
        return res.fun

    # 运行模型

    def run(self, pri_data=''):
        # 去除易感人群
        keys = [k for k in self.keys if not k == '易感人群']
        # 获取预测值
        if len(pri_data) == 0:
            pri_data = self.getIntData(self.args)[keys]
        # 人群映射
        trans_keys = [self.translator[k] for k in keys]
        # 拼接预测值与真实值
        self.data = pd.concat(
            [pri_data, self.trueData[trans_keys]], axis=1)
        # 储存结果
        TexTabelBulier(name=self.name + '模型拟合数据',
                       data=self.data // 1, isInt=True)
        # 绘制图像
        self.drawLine(keys+trans_keys)

    # 分段拟合
    def AF(self):
        # 隔离措施实施日期
        date = '2020-02-12'
        name = self.name
        _name = name + '隔离前'
        name_ = name + '隔离后'
        _data = self.trueData.loc[:date]
        data_ = self.trueData.loc[date:]
        columns = [t.upper() for t in self.args_key.copy()]
        columns = ['$\\P{'+t[0]+'}{'+t[1]+'}$' for t in columns]
        columns.append('$LOSS$')
        columns.append('$FIT$')
        # 整体拟合
        loss = self.optimize()
        # 保存结果参数
        value = list(self.args.copy())
        value.append(loss)
        value.append(self.fit)
        data = pd.DataFrame([value])
        data.columns = columns
        data.index = ['参数值']
        TexTabelBulier(name=name, data=data)
        self.run()
        # 分段拟合
        # 拟合前半段
        self.name = _name
        self.trueData = _data
        loss = self.optimize()
        value = list(self.args.copy())
        value.append(loss)
        value.append(self.fit)
        temp = value
        self.run()
        # 拟合后半段
        self.name = name_
        # 获取初值
        self.y0 = self.getIntData(self.args).loc[date]
        self.trueData = data_
        loss = self.optimize()
        value = list(self.args.copy())
        value.append(loss)
        value.append(self.fit)
        data = pd.DataFrame([temp, value])
        data.columns = columns
        data.index = ['隔离前参数值', '隔离后参数值']
        TexTabelBulier(name=name+'隔离', data=data)
        self.run()


class SIR(Model):
    def __init__(self):
        super().__init__(name='SIR',
                         y0='sir',
                         args='si,ir',
                         )
        self.keys = ['易感人群', '预测确诊', '预测治愈']

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
                         args='se,ei,er,ir')
        self.keys = ['易感人群', '预测疑似', '预测确诊', '预测治愈']

    def diff(self, y, t, args):
        s, e, i, r = y
        sep, eip, erp, irp = args
        s2e = (i+e)*s*sep/self.N
        e2i = e * eip
        e2r = e * erp
        i2r = i * irp
        ds = -s2e
        de = s2e - e2i - e2r
        di = e2i - i2r
        dr = i2r + e2r
        return [ds, de, di, dr]


class SEIRD(Model):
    def __init__(self):
        super().__init__(name='SEIRD',
                         y0='seird',
                         args='se,ei,er,ir,id')
        self.keys = ['易感人群', '预测疑似', '预测确诊', '预测治愈', '预测死亡']

    def diff(self, y, t, args):
        s, e, i, r, d = y
        sep, eip, erp, irp, idp = args
        s2e = sep * s * (i + e) / self.N
        e2i = eip * e
        e2r = erp * e
        i2r = irp * i
        i2d = idp * i
        ds = -s2e
        de = s2e - e2i - e2r
        di = e2i - i2r - i2d
        dr = i2r + e2r
        dd = i2d
        return [ds, de, di, dr, dd]


class SEIRS(Model):
    def __init__(self):
        super().__init__(name='SEIRS',
                         y0='seird',
                         args='se,ei,er,ir,id,ri')
        self.keys = ['易感人群', '预测疑似', '预测确诊', '预测治愈', '预测死亡']

    def diff(self, y, t, args):
        s, e, i, r, d = y
        sep, eip, erp, irp, idp, rip = args
        s2e = sep * s * (i + e) / self.N
        e2i = eip * e
        e2r = erp * e
        i2r = irp * i
        i2d = idp * i
        r2i = rip * r
        ds = -s2e
        de = s2e - e2i - e2r
        di = e2i - i2r - i2d + r2i
        dr = i2r - r2i + e2r
        dd = i2d
        return [ds, de, di, dr, dd]


class ModelFilter(SEIRD):
    # 用于模拟不同年龄段的人群

    def __init__(self):
        super().__init__()

    def filter(self, name, s_r, i_r, d_r):
        self.name = name
        y0 = self.y0
        trueData = self.trueData
        self.y0[0] = y0[0]*s_r
        self.y0[1] = y0[1]*s_r
        self.y0[2] = y0[2]*i_r
        self.y0[3] = y0[3]*s_r
        self.y0[4] = y0[4]*d_r
        self.trueData['疑似'] = trueData['疑似']*s_r
        self.trueData['确诊'] = trueData['确诊']*i_r
        self.trueData['治愈'] = trueData['治愈'] * s_r
        self.trueData['死亡'] = trueData['死亡']*d_r
        columns = [t.upper() for t in self.args_key.copy()]
        columns = ['$\\P{'+t[0]+'}{'+t[1]+'}$' for t in columns]
        columns.append('$LOSS$')
        columns.append('$FIT$')
        # 整体拟合
        loss = self.optimize()
        # 保存结果参数
        value = list(self.args.copy())
        value.append(loss)
        value.append(self.fit)
        data = pd.DataFrame([value])
        data.columns = columns
        data.index = ['参数值']
        TexTabelBulier(name=name, data=data)
        # self.run()
        data = self.getIntData(self.args)
        self.y0 = y0
        self.trueData = trueData
        return data

    def killTime(self):
        young = self.filter("青年", 0.295, 0.033, 0.0078)
        mean = self.filter("中年", 0.463, 0.157, 0.1818)
        old = self.filter("老年", 0.242, 0.810, 0.8104)
        data = young+mean+old
        self.name = '年龄分层预测结果'
        self.run(pri_data=data)


def optiAllModel():
    SIR().AF()
    SEIR().AF()
    SEIRD().AF()
    SEIRS().AF()
    ModelFilter().killTime()


if __name__ == "__main__":
    optiAllModel()
