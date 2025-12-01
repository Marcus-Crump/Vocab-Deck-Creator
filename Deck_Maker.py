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
        pass


if __name__ == "__main__":
    main()
