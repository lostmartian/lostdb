from utils.dal import Dal


def main():
    # Initialize or open the database
    db_path = "db.db"
    dal = Dal(db_path)

    try:
        # Create a new page
        p = dal.allocate_empty_page()
        p.num = dal.get_next_page()
        p.data = bytearray("data", 'utf-8')

        # Write the page to the database
        dal.write_page(p)

        # Write the freelist to the database
        dal.write_freelist()

        # Close the database
        dal.close()

        # Re-open the database to simulate restart
        dal = Dal(db_path)

        # Create and write another page without overwriting previous pages
        p = dal.allocate_empty_page()
        p.num = dal.get_next_page()
        p.data = bytearray("data2", 'utf-8')
        dal.write_page(p)

        # Release a page to update the freelist
        page_num = dal.get_next_page()
        dal.free_page_list.release_page(page_num)

        # Write the updated freelist to the database
        dal.write_freelist()

    finally:
        # Close the database
        dal.close()


if __name__ == "__main__":
    main()
