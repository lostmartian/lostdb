import os

class Page:
    def __init__(self, num, data):
        self.num = num
        self.data = data

class dataAccessLayer:
    def __init__(self, path, page_size):
        self.path = path
        self.page_size = page_size
        self.file = self.open_file(path)

    def open_file(self, path):
        if os.path.exists(path):
            return open(path, 'r+b')
        return open(path, 'w+b')
    
    @classmethod
    def newInstance(cls, path, page_size):
        return cls(path, page_size)
    
