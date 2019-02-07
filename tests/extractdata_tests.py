import unittest
from findText import extractdata


class TestGettingPageContent(unittest.TestCase):
    def testWorkingPage(self):
        code, content = extractdata.get_page_content('https://www.google.com/')
        self.assertEqual(code, 200)
        self.assertTrue(len(content) > 0)

    def testURLError(self):
        code, content = extractdata.get_page_content('http://www.google.p/')
        self.assertEqual(-1, code)

    def testHTTPError(self):
        code, content = extractdata.get_page_content('https://flippingbook.com/404')
        self.assertEqual(404, code)


if __name__ == '__main__':
    unittest.main()
