import unittest
import os
import sys
import s3_file_manager

class s3_file_manager_tests(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        self.s3_manager = s3_file_manager.s3_file_manager()
        self.s3_manager.set_bucket_name("matt-maatubang-insight-la-test")

    def test_get_file(self):
        hello_file = self.s3_manager.get_file("read_test.txt")
        with open(hello_file, 'r') as my_file:
            hello_str = str(my_file.read())
        self.assertEqual(hello_str, "Hello world!")

    def test_put_file(self):
        self.assertTrue(self.s3_manager.put_file('put_test.txt'))

if __name__ == '__main__':
    unittest.main()
