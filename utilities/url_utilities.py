import re
import string
import sys
from bs4 import BeautifulSoup
from urllib.request import urlopen


def load_urls_from_file(file_path: str):
    try:
        with open(file=file_path, mode="r+") as file_in:
            content = file_in.readline()
            return content
    except FileNotFoundError:
        print(f"[Error]: The file {file_path} could not be found.")
        exit(2)
    except IOError as err:
        print(f"[Error]: Cause: {err}.")
        exit(3)
    except BaseException:
        print(f"[Error]: Unexpected error: {sys.exc_info()}")
        exit(4)


def load_page(url: str):
    response = urlopen(url)
    html = response.read().decode("utf-8")
    return html


def scrape_page(page_contents: str):
    chicken_noodle = BeautifulSoup(page_contents, "html5lib")

    for script in chicken_noodle(["script", "style"]):
        script.extract()

    text = chicken_noodle.get_text()
    lines = (line.strip() for line in text.splitlines())
    chunks = (phrase.strip() for line in lines for phrase in line.split("  "))

    text = ' '.join(chunk for chunk in chunks if chunk)
    plain_text = ''.join(filter(lambda x: x in string.printable, text))

    clean_words = []

    words = plain_text.split(" ")
    for word in words:
        clean = True

        # no punctuation
        for punctuation_mark in string.punctuation:
            if punctuation_mark in word:
                clean = False

                # no numbers
            if any(char.isdigit() for char in word):
                clean = False

                # at least two characters but no more than 10
            if len(word) < 2 or len(word) > 10:
                clean = False

            if not re.match(r'^\w+$', word):
                clean = False

            if clean:
                try:
                    clean_words.append(word.lower())
                except UnicodeEncodeError:
                    print(".")

    return clean_words
