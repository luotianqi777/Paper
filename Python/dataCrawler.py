import json
import requests
import pandas as pd


class WebCrawler(object):

    def __init__(self, keys):
        # 请求头
        self.headers = {
            'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36'
        }
        # 访问位置：网易的数据
        self.url = 'https://c.m.163.com/ug/api/wuhan/app/data/list-total'
        # 提取关键字
        self.keys = keys
        # 结果储存位置
        self.savePath = 'data.csv'
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

    # 获取数据
    def getData(self):
        # 请求数据
        r = requests.get(url=self.url, headers=self.headers)
        # 检查是否成功
        if not r.status_code == 200:
            print('request error')
            return
        else:
            print('request success')
            # 返回读取数据
            return json.loads(r.text)['data']

    # 运行爬虫并保存数据
    def run(self):
        result = []
        data = self.getData()
        # 截取每个关键字
        for key in self.keys:
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
        # 将日期列数据类型改为date类
        data['date'] = pd.to_datetime(data['date'])
        # 将日期设为索引
        data.set_index('date', inplace=True)
        # 储存数据
        data.to_csv(self.savePath)
        # 输出提示信息
        print('数据获取完成，保存到'+self.savePath)


class Province(WebCrawler):
    def __init__(self):
        super().__init__(keys=['name', 'total', 'today'])

    def getData(self):
        return super().getData()['areaTree'][2]['children']


class Country(WebCrawler):
    def __init__(self):
        super().__init__(keys=['name', 'total', 'today'])

    def getData(self):
        return super().getData()['areaTree']


class DayList(WebCrawler):
    def __init__(self):
        super().__init__(keys=['date', 'today', 'total'])

    def getData(self):
        return super().getData()['chinaDayList']


if __name__ == '__main__':
    # crawler = Province()
    crawler = DayList()
    # crawler = Country()
    # crawler.saveData()
    crawler.run()
