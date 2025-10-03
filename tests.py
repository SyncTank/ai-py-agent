# tests.py

import unittest
from functions.get_files_info import *
from functions.get_file_content import *

class Test_get_file_content(unittest.TestCase):
    def test_get_file_base(self) :
        asset_info = get_file_content("calculator", "main.py")
        print(asset_info)

    def test_get_file_lorsum(self) :
        asset_info = get_file_content("calculator", "lorem.txt")
        print(asset_info)

    def test_get_file_pkg(self) :
        asset_info = get_file_content("calculator", "pkg/calulator.py")
        print(asset_info)

    def test_get_file_bin(self) :
        asset_info = get_file_content("calculator", "/bin/cat")
        print(asset_info)

    def test_get_file_miss(self) :
        asset_info = get_file_content("calculator", "pkg/does_not_exist.py")
        print(asset_info)

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
