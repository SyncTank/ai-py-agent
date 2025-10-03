# tests.py

import unittest
from functions.get_files_info import *


class Test_get_files_info(unittest.TestCase):
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
