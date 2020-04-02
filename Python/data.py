"""
    author: LTQ
    time: 20.4.2
    get COVID-19 data by web crawler
"""
import matplotlib.pyplot as plt
import requests
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
        self.getData()

    def getData(self):
        pass

    def run(self):
        result = []
        for key in self.keys:
            frame = pd.DataFrame([unit[key] for unit in self.data])
            if frame.shape[1] == 1:
                frame.columns = [key]
            else:
                frame.columns = [key + '_' + column for column in frame.columns]
            result.append(frame)
        data = pd.concat(result, axis=1)
        data.plot()
        plt.show()


class Province(WebCrawler):
    def __init__(self):
        super().__init__(keys=['name', 'total', 'today'])

    def getData(self):
        self.data = self.data['areaTree'][2]['children']


class Country(WebCrawler):
    def __init__(self):
        super().__init__(keys=['name', 'total', 'today'])

    def getData(self):
        self.data = self.data['areaTree']


class DayList(WebCrawler):
    def __init__(self):
        super().__init__(keys=['date', 'today'])

    def getData(self):
        self.data = self.data['chinaDayList']


if __name__ == '__main__':
    # bug = Province()
    bug = DayList()
    # bug = Country()
    bug.run()
