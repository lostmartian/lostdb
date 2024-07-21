from utils.dal import Dal


def main():
    page_size = Dal.get_page_size()
    if not page_size:
        print("Failed to get page size")
        return

    # Initialize DB
    dal = Dal.new_dal("db.db", page_size)

    # Create a new page
    p = dal.allocate_empty_page()
    p.num = dal.freelist.get_next_page()
    p.data[:4] = b"data"

    # Commit it
    dal.write_page(p)
    dal.write_freelist()

    # Close the db
    dal.close()

    # We expect the freelist state was saved, so we write to page number 3 and not overwrite the one at number 2
    dal = Dal.new_dal("db.db", page_size)
    p = dal.allocate_empty_page()
    p.num = dal.freelist.get_next_page()
    p.data[:5] = b"data2"
    dal.write_page(p)

    # Create a page and free it so the released pages will be updated
    page_num = dal.freelist.get_next_page()
    dal.freelist.release_page(page_num)

    # Commit it
    dal.write_freelist()
    dal.close()


if __name__ == "__main__":
    main()
