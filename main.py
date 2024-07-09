import os
from utils.dal import Dal
from utils.meta import Meta
from utils.freepage import FreePageList


def test_dal():
    # Initialize a new database (or use an existing one)
    db_path = "test.db"
    dal = Dal(db_path)

    if not dal:
        print("Failed to initialize database")
        return

    try:
        # Create a meta object with a freelist_page set to 5 for testing
        meta = Meta(freelist_page=5)

        # Write the meta to the database
        written_meta = dal.write_meta(meta)
        if written_meta:
            print(f"Meta written to page number: {written_meta.num}")
        else:
            print("Failed to write meta to the database")

        # Read the meta from the database
        read_meta = dal.read_meta()
        if read_meta:
            print(f"Freelist page number read from meta: {
                  read_meta.freelist_page}")
        else:
            print("Failed to read meta from the database")

        # Write the freelist to the database
        written_freelist = dal.write_freelist()
        if written_freelist:
            print(f"Freelist written to page number: {written_freelist.num}")
        else:
            print("Failed to write freelist to the database")

        # Read the freelist from the database
        read_freelist = dal.read_freelist()
        if read_freelist:
            print(f"Freelist read from page number: {read_freelist.max_page}")
        else:
            print("Failed to read freelist from the database")

    finally:
        dal.close()
        print("Database closed")

def main():
    test_dal()
    # page_size = get_page_size()
    # if not page_size:
    #     print("Failed to get page size")
    #     return

    # dal = Dal.new_dal("db.db", page_size)

    # # Create a meta object with a freelist_page set to 1 for example
    # meta = Meta(freelist_page=5)

    # # Write the meta to the database
    # written_page = dal.write_meta(meta)
    # if written_page:
    #     print(f"Meta written to page number: {written_page.num}")
    # else:
    #     print("Failed to write meta to the database")

    # # Read the meta from the database
    # read_meta = dal.read_meta()
    # if read_meta:
    #     print(f"Freelist page number read from meta: {
    #           read_meta.freelist_page}")
    # else:
    #     print("Failed to read meta from the database")

    # # Close the database
    # dal.close()


if __name__ == "__main__":
    main()
