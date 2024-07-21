import os
from utils.freepage import FreePageList
from utils.meta import Meta, META_PAGE_NUM, PAGE_NUM_SIZE


class PageNumber(int):
    pass


class Page:
    def __init__(self, num, data):
        if num is not None:
            self.num = PageNumber(num)
        else:
            self.num = None
        self.data = data


class Dal:
    def __init__(self, file, page_size, meta, freelist):
        self.file = file
        self.page_size = page_size
        self.meta = meta
        self.freelist = freelist

    @staticmethod
    def get_page_size():
        try:
            page_size = os.sysconf('SC_PAGE_SIZE')
            return page_size
        except (AttributeError, ValueError, OSError):
            print("Could not determine the page size")
            return None

    @classmethod
    def new_dal(cls, path, page_size):
        try:
            file = open(path, 'r+b')
        except FileNotFoundError:
            file = open(path, 'w+b')
            meta = Meta(freelist_page=1)
            freelist = FreePageList()
            dal = cls(file, page_size, meta, freelist)
            dal.write_meta()
            dal.write_freelist()
            return dal

        meta = cls.read_meta(file, page_size)
        freelist = cls.read_freelist(file, page_size, meta.freelist_page)
        return cls(file, page_size, meta, freelist)

    @staticmethod
    def read_meta(file, page_size):
        file.seek(META_PAGE_NUM * page_size)
        data = file.read(page_size)
        meta = Meta()
        # Read only the size of the meta data
        meta.deserialize(data[:PAGE_NUM_SIZE])
        return meta

    @staticmethod
    def read_freelist(file, page_size, freelist_page_num):
        file.seek(freelist_page_num * page_size)
        data = file.read(page_size)
        freelist = FreePageList()
        freelist.deserialize(data)
        return freelist

    def write_meta(self):
        data = self.meta.serialize()
        p = self.allocate_empty_page()
        p.num = META_PAGE_NUM
        p.data[:len(data)] = data
        self.write_page(p)

    def write_freelist(self):
        data = self.freelist.serialize()
        p = self.allocate_empty_page()
        p.num = self.meta.freelist_page
        p.data[:len(data)] = data
        self.write_page(p)

    def allocate_empty_page(self):
        return Page(None, bytearray(self.page_size))

    def write_page(self, p):
        offset = p.num * self.page_size
        self.file.seek(offset)
        self.file.write(p.data)
        self.file.flush()

    def close(self):
        if self.file is not None:
            self.file.close()
            self.file = None
