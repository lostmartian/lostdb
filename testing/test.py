import os
import tempfile
import shutil
from utils.dal import Dal
from utils.meta import Meta


def create_test_database(db_path):
    # Initialize a new database
    dal = Dal(db_path)
    if not dal:
        raise Exception("Failed to initialize database")
    return dal


def test_database_initialization():
    # Create a temporary directory

        # Path to the temporary database file
        db_path = os.path.join("test.db")

        # Create a new database instance
        dal = create_test_database(db_path)

        try:
            # Ensure the database file exists
            assert os.path.exists(db_path), "Database file does not exist"

            # Check if metadata and freelist are initialized properly
            assert dal.read_meta().freelist_page is not None, "Metadata freelist page is not initialized"
            assert dal.free_page_list.max_page == 0, "Freelist max page is not initialized"

        finally:
            # Close the database
            dal.close()


def test_metadata_operations():
    # Create a temporary directory
    with tempfile.TemporaryDirectory() as temp_dir:
        # Path to the temporary database file
        db_path = os.path.join(temp_dir, "test.db")

        # Create a new database instance
        dal = create_test_database(db_path)

        try:
            # Create a meta object with a freelist_page set to 5 for testing
            meta = Meta(freelist_page=5)

            # Write the meta to the database
            written_meta = dal.write_meta(meta)
            assert written_meta is not None, "Failed to write meta to the database"

            # Read the meta from the database
            read_meta = dal.read_meta()
            assert read_meta is not None, "Failed to read meta from the database"
            assert read_meta.freelist_page == meta.freelist_page, f"Expected freelist page {
                meta.freelist_page}, got {read_meta.freelist_page}"

        finally:
            # Close the database
            dal.close()


def test_freelist_operations():
    # Create a temporary directory
    with tempfile.TemporaryDirectory() as temp_dir:
        # Path to the temporary database file
        db_path = os.path.join(temp_dir, "test.db")

        # Create a new database instance
        dal = create_test_database(db_path)

        try:
            # Write the freelist to the database
            written_freelist = dal.write_freelist()
            assert written_freelist is not None, "Failed to write freelist to the database"

            # Read the freelist from the database
            read_freelist = dal.read_freelist()
            assert read_freelist is not None, "Failed to read freelist from the database"
            assert read_freelist.max_page == dal.free_page_list.max_page, f"Expected freelist max page {
                dal.free_page_list.max_page}, got {read_freelist.max_page}"

        finally:
            # Close the database
            dal.close()


def test_database_operations():
    # Create a temporary directory
    with tempfile.TemporaryDirectory() as temp_dir:
        # Path to the temporary database file
        db_path = os.path.join(temp_dir, "test.db")

        # Create a new database instance
        dal = create_test_database(db_path)

        try:
            # Perform various database operations
            page_size = dal.page_size

            # Allocate and write pages
            page1 = dal.allocate_empty_page()
            page1.data = bytearray(page_size)
            page1.num = dal.get_next_page()

            written = dal.write_page(page1)
            assert written, "Failed to write page to database"

            # Read the page back
            read_page1 = dal.read_page(page1.num)
            assert read_page1 is not None, "Failed to read page from database"
            assert read_page1.num == page1.num, f"Expected page number {
                page1.num}, got {read_page1.num}"

        finally:
            # Close the database
            dal.close()


if __name__ == "__main__":
    test_database_initialization()
    test_metadata_operations()
    test_freelist_operations()
    test_database_operations()
    print("All tests passed!")
