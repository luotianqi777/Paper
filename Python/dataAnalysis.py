import pandas as pd
from baseClass import BaseClass
from pyecharts.charts import Line
from dataCrawler import DataCrawler
from pyecharts import options as opts


class DataAnalysiser(BaseClass):

    def __init__(self, name, keys):
        super().__init__(name=name)
        self.keys = keys

    def analysis(self):
        data = DataCrawler().getData()
        line = (Line()
                .add_xaxis(data.index.tolist())
                .set_global_opts(title_opts=opts.TitleOpts(title=self.name)))
        for key in self.keys:
            line.add_yaxis(series_name=key,
                           y_axis=data[key].tolist(),
                           label_opts=opts.LabelOpts(is_show=False),
                           is_smooth=True)
        self.saveImage(line.render())


# 日期,今日确诊,今日死亡,今日治愈,今日重症,累计确诊,今日疑似,累计确诊,累计死亡,累计治愈,累计重症,累计疑似

class A(DataAnalysiser):
    def __init__(self):
        super().__init__(name='疫情数据A', keys=['累计确诊', '累计死亡', '累计治愈', '累计疑似'])


if __name__ == "__main__":
    A().analysis()
