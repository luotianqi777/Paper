import os
import json
import requests
import pandas as pd
from baseClass import BaseClass


class DataCrawler(BaseClass):

    def __init__(self):
        super().__init__()
        # 请求头
        self.headers = {
            'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36'
        }
        # 访问位置：网易的数据
        self.url = 'https://c.m.163.com/ug/api/wuhan/app/data/list-total'
        # 结果储存位置
        self.savePath = self.getSavePath('data.csv')
        # 英汉映射
        self.nameDict = {
            'date': '日期',
            'today_confirm': '今日确诊',
            'today_dead': '今日死亡',
            'today_heal': '今日治愈',
            'today_severe': '今日重症',
            'today_storeConfirm': '累计确诊',
            'today_suspect': '今日疑似',
            'total_confirm': '累计确诊',
            'total_dead': '累计死亡',
            'total_heal': '累计治愈',
            'total_severe': '累计重症',
            'total_suspect': '累计疑似'
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
        result = []
        # 截取每个关键字
        for key in ['date', 'today', 'total']:
            # 提取每个关键字的数据
            frame = pd.DataFrame([unit[key] for unit in data])
            # 更改列名
            frame.columns = [key] if frame.shape[1] == 1 else [
                key + '_' + column for column in frame.columns]
            result.append(frame)
        # 将数据进行拼接
        data = pd.concat(result, axis=1)
        # 计算截至今日已确诊人数
        data['today_storeConfirm'] = data['total_confirm'] - \
            data['total_dead'] - data['total_heal']
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
        data.set_index('date', inplace=True)
        return data


if __name__ == '__main__':
    print(DataCrawler().getData().describe())
