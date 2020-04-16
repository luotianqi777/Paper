import os
import json
import requests
import pandas as pd
from baseClass import BaseClass


class DataCrawler(BaseClass):

    def __init__(self):
        super().__init__(name='data', type='csv')
        # 请求头
        self.headers = {
            'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36'
        }
        # 访问位置：网易的数据
        self.url = 'https://c.m.163.com/ug/api/wuhan/app/data/list-total'
        # 结果储存位置
        self.savePath = self.getSavePath()
        # 英汉映射
        self.nameDict = {
            'date': '日期',
            'confirm': '确诊',
            'dead': '死亡',
            'heal': '治愈',
            'severe': '重症',
            'suspect': '疑似',
        }

    def __run__(self):
        # 请求数据
        r = requests.get(url=self.url, headers=self.headers)
        # 检查是否成功
        if not r.status_code == 200:
            print('请求数据失败')
            return
        else:
            print('请求数据成功')
            # 读取读取数据
            data = json.loads(r.text)['data']['chinaDayList']
        # 获取日期
        _date = pd.DataFrame([unit['date'] for unit in data])
        # 修改列名
        _date.columns = ['date']
        # 获取数据
        _data = pd.DataFrame([unit['total'] for unit in data])
        # 拼接数据
        data = pd.concat([_date, _data], axis=1)
        # 英汉映射
        data.rename(columns=self.nameDict, inplace=True)
        # 计算截至目前确诊人数
        data['确诊'] = data['确诊']-data['死亡']-data['治愈']
        # 储存数据
        data.to_csv(self.savePath, index=False)
        # 输出提示信息
        print('数据获取完成，保存到' + self.savePath)

    def getData(self):
        # 未找到数据文件则获取数据
        if not os.path.exists(self.savePath):
            self.__run__()
        # 读取数据
        data = pd.read_csv(self.savePath)
        # 将日期设为索引
        data.set_index('日期', inplace=True)
        return data


if __name__ == '__main__':
    print(DataCrawler().getData().describe())
