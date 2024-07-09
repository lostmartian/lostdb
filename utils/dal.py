import os
from utils.freepage import FreePageList
from utils.meta import Meta, META_PAGE_NUM, PAGE_NUM_SIZE

# Get system page size


def get_page_size():
    try:
        page_size = os.sysconf(os.sysconf_names['SC_PAGESIZE'])
        return page_size
    except AttributeError:
        print("Could not determine the page size")
        return None

# A subclass for int
# This means that the int type and PageNumber type is now same just that we have a explicit
# int type called PageNumber to denote PageNumber


class PageNumber(int):
    pass


class Page:
    def __init__(self, num, data):
        # num is of type PageNumber. It is an instance of PageNumber
        if num is not None:
            self.num = PageNumber(num)
        else:
            self.num = None
        self.data = data


class Dal:
    def __init__(self, path):
        self.file = None
        self.page_size = self.get_page_size()
        self.free_page_list = FreePageList()
        self.meta = Meta.new_empty_meta()

        if os.path.exists(path):
            try:
                self.file = open(path, 'r+b')
            except Exception as e:
                print(f"Error opening file: {e}")
                if self.file:
                    self.file.close()
                return None

            meta = self.read_meta()
            if meta:
                self.meta = meta

            freelist = self.read_freelist()
            if freelist:
                self.free_page_list = freelist

        else:
            try:
                self.file = open(path, 'w+b')
            except Exception as e:
                print(f"Error creating file: {e}")
                if self.file:
                    self.file.close()
                return None

            self.free_page_list = FreePageList()
            self.freelist_page = self.get_next_page()
            written_freelist = self.write_freelist()
            if not written_freelist:
                print("Error writing freelist")
                return None

            written_meta = self.write_meta(self.meta)
            if not written_meta:
                print("Error writing meta")
                return None
            
    def get_page_size(self):
        try:
            page_size = os.sysconf(os.sysconf_names['SC_PAGESIZE'])
            return page_size
        except AttributeError:
            print("Could not determine the page size")
            return None

    # Create a new instance of class with a given file path and return the file and its
    # pagesize into the contructor __init__ of dal
    @classmethod
    def new_dal(cls, path, page_size):
        try:
            file = open(path, 'r+b')
        except FileNotFoundError:
            file = open(path, 'w+b')
        free_page_list = FreePageList()
        meta = Meta.new_empty_meta()
        return cls(file, page_size, free_page_list, meta)

    def close(self):
        if self.file is not None:
            try:
                self.file.close()
            except Exception as e:
                print(f"Couldn't close file: {e}")
                return False
            self.file = None
        return True

    # Allocating an empty page
    def allocate_empty_page(self):
        data = bytearray(self.page_size)
        return Page(None, data)

    def get_next_page(self):
        return self.free_page_list.get_next_page()

    # Read the page_num from the file. Each page is of page_size hence to access the page_num
    # page we have to move the file pointer by page_size * page_num bytes
    # Example: page_num = 3 and page_size = 1024B. Indexing of page number is done from zero
    # hence 3rd page is 2nd page which is 2*1024 = 2048B. Hence the 3rd page(2nd Page) starts
    # at 2048 byte position
    def read_page(self, page_num):
        try:
            # Offset of page_num * page_size from the beginning of the file. This will make
            # the file pointer, point towards the starting of the page_num required
            offset = page_num * self.page_size
            self.file.seek(offset)
            # Read the page_size byte of data of the page_number as the file_pointer now
            # points towrds the page_number byte
            data = self.file.read(self.page_size)
            return Page(page_num, data)
        except Exception as e:
            print(f"Error reading page: {e}")
            return None

    # Similar process as of read_page()
    def write_page(self, Page):
        try:
            page_num = Page.num
            data = Page.data
            # Move the file pointer to the required page_number
            offset = page_num * self.page_size
            self.file.seek(offset)
            # Write the Page data to the file
            self.file.write(data)
            # Commit the chnages to the disk
            self.file.flush()
        except Exception as e:
            print(f"Error writing page: {e}")
            return False
        return True

    def write_meta(self, meta):
        p = self.allocate_empty_page()
        p.num = META_PAGE_NUM
        p.data = meta.serialize()

        if not self.write_page(p):
            return None
        return p

    def read_meta(self):
        p = self.read_page(META_PAGE_NUM)
        if p is None:
            return None
        print("pnum", p.num)
        meta = Meta.new_empty_meta()
        meta.deserialize(p.data)
        return meta
    
    def write_freelist(self):
        try:
            p = self.allocate_empty_page()
            meta_t = self.read_meta()
            print("pnum", meta_t.freelist_page)
            p.num = meta_t.freelist_page
            p.data = self.free_page_list.serialize()
            # print(p.num)
            if not self.write_page(p):
                raise Exception("Failed to write freelist page to database")

            self.meta.freelist_page = p.num
            return p
        except Exception as e:
            print(f"Error writing freelist: {e}")
            return None

    def read_freelist(self):
        p = self.read_page(self.meta.freelist_page)
        if p is None:
            return None
        self.free_page_list.deserialize(p.data)
        return self.free_page_list
