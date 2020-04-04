"""
    author: LTQ
    time: 20.4.2
    get COVID-19 data by web crawler
"""
import matplotlib.pyplot as plt
import requests
import os
import pandas as pd
import json


class WebCrawler(object):

    def __init__(self, keys):
        self.headers = {
            'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36'
        }
        self.url = 'https://c.m.163.com/ug/api/wuhan/app/data/list-total'
        r = requests.get(url=self.url, headers=self.headers)
        if not r.status_code == 200:
            print('request error')
        else:
            print('request success')
        self.data = json.loads(r.text)['data']
        self.keys = keys
        self.savePath = 'data.csv'

    def getData(self):
        pass

    def saveData(self):
        result = []
        for key in self.keys:
            frame = pd.DataFrame([unit[key] for unit in self.getData()])
            frame.columns = [key] if frame.shape[1] == 1 else [key + '_' + column for column in frame.columns]
            result.append(frame)
        data = pd.concat(result, axis=1)
        data.to_csv(self.savePath, index=None)

    def run(self):
        if not os.path.exists(self.savePath):
            self.saveData()
        data = pd.read_csv(self.savePath)
        data['today_storeConfirm'] = data['total_confirm']-data['total_dead']-data['total_heal']
        data['date'] = pd.to_datetime(data['date'])
        data.set_index('date', inplace=True)
        print(data.describe())
        print(data.info())
        data[['today_storeConfirm', 'today_confirm', 'today_heal', 'today_dead', 'total_dead']].plot(marker='o', ms=3)
        plt.legend(bbox_to_anchor=[1, 1])
        plt.grid(axis='y')
        plt.ylabel('people')
        plt.box(False)
        plt.show()



class Province(WebCrawler):
    def __init__(self):
        super().__init__(keys=['name', 'total', 'today'])

    def getData(self):
        return self.data['areaTree'][2]['children']


class Country(WebCrawler):
    def __init__(self):
        super().__init__(keys=['name', 'total', 'today'])

    def getData(self):
        return self.data['areaTree']


class DayList(WebCrawler):
    def __init__(self):
        super().__init__(keys=['date', 'today', 'total'])

    def getData(self):
        return self.data['chinaDayList']


if __name__ == '__main__':
    # crawler = Province()
    crawler = DayList()
    # crawler = Country()
    crawler.run()

