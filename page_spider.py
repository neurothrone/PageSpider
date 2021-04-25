import os
import argparse

from utilities import database_utilities, url_utilities


def main(database: str, url_list_file: str):
    big_word_list = []

    print(f"Working with: {database}")
    print(f"By scanning: {url_list_file}")

    # Url code
    urls = url_utilities.load_urls_from_file(url_list_file)
    for url in urls:
        print(f"Reading {url}")
        page_content = url_utilities.load_page(url=url)
        words = url_utilities.scrape_page(page_contents=page_content)
        big_word_list.extend(words)

    # Database code
    os.chdir(os.path.dirname(__file__))
    path = os.path.join(os.getcwd(), "words.db")
    database_utilities.create_database(database_path=path)
    database_utilities.save_words_to_database(database_path=path,
                                              words_list=big_word_list)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-db", "--database", help="SQLite File Name")
    parser.add_argument("-i", "--input", help="File containing urls to read")
    args = parser.parse_args()
    database_file = args.database
    input_file = args.input
    main(database=database_file, url_list_file=input_file)
