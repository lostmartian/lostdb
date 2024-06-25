import os

# A subclass for int
# This means that the int type and PageNumber type is now same just that we have 
# a explicit int type called PageNumber to denote PageNumber
class PageNumber(int):
    pass

class Page:
    def __init__(self, num, data):
        # num is of type PageNumber. It is an instance of PageNumber
        self.num = PageNumber(num)
        self.data = data

class Dal:
    def __init__(self, file, pagesize):
        self.file = file
        self.pagesize = pagesize
    
    # Create a new instance of class with a given file path and 
    # return the file and its pagesize into the contructor __init__ of dal
    @classmethod
    def new_dal(cls, path, pagesize):
        try:
            file = open(path, 'a+b')
            return cls(file, pagesize)
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


if __name__ == "__main__":
    d = Dal.new_dal("example.txt")
    if d:
        # Perform file operations here if needed
        success = d.close()
        if success:
            print("File closed successfully.")
        else:
            print("Failed to close the file.")
    
