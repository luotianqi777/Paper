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

    def getSavePath(self):
        if not os.path.exists(self.baseSavePath):
            os.mkdir(self.baseSavePath)
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
        self.area = False

    def setLineData(self):
        pass

    def getSaveHtmlPath(self):
        if not os.path.exists(self.baseHtmlSavePath):
            os.mkdir(self.baseHtmlSavePath)
        return self.baseHtmlSavePath+self.name+'.html'

    def drawLine(self, keys=None):
        if keys == None:
            keys = self.keys
        self.setLineData()
        line = (
            Line()
            .add_xaxis(self.data.index.tolist())
            .set_global_opts(title_opts=opts.TitleOpts(title=self.name))
        )
        for key in keys:
            line.add_yaxis(
                series_name=key,
                y_axis=self.data[key].tolist(),
                is_smooth=True,
                label_opts=opts.LabelOpts(is_show=False),
                areastyle_opts=opts.AreaStyleOpts(
                    opacity=[0.0, 0.3][self.area])
            )
        print('保存图片到'+self.getSavePath())
        line.render(self.getSaveHtmlPath())
        make_snapshot(snapshot,
                      file_name=line.render(),
                      output_name=self.getSavePath(),
                      )


class TexTabelBulier(BaseClass):

    def __init__(self, name, title):
        super().__init__(name=name, type='tex')
        self.baseSavePath = './LaTeX/Table/'
        title = [t.upper() for t in title]
        self.title = []
        for t in title:
            self.title.append('$\\P{'+t[0]+'}{'+t[1]+'}$')
        self.data = []

    def addData(self, data):
        data = ['{:.3f}'.format(num) for num in data]
        self.data.append(data)

    def saveData(self):
        with open(self.getSavePath(), mode='w+') as f:
            f.write('\\begin{tabular}{'+'c'*len(self.title)+'}\n')
            f.write('\\hline\n')
            f.write('&'.join(self.title)+'\\\\\n')
            f.write('\\hline\n')
            for data in self.data:
                f.write('&'.join(data)+'\\\\\n')
            f.write('\\hline\n')
            f.write('\\end{tabular}')
            f.close()
