META_PAGE_NUM = 0
PAGE_NUM_SIZE = 8


class Meta:
    def __init__(self, freelist_page=None):
        self.freelist_page = freelist_page

    def serialize(self):
        if self.freelist_page is None:
            raise ValueError("freelist_page cannot be None")
        return self.freelist_page.to_bytes(PAGE_NUM_SIZE, byteorder='little')

    def deserialize(self, buf):
        # if len(buf) < PAGE_NUM_SIZE:
        #     raise ValueError(f"Buffer size must be at least {
        #                      PAGE_NUM_SIZE} bytes")
        self.freelist_page = int.from_bytes(
            buf[:PAGE_NUM_SIZE], byteorder='little')
