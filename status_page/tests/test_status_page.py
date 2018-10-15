import unittest

import status_page


class Status_pageTestCase(unittest.TestCase):

    def setUp(self):
        self.app = status_page.app.test_client()

    def test_index(self):
        rv = self.app.get('/')
        self.assertIn('Welcome to status_page', rv.data.decode())


if __name__ == '__main__':
    unittest.main()
