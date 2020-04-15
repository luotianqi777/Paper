import os
from snapshot_phantomjs import snapshot
from pyecharts.render import make_snapshot


class BaseClass(object):

    def __init__(self, name, type='png'):
        self.baseSavePath = './Output'
        self.name = name
        self.type = '.'+type
        if not os.path.exists(self.baseSavePath):
            os.mkdir(self.baseSavePath)

    def getSavePath(self):
        return os.path.join(self.baseSavePath, self.name+self.type)

    def saveImage(self, render_file):
        print('保存图片到'+self.getSavePath())
        make_snapshot(snapshot, file_name=render_file,
                      output_name=self.getSavePath())
