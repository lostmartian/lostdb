from utils.dal import Dal, get_page_size

def main():
    dal = Dal.new_dal("database.db", get_page_size())

    npage = dal.allocate_empty_page()
    npage.num = dal.get_next_page()

    # Allot the first 5 data bytes for "Hello"
    npage.data[:5] = b"Hello"

    # Commit the changes
    success = dal.write_page(npage)

    npage = dal.allocate_empty_page()
    npage.num = dal.get_next_page()

    # Allot the first 5 data bytes for "Hello"
    npage.data[:5] = b"Hello"

    # Commit the changes
    success = dal.write_page(npage)

    if success:
        print("Page commited successfully")
    else:
        print("Error")
    dal.close()

if __name__== '__main__':
    main()