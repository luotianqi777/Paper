import pandas as pd
from baseClass import BaseClass
from pyecharts.charts import Line
from dataCrawler import DataCrawler
from pyecharts import options as opts


class DataAnalysis(BaseClass):

    def __init__(self):
        super().__init__(name='analysis')
        # 截取数据
        self.keys = ['today_storeConfirm', 'today_confirm',
                     'today_heal', 'today_dead', 'total_dead']

    def analysis(self):
        data = DataCrawler().getData()
        line = Line().add_xaxis(data.index.tolist())
        # for key in self.keys:
        for key in data.columns:
            line.add_yaxis(series_name=key,
                           y_axis=data[key].tolist(),
                           label_opts=opts.LabelOpts(is_show=False))
        self.saveImage(line.render())


if __name__ == "__main__":
    DataAnalysis().analysis()
