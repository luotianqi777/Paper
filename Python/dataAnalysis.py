import os
import dataCrawler
import pandas as pd
import matplotlib.pyplot as plt
import pyecharts.charts as charts
import pyecharts.options as opts
import snapshot_phantomjs.snapshot as snapshot
from pyecharts.render import make_snapshot


class analysiser(object):

    def __init__(self):
        crawler = dataCrawler.DayList()
        # 判断数据文件是否存在
        if not os.path.exists(crawler.savePath):
            # 不存在则读取并保存数据
            print('未找到保存的数据，开始数据获取')
            crawler.run()
        # 读取数据文件
        self.data = pd.read_csv(crawler.savePath)

    def run(self):
        keys = ['today_storeConfirm', 'today_confirm',
                'today_heal', 'today_dead', 'total_dead']
        line = charts.Line().add_xaxis(xaxis_data=self.data['date'].values)
        for key in keys:
            line.add_yaxis(series_name=key, y_axis=self.data[key])
        make_snapshot(snapshot, line.render(), 'test.png')


if __name__ == "__main__":
    analysiser().run()
