import os

class Dal:
    def __init__(self, file=None):
        self.file = file
    
    @classmethod
    def new_dal(cls, path):
        try:
            file = open(path, 'a+b')
            return cls(file)
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
    
