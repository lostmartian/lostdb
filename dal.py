import os

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
        self.num = PageNumber(num)
        self.data = data

class Dal:
    def __init__(self, file, page_size):
        self.file = file
        self.page_size = page_size
    
    # Create a new instance of class with a given file path and return the file and its 
    # pagesize into the contructor __init__ of dal
    @classmethod
    def new_dal(cls, path, page_size):
        try:
            file = open(path, 'a+b')
            return cls(file, page_size)
        except Exception as e:
            print(f"Error opening file: {e}")
            return None
    
    def close(self):
        if self.file is not None:
            try:
                self.file.close()
            except Exception as e:
                print(f"Couldn't close file: {e}")
                return False
            self.file = None
        return True
    
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
    def write(self, Page):
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




if __name__ == "__main__":
    # d = Dal.new_dal("example.txt")
    # if d:
    #     # Perform file operations here if needed
    #     success = d.close()
    #     if success:
    #         print("File closed successfully.")
    #     else:
    #         print("Failed to close the file.")
    print(get_page_size())
    
