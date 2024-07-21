class PageNumber(int):
    pass
PAGE_NUM_SIZE = 8

class FreePageList:
    def __init__(self):
        self.max_page = PageNumber(1)
        self.released_pages = []

    def get_next_page(self):
        if self.released_pages:
            return self.released_pages.pop()
        else:
            self.max_page += 1
            return self.max_page

    def release_page(self, page_id):
        self.released_pages.append(page_id)

    def serialize(self):
        buf = bytearray(PAGE_NUM_SIZE + 2 +
                        len(self.released_pages) * PAGE_NUM_SIZE)
        pos = 0

        buf[pos:pos +
            2] = self.max_page.to_bytes(PAGE_NUM_SIZE, byteorder='little')
        pos += 2

        buf[pos:pos + 2] = len(self.released_pages).to_bytes(2,
                                                             byteorder='little')
        pos += 2

        for page in self.released_pages:
            buf[pos:pos +
                PAGE_NUM_SIZE] = page.to_bytes(PAGE_NUM_SIZE, byteorder='little')
            pos += PAGE_NUM_SIZE

        return buf

    def deserialize(self, buf):
        pos = 0
        self.max_page = PageNumber(int.from_bytes(
            buf[pos:2], byteorder='little'))
        pos += 2

        released_pages_count = int.from_bytes(
            buf[pos:pos + 2], byteorder='little')
        pos += 2

        self.released_pages = [
            PageNumber(int.from_bytes(
                buf[pos + i * PAGE_NUM_SIZE:pos + (i + 1) * PAGE_NUM_SIZE], byteorder='little'))
            for i in range(released_pages_count)
        ]
