from bs4 import BeautifulSoup
import urllib.request


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


def text_to_bs(text):
    return BeautifulSoup(text, 'html.parser')


def get_num_pages(bs):
    pages = bs.find_all(class_='page')
    return int(pages[-1].get_text()) if pages else 0


def verify_list(bs):
    song_list = bs.find(class_='ranking-lista')
    return not song_list.get_text().strip() == ''


def get_songs_list(bs):
    pass


def get_list_of_similar_authors(author):
    pass


def get_author_page(author):
    pass


def get_list_of_given_author_and_page_num(author, page):
    url = "https://www.tekstowo.pl/piosenki_artysty," + author + ",alfabetycznie,strona," + str(page) + ".html"
    text = get_page_content(url)
    bs = text_to_bs(text)
    return get_songs_list(bs)


def get_whole_songs_list(author):
    first_page = get_author_page(author)
    first_page_bs = text_to_bs(first_page)

    pg_num = get_num_pages(first_page_bs)
    songs_list = []
    for i in range(1, pg_num + 1):
        songs_list.extend(get_list_of_given_author_and_page_num(author, i))

    return songs_list
