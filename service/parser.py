import requests

from bs4 import BeautifulSoup

r = requests.get('https://cvillecatcare.com/veterinary-topics/101-amazing-cat-facts-fun-trivia-about-your-feline-friend/')

soup = BeautifulSoup(r.content, 'html.parser')

# print(soup.prettify())
texts = soup.find_all('li')

for li in texts:
    print('"' + li.get_text() + '",')
