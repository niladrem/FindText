from bs4 import BeautifulSoup
import urllib.request
import re


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
    return int(pages[-1].get_text()) if pages else 1


def verify_list(bs):
    song_list = bs.find(class_='ranking-lista')
    return not song_list.get_text().strip() == ''


def extract_list(bs):
    song_list = bs.find('div', class_='content').find_all(class_='title')
    out = []
    for song_line in song_list:
        link = re.search('href="([^"]+)"', str(song_line)).group(1)
        title = re.search('title="([^"]+)"', str(song_line)).group(1)
        out.append((link, title))
    return out


def get_list_of_similar_authors(author):
    normalized_author = normalize_text(author)
    normalized_author = re.sub('[ ]+', '+', normalized_author)
    url = "https://www.tekstowo.pl/szukaj,wykonawca," + normalized_author.lower() + ",tytul,.html"
    code, page = get_page_content(url)
    page_bs = text_to_bs(page)
    return extract_list(page_bs)


def get_author_page(author):
    normalized_author = normalize_text(author)
    normalized_author = re.sub('[^A-Za-z0-9 _()-]+', '', normalized_author)  # remove special characters
    normalized_author = re.sub('[ ()-]+', '_', normalized_author)  # remove spaces
    url = "https://www.tekstowo.pl/piosenki_artysty," + normalized_author.lower() + ".html"
    code, page = get_page_content(url)
    return text_to_bs(page)


def get_list_of_given_author_and_page_num(author, page):
    url = "https://www.tekstowo.pl/piosenki_artysty," + author + ",alfabetycznie,strona," + str(page) + ".html"
    code, text = get_page_content(url)
    bs = text_to_bs(text)
    return extract_list(bs)


def get_whole_songs_list(author):
    normalized_author = normalize_text(author)
    normalized_author = re.sub('[^A-Za-z0-9 _()-]+', '', normalized_author)  # remove special characters
    normalized_author = re.sub('[ ()-]+', '_', normalized_author)  # remove spaces
    first_page_bs = get_author_page(author)

    pg_num = get_num_pages(first_page_bs)
    songs_list = []
    for i in range(1, pg_num + 1):
        songs_list.extend(get_list_of_given_author_and_page_num(normalized_author, i))

    return songs_list


def get_song_text(link):
    url = "https://www.tekstowo.pl" + link
    code, text = get_page_content(url)
    bs = text_to_bs(text)
    song_text = bs.find('div', class_='song-text')
    return re.sub('Poznaj historię zmian tego tekstu', '', song_text.get_text())


def text_contains(link, phrase):
    text = get_song_text(link)
    return phrase.lower() in text.lower()


def normalize_text(input_text):
    intab = 'ęóąśłżźćńĘÓĄŚŁŻŹĆŃ'
    outtab = 'eoaslzzcnEOASLZZCN'
    translator = str.maketrans(intab, outtab)
    return input_text.translate(translator)
