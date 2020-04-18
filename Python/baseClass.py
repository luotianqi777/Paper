import os
import pandas as pd
from pyecharts.charts import Line
from snapshot_phantomjs import snapshot
from pyecharts.render import make_snapshot
from pyecharts import options as opts


class BaseClass(object):

    def __init__(self, name, type):
        self.baseSavePath = './Output/'
        self.name = name
        self.type = ['.', ''][type[0] == '.'] + type
        if not os.path.exists(self.baseSavePath):
            os.mkdir(self.baseSavePath)

    def getSavePath(self):
        return self.baseSavePath+self.name+self.type


class DataManager(BaseClass):
    def __init__(self, name, type):
        super().__init__(name=name, type=type)

    def isExists(self):
        return os.path.exists(self.getSavePath())

    def getData(self):
        pass

    def saveData(self):
        pass


class Drawer(BaseClass):

    def __init__(self, name):
        super().__init__(name=name, type='png')
        self.baseHtmlSavePath = self.baseSavePath+'html/'
        self.title = name
        self.data = pd.DataFrame()
        self.keys = []
        if not os.path.exists(self.baseHtmlSavePath):
            os.mkdir(self.baseHtmlSavePath)

    def setLineData(self):
        pass

    def getSaveHtmlPath(self):
        return self.baseHtmlSavePath+self.name+'.html'

    def drawLine(self):
        self.setLineData()
        line = (
            Line()
            .add_xaxis(self.data.index.tolist())
            .set_global_opts(title_opts=opts.TitleOpts(title=self.name))
        )
        for key in self.keys:
            line.add_yaxis(
                series_name=key,
                y_axis=self.data[key].tolist(),
                is_smooth=True,
                label_opts=opts.LabelOpts(is_show=False)
            )
        print('保存图片到'+self.getSavePath())
        line.render(self.getSaveHtmlPath())
        make_snapshot(snapshot,
                      file_name=line.render(),
                      output_name=self.getSavePath(),
                      )
