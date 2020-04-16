import pandas as pd
from baseClass import BaseClass
from pyecharts.charts import Line
from dataCrawler import DataCrawler
from pyecharts import options as opts


class DataAnalysiser(BaseClass):

    def __init__(self, name='数据分析图'):
        super().__init__(name=name)
        self.data = DataCrawler().getData()
        self.keys = self.data.columns


class A(DataAnalysiser):
    def __init__(self):
        super().__init__(name='疫情数据')


class B(DataAnalysiser):
    def __init__(self):
        super().__init__(name='确诊重症死亡比例')

    def setLineData(self):
        self.data['确诊重症比例'] = self.data['重症']/self.data['确诊']
        self.data['确诊死亡比例'] = self.data['死亡']/self.data['确诊']
        self.data['重症死亡比例'] = self.data['死亡']/self.data['重症']
        self.keys = ['确诊重症比例', '确诊死亡比例', '重症死亡比例']


class C(DataAnalysiser):
    def __init__(self):
        super().__init__(name='每日新增人数')

    def setLineData(self):
        self.data = self.data - self.data.shift(1)


def saveAllImage():
    A().drawLine()
    B().drawLine()
    C().drawLine()


if __name__ == "__main__":
    saveAllImage()
