META_PAGE_NUM = 0
PAGE_NUM_SIZE = 8

class Meta:
    def __init__(self, freelist_page = None):
        self.freelist_page = freelist_page

    @staticmethod
    def new_empty_meta():
        return Meta()
    
    # Convert Meta object to bytes
    def serialize(self):
        if self.freelist_page is None:
            raise ValueError("freelist_page cannot be none")
        # Convert the freelist_page number to byte size array
        # Little endian byte orfer(LSB first) is preferred as it is compatible with common 
        # x86 and ARM architectures with respect to performance
        buf = self.freelist_page.to_bytes(PAGE_NUM_SIZE, byteorder='little', signed='False')
        return buf
    
    def deserialize(self, buf):
        if len(buf) != PAGE_NUM_SIZE:
            raise ValueError("Size of the buffer must be of {PAGE_NUM_SIZE} size")
        self.freelist_page = int.from_bytes(buf, byteorder='little', signed='False')

    
# Example
# meta = Meta(freelist_page=51)
# serialized_data = meta.serialize()
# print("Serialized data:", serialized_data)

# meta2 = Meta()
# meta2.deserialize(serialized_data)
# print("Deserialized freelist_page:", meta2.freelist_page)

