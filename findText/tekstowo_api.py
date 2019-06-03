import extractdata
import sys
import re


def search_artist(name, print_num=False):
    """Return list of artists"""
    list_of_artists = extractdata.get_list_of_similar_authors(name)
    if len(list_of_artists) == 0:
        print("Artist not found")
        return -1
    for num, artist in enumerate(list_of_artists):
        print("{}{}".format(("[{}] ".format(num) if print_num else ""), artist[1]))
    if print_num:
        while True:
            try:
                num = int(input("Enter number of artist: "))
                artist_name = re.search("artysty,([^.]+).html", list_of_artists[num][0]).group(1)
                return artist_name
            except ValueError:
                print("Please enter the number")
            except IndexError:
                print("Index out of range")


def search():
    """Return names of songs of given artist with given phrase"""
    artist_name = input("Enter artist name: ")
    artist_page = extractdata.get_author_page(artist_name)
    if not extractdata.verify_list(artist_page):
        print("Artist not found. Choose one below:")
        artist_name = search_artist(artist_name, True)
    phrase = input("Enter phrase: ")
    songs_list = extractdata.get_whole_songs_list(artist_name)
    for song in songs_list:
        if extractdata.text_contains(song[0], phrase):
            print(song[1])


def print_help():
    print("help - print help")
    print("search_artist - search artist with given name")
    print("search - search text")
    print("exit - close app\n")


if __name__ == '__main__':
    print("Welcome in FindText App")
    print("Print 'help' to get help")
    while True:
        user_input = input("Enter command:\n").strip()
        if user_input == 'help':
            print_help()
        elif user_input == 'exit':
            sys.exit()
        elif user_input == 'search':
            search()
        elif user_input == 'search_artist':
            artist_name = input("Enter artist name: ")
            search_artist(artist_name)
        else:
            print("Unknown command")
