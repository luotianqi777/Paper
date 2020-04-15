import os


class BaseClass(object):

    def __init__(self):
        self.baseSavePath = 'Output'
        if not os.path.exists(self.baseSavePath):
            os.mkdir(self.baseSavePath)

    def getSavePath(self, fileName='uname'):
        return os.path.join(self.baseSavePath, fileName)
