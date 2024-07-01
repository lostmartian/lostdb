from utils.dal import Dal, get_page_size
from utils.meta import Meta


def main():
    page_size = get_page_size()
    if not page_size:
        print("Failed to get page size")
        return

    dal = Dal.new_dal("db.db", page_size)

    # Create a meta object with a freelist_page set to 1 for example
    meta = Meta(freelist_page=5)

    # Write the meta to the database
    written_page = dal.write_meta(meta)
    if written_page:
        print(f"Meta written to page number: {written_page.num}")
    else:
        print("Failed to write meta to the database")

    # Read the meta from the database
    read_meta = dal.read_meta()
    if read_meta:
        print(f"Freelist page number read from meta: {
              read_meta.freelist_page}")
    else:
        print("Failed to read meta from the database")

    # Close the database
    dal.close()


if __name__ == "__main__":
    main()
