class PageNumber(int):
    pass

class FreePageList:
    def __init__(self):
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


