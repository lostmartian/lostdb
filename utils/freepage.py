

class PageNumber(int):
    pass

class FreePageList:
    def __init__(self):

        self.PAGE_NUM_SIZE = 8
        # Page 0 stores the metadata of the database.
        self.max_page = PageNumber(0)
        # Stores the list of pages that were previously used but are now free
        self.released_pages = []

    def get_next_page(self):
        # Allocates a new page number. If there are any released pages, reuses one of them.
        # otherwise, increments max_page to allocate a new page.
        if self.released_pages:
            # Use the page that was recently freed
            page_id = self.released_pages.pop()
            return page_id
        else:
            # if the released pages are empty then start from 1st page as 0th page is kept
            # for metadata
            self.max_page += 1
            return self.max_page

    def release_page(self, pageid):
        self.released_pages.append(pageid)
    
    def serialize(self):
        buf = bytearray()

        # Serialize max_page
        buf.extend(self.max_page.to_bytes(2, byteorder='little', signed=False))

        # Serialize the count of released pages
        buf.extend(len(self.released_pages).to_bytes(
            2, byteorder='little', signed=False))

        # Serialize each released page
        for page in self.released_pages:
            buf.extend(page.to_bytes(self.PAGE_NUM_SIZE,
                       byteorder='little', signed=False))

        return bytes(buf)
    
    def deserialize(self, buf):
        pos = 0

        # Deserialize max_page
        self.max_page = PageNumber(int.from_bytes(
            buf[pos:pos+2], byteorder='little', signed=False))
        pos += 2

        # Deserialize the count of released pages
        released_pages_count = int.from_bytes(
            buf[pos:pos+2], byteorder='little', signed=False)
        pos += 2

        # Deserialize each released page
        self.released_pages = []
        for _ in range(released_pages_count):
            page = PageNumber(int.from_bytes(
                buf[pos:pos+self.PAGE_NUM_SIZE], byteorder='little', signed=False))
            self.released_pages.append(page)
            pos += self.PAGE_NUM_SIZE


# if __name__ == "__main__":
#     freelist = FreePage()

#     # Allocate new pages
#     # Output: Allocated page: 2
#     print(f"Allocated page: {freelist.get_next_page()}")
#     # Output: Allocated page: 3
#     print(f"Allocated page: {freelist.get_next_page()}")

#     # Release a page
#     freelist.release_page(PageNumber(2))
#     print(f"Released page 2")  # Output: Released page 2

#     # Allocate a page again, should reuse released page
#     # Output: Allocated page: 2
#     print(f"Allocated page: {freelist.get_next_page()}")

# if __name__ == "__main__":
#     # Create an instance of FreePageList and allocate some pages
#     freelist = FreePageList()
#     page1 = freelist.get_next_page()
#     page2 = freelist.get_next_page()
#     freelist.release_page(page1)

#     # Serialize the freelist
#     serialized_data = freelist.serialize()
#     print("Serialized data:", serialized_data)

#     # Create a new FreePageList instance and deserialize the data into it
#     new_freelist = FreePageList()
#     new_freelist.deserialize(serialized_data)

#     # Check if the new freelist has the same state as the original one
#     print("Original max_page:", freelist.max_page)
#     print("Deserialized max_page:", new_freelist.max_page)
#     print("Original released_pages:", freelist.released_pages)
#     print("Deserialized released_pages:", new_freelist.released_pages)

#     assert freelist.max_page == new_freelist.max_page, "Max page does not match"
#     assert freelist.released_pages == new_freelist.released_pages, "Released pages do not match"

#     print("Serialization and deserialization test passed!")
