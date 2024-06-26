from dal import Dal, PageNumber, get_page_size

if __name__ == "__main__":
    dal = Dal.new_dal("database.db", get_page_size())
    print(f"DAL initialized with file: {
          dal.file.name}, page size: {dal.page_size}")

    # Allocate new pages
    # Output: Allocated page: 2
    print(f"Allocated page: {dal.free_page_list.get_next_page()}")
    # Output: Allocated page: 3
    print(f"Allocated page: {dal.free_page_list.get_next_page()}")

    # Release a page
    dal.free_page_list.release_page(PageNumber(2))
    print(f"Released page 2")  # Output: Released page 2

    # Allocate a page again, should reuse released page
    # Output: Allocated page: 2
    print(f"Allocated page: {dal.free_page_list.get_next_page()}")

    # Close the DAL
    dal.close()
