import unittest
from findText import extractdata


class TestGettingPageContent(unittest.TestCase):
    def test_working_page(self):
        code, content = extractdata.get_page_content('https://www.google.com/')
        self.assertEqual(code, 200)
        self.assertTrue(len(content) > 0)

    def test_url_error(self):
        code, content = extractdata.get_page_content('http://www.google.p/')
        self.assertEqual(code, -1)

    def test_http_error(self):
        code, content = extractdata.get_page_content('https://flippingbook.com/404')
        self.assertEqual(code, 404)


class TextExtractingDataFromList(unittest.TestCase):
    def test_working_page(self):
        # get page content
        code, content = extractdata.get_page_content('https://www.tekstowo.pl/piosenki_artysty,kult.html')
        self.assertEqual(code, 200)
        bs = extractdata.text_to_bs(content)
        # verify
        self.assertEqual(extractdata.verify_list(bs), True)
        # get pages
        pg_num = extractdata.get_num_pages(bs)
        self.assertEqual(pg_num, 8)

    def test_not_working_page(self):
        # get page content
        code, content = extractdata.get_page_content('https://www.tekstowo.pl/piosenki_artysty,klt.html')
        self.assertEqual(code, 200)
        bs = extractdata.text_to_bs(content)
        # verify
        self.assertEqual(extractdata.verify_list(bs), False)
        # get pages
        pg_num = extractdata.get_num_pages(bs)
        self.assertEqual(pg_num, 0)

    def test_extracting_data(self):
        code, content = extractdata.get_page_content('https://www.tekstowo.pl/piosenki_artysty,zabili_mi_zolwia.html')
        code, test_content = extractdata.get_author_page("Zabili Mi Żółwia")
        self.assertEqual(content, test_content)
        link, title = extractdata.get_list_of_similar_authors("kult")[0]
        self.assertEqual(title, "Kult")
        self.assertEqual(link, "/piosenki_artysty,kult.html")

    def test_normalization(self):
        self.assertEqual(extractdata.normalize_text("żółć"), "zolc")
        self.assertEqual(extractdata.normalize_text("AĄĘ"), "AAE")
        print(extractdata.get_song_text('/piosenka,kult,bliskie_spotkanie_3_stopnia.html'))


if __name__ == '__main__':
    unittest.main()
