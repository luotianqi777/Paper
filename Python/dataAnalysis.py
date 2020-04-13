import pandas as pd
from dataCrawler import dataCrawler
from pyecharts.charts import Line
from pyecharts.render import make_snapshot
from snapshot_phantomjs import snapshot


class dataAnalysis(object):

    def __init__(self):
        self.keys = ['today_storeConfirm', 'today_confirm',
                     'today_heal', 'today_dead', 'total_dead']
        self.outfile = 'out.png'
        self.data = dataCrawler().getData()

    def analysis(self):
        line = Line().add_xaxis(self.data['date'].values)
        for key in self.keys:
            line.add_yaxis(series_name=key, y_axis=self.data[key])
        make_snapshot(snapshot, line.render(), self.outfile)


if __name__ == "__main__":
    dataAnalysis().analysis()
