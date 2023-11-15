import requests
import re
# import time
from bs4 import BeautifulSoup


bible_books_translation = {
    'Mateo': 'Matthew',
    'Marcos': 'Mark',
    'Lucas': 'Luke',
    'Juan': 'John',
    'Mga Gawa': 'Acts',
    'Roma': 'Romans',
    'Corinto': 'Corinthians',
    'Galata': 'Galatians',
    'Efeso': 'Ephesians',
    'Filipos': 'Philippians',
    'Coloso': 'Colossians',
    'Tesalonica': 'Thessalonians',
    'Timoteo': 'Timothy',
    'Tito': 'Titus',
    'Filemon': 'Philemon',
    'Hebreo': 'Hebrews',
    'Santiago': 'James',
    'Pedro': 'Peter',
    'Judas': 'Jude',
    'Pahayag': 'Revelation'
}

url_list = []


def remove_non_alphabet_chars(input_text):
    # regular expression to remove non-alphabetic characters, excluding 
whitespaces
    cleaned_text = re.sub(r'[^a-zA-Z\s]', '', input_text)
    return cleaned_text


def scrape(url):
    response = requests.get(url)

    # time.sleep(1)

    soup = BeautifulSoup(response.content, "html.parser")

    bible_text_elements = soup.findAll("span")

    full_text = ""

    for section in bible_text_elements:
        bible_text = section.get_text(strip=True)
        cleaned_text = remove_non_alphabet_chars(bible_text)
        if (not cleaned_text.endswith("Loading") and not 
cleaned_text.endswith("Learn More") and
                not cleaned_text.endswith("Chapter") and not 
cleaned_text.endswith("Films")):
            full_text += " "
            full_text += cleaned_text

    print(url)
    chapter_el = soup.find("h1", class_="book-chapter-text")
    chapter_name = chapter_el.get_text()
    chapter_tokens = chapter_name.split()

    file_name = ""
    for t in chapter_tokens:
        if t in bible_books_translation:
            file_name += bible_books_translation[t]
        else:
            file_name += t

    output_file_path = "texts/" + file_name + ".txt"

    print(file_name)

    # Write the cleaned text to the new text file
    with open(output_file_path, "w", encoding="utf-8") as output_file:
        output_file.write(full_text)


def main(url_l):
    for url in url_l:
        scrape(url)
        # time.sleep(1)


main(url_list)

