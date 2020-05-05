import os
import pandas as pd
from pyecharts.charts import Line
from snapshot_phantomjs import snapshot
from pyecharts.render import make_snapshot
from pyecharts import options as opts


class BaseClass(object):
    # 基础类

    def __init__(self, name, type):
        # 数据保存地址
        self.baseSavePath = './Output/'
        # 文件名称
        self.name = name
        # 文件类型
        self.type = ['.', ''][type[0] == '.'] + type

    # 获取文件保存路径
    def getSavePath(self):
        # 路径不存在则创建
        if not os.path.exists(self.baseSavePath):
            os.mkdir(self.baseSavePath)
        return self.baseSavePath+self.name+self.type


class DataManager(BaseClass):

    # 用于管理数据
    def __init__(self, name, type):
        super().__init__(name=name, type=type)

    # 判断文件是否已经存在
    def isExists(self):
        return os.path.exists(self.getSavePath())

    # 获取数据
    def getData(self):
        pass

    # 保存数据
    def saveData(self):
        pass


class Drawer(BaseClass):
    # 用于绘制图像

    def __init__(self, name):
        super().__init__(name=name, type='png')
        # html文件保存路径
        self.baseHtmlSavePath = self.baseSavePath+'html/'
        # 绘制数据源
        self.data = pd.DataFrame()
        # 绘制列
        self.keys = []
        # 是否使用面积图
        self.area = False
        # 是否保存图片
        self.save = True

    # 数据预处理
    def setLineData(self):
        pass

    # 获取html路径
    def getSaveHtmlPath(self):
        if not os.path.exists(self.baseHtmlSavePath):
            os.mkdir(self.baseHtmlSavePath)
        return self.baseHtmlSavePath+self.name+'.html'

    def drawLine(self, keys=None):
        if keys == None:
            keys = self.keys
        # 数据预处理
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
            line.render(self.getSaveHtmlPath())
        if self.save:
            # 保存图像
            print('保存图片到'+self.getSavePath())
            make_snapshot(snapshot,
                          file_name=line.render(),
                          output_name=self.getSavePath(),
                          )


class TexTabelBulier(BaseClass):
    # 用于生成tex表格

    def __init__(self, name, title):
        super().__init__(name=name, type='tex')
        self.baseSavePath = './LaTeX/Table/'
        title = [t.upper() for t in title]
        self.title = ['参数名']
        for t in title:
            if len(t) == 2:
                self.title.append('$\\P{' + t[0] + '}{' + t[1] + '}$')
            else:
                self.title.append(t)
        self.data = []

    # 添加行数据
    def addData(self, indexName, data):
        data = ['{:.3f}'.format(num) for num in data]
        data.insert(0, indexName)
        self.data.append(data)

    def saveData(self):
        with open(self.getSavePath(), mode='w+') as f:
            print('保存数据到', self.getSavePath())
            f.write('\\begin{tabular}{'+'c'*len(self.title)+'}\n')
            f.write('\\hline\n')
            f.write('&'.join(self.title)+'\\\\\n')
            f.write('\\hline\n')
            for data in self.data:
                f.write('&'.join(data)+'\\\\\n')
            f.write('\\hline\n')
            f.write('\\end{tabular}')
            f.close()
