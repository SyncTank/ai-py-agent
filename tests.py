# tests.py

import unittest
from functions.get_files_info import *
from functions.get_file_content import *
from functions.write_file import *

class Test_write_file(unittest.TestCase):
    def test_write_file_base(self):
        print(f"\nTEST 1\n")
        assert_info = write_file("calculator", "lorem.txt", "wait, this isn't lorem ipsum")
        print(f"{assert_info}\n")

    def test_write_file_pkg(self):
        print(f"\nTEST 2\n")
        assert_info = write_file("calculator", "pkg/morelorem.txt", "lorem ipsum dolor sit amet")
        print(f"{assert_info}\n")

    def test_write_file_temp(self):
        print(f"\nTEST 3\n")
        assert_info = write_file("calculator", "/tmp/temp.txt", "this should not be allowed")
        print(f"{assert_info}\n")

class Test_get_file_content():
    def test_get_file_base(self):
        print(f"\nTEST 1\n")
        asset_info = print(get_file_content("calculator", "main.py"))
        print(f"{asset_info}\n")

    def test_get_file_lorsum(self) :
        print(f"\nTEST 2\n")
        asset_info = get_file_content("calculator", "lorem.txt")
        print(f"{asset_info}\n")

    def test_get_file_pkg(self) :
        print(f"\nTEST 3\n")
        asset_info = print(get_file_content("calculator", "pkg/calculator.py"))
        print(f"{asset_info}\n")

    def test_get_file_bin(self) :
        print(f"\nTEST 4\n")
        asset_info = print(get_file_content("calculator", "/bin/cat"))
        print(f"{asset_info}\n")

    def test_get_file_miss(self) :
        print(f"\nTEST 5\n")
        asset_info = print(get_file_content("calculator", "pkg/does_not_exist.py"))
        print(f"{asset_info}\n")

class Test_get_files_info():
    def test_get_file_base(self) :
        asset_info = get_files_info("calculator", ".")
        print(asset_info)

    def test_get_file_pkg(self) :
        asset_info = get_files_info("calculator", "pkg")
        print(asset_info)

    def test_get_file_bin(self) :
        asset_info = get_files_info("calculator", "/bin")
        print(asset_info)

    def test_get_file_miss(self) :
        asset_info = get_files_info("calculator", "../")
        print(asset_info)

if __name__ == "__main__":
    unittest.main()
