import requests as r
from bs4 import BeautifulSoup as bs
import os, platform

def clear():
    if platform.system() != 'Windows':
        os.system('clear -force')
    else:
        os.system('CLS')

def get_soup(link):
    page = r.get(link)
    soup = bs(page.text,'html.parser')
    page.close()
    return soup

def get_kanji_and_kana(soup):
    term_block = soup.find("div", class_="concept_light clearfix")
    term = term_block.find("span", class_="text").text.strip()
    hurigana_list =  []
    hurigana = []

    for c in term_block.find("span", class_="furigana").find_all("span"):
        c = c.text.strip()
        if c != "":
            hurigana_list.append(c)

    hurigana_list.reverse()

    for c in term:
        if ord(c) < 12354 or ord(c) > 12447:
            hurigana.append(hurigana_list.pop())
        else:
            hurigana.append(c)

    return term, "".join(hurigana)

def write_kanji_line(file, soup):
    kanji, kana = get_kanji_and_kana(soup)
    file.write(f"{kanji},{kana}\n")

def write_vocab_line(file, soup):
    term_block = soup.find("div", class_="concept_light clearfix")
    term = term_block.find("span", class_="text").text.strip()
    defn_list = term_block.find_all("div", class_="meaning-definition zero-padding")
    defn = ""
    for i in defn_list:
        item = i.find("span", class_="meaning-meaning").text.strip()
        if ord(item[0]) <= 255:
            defn += item + "; "
    file.write(f"{term}, {defn}\n")

def open_ended():
    name = input("Enter name of deck:")
    while name == "":
        clear()
        name = input("Please input valid name:")
    clear()
    term = input("Term:").strip()

    if term == "": return

    kanji = open(f"{name}-漢字.csv",'a')
    vocab = open(f"{name}-単語.csv", 'a')

    while term != "":
        soup = get_soup(f"https://jisho.org/search/{term}")
        write_kanji_line(kanji, soup)
        write_vocab_line(vocab, soup)
        clear()
        term = input("Term:").strip()

    kanji.close()
    vocab.close()

def deck_from_list(file):
    name = input("Enter name of deck:")

    while name == "":
        clear()
        name = input("Please input valid name:")

    clear()

    kanji = open(f"{name}-漢字.csv")
    vocab = open(f"{name}-単語.csv")

    with open(file,'r') as lst:
        for l in lst:
            soup = get_soup(f"https://jisho.org/search/{l}")
            write_kanji_line(kanji,soup)
            write_vocab_line(vocab,soup)

    kanji.close()
    vocab.close()

def main():
    clear()
    clear()
    choice = input("Open ended feed 1\nFeed list 2\n")
    while choice != "1" and choice != "2" and choice != "１" and choice != "２":
        clear()
        print("Please make a valid selection")
        choice = input("Open ended feed 1\nFeed list 2\n")
    
    if choice == "1" or choice == "１":
        open_ended()
    else:
        dne = True
        while dne:
            try:
                file = input("File path: ")
                deck_from_list(file)
                dne = False
            except FileNotFoundError:
                print("File not found, please try again...")


if __name__ == "__main__":
    try:
        main()
    except (r.exceptions.ConnectionError, r.exceptions.ConnectTimeout) as e:
        print(f"Connection could not be established ({e})")