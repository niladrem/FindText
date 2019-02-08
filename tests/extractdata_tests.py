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


class TestGettingTagContent(unittest.TestCase):
    @classmethod
    def getTestText(self):
        return "<html><div>1</div><div id=\"2\">2</div><p id=\"2\">3</p><p id=\"4\">4</p><div class=\"5 7\">5</div>\
        <p class=\"5\" id=\"2\">6</p><div class=\"6\"><span id=\"2\">7</span></div></html>"

    def testNormalTag(self):
        text = self.getTestText()
        self.assertEqual('<div>1</div>', extractdata.get_tag_content(text, 'div'))
        self.assertEqual('<p id="2">3</p>', extractdata.get_tag_content(text, 'p'))
        self.assertEqual('<span id="2">7</span>', extractdata.get_tag_content(text, 'span'))

    def testClassTag(self):
        text = self.getTestText()
        self.assertEqual('<p class="5" id="2">6</p>', extractdata.get_tag_content(text, 'p', classes='5'))
        self.assertEqual('<div class="6"><span id="2">7</span></div>',
                         extractdata.get_tag_content(text, 'div', classes='6'))
        self.assertEqual('<div class="5 7">5</div>', extractdata.get_tag_content(text, '', classes='5'))
        self.assertEqual('<div class="5 7">5</div>', extractdata.get_tag_content(text, '', classes='7'))

    def testIdTag(self):
        text = self.getTestText()
        self.assertEqual('<p id="4">4</p>', extractdata.get_tag_content(text, 'p', ids='4'))
        self.assertEqual('<div id="2">2</div>', extractdata.get_tag_content(text, '', ids='2'))
        self.assertEqual('<p class="5" id="2">6</p>', extractdata.get_tag_content(text, 'p', ids='2'))

    def testReadText(self):
        text = self.getTestText()
        self.assertEqual('1', extractdata.read_text(extractdata.get_tag_content(text, 'div')))
        self.assertEqual('7', extractdata.read_text(extractdata.get_tag_content(text, 'div', classes='6')))


if __name__ == '__main__':
    unittest.main()
