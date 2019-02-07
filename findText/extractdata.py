from bs4 import BeautifulSoup
import urllib.request


def get_tag_content(text, tag, attr=""):
    pass


def get_page_content(url):
    """Return tuple with HTTP status code and page content"""
    try:
        response = urllib.request.urlopen(url)
        return (response.code, response.read())
    except urllib.error.HTTPError as e:
        return (e.code, e.reason)
    except urllib.error.URLError as e:
        return (-1, e.reason)


def get_list_with_class(text, class_name):
    pass

