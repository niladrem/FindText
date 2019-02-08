from bs4 import BeautifulSoup
import urllib.request


def get_tag_content(text, tag, classes='', ids=''):
    soup = BeautifulSoup(text, 'html.parser')
    tag_content = soup.find_all(tag, class_=classes, ids=ids)
    return str(tag_content[0]) if tag_content else ''

def read_text(text):
    soup = BeautifulSoup(text, 'html.parser')
    return soup.get_text()

def get_page_content(url):
    """Return tuple with HTTP status code and page content"""
    try:
        response = urllib.request.urlopen(url)
        return response.code, response.read()
    except urllib.error.HTTPError as e:
        return e.code, e.reason
    except urllib.error.URLError as e:
        return -1, e.reason
    except:
        return -1, "Unexpected error"


def get_list_with_class(text, class_name):
    pass

