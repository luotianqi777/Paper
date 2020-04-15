from baseClass import BaseClass
import pandas as pd
from dataCrawler import DataCrawler
from pyecharts.charts import Line
from pyecharts import options as opts
from pyecharts.render import make_snapshot
from snapshot_phantomjs import snapshot


class DataAnalysis(BaseClass):

    def __init__(self):
        super().__init__()
        # 截取数据
        self.keys = ['today_storeConfirm', 'today_confirm',
                     'today_heal', 'today_dead', 'total_dead']
        # 输出文件
        self.outfile = self.getSavePath('analysis.png')

    def analysis(self):
        data = DataCrawler().getData()
        line = Line().add_xaxis(data.index.tolist())
        # for key in self.keys:
        for key in data.columns:
            line.add_yaxis(series_name=key,
                           y_axis=data[key].tolist(),
                           label_opts=opts.LabelOpts(is_show=False))
        make_snapshot(snapshot, line.render(), self.outfile)


if __name__ == "__main__":
    DataAnalysis().analysis()
