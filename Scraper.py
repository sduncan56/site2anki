import urllib.request
from bs4 import BeautifulSoup

from CardGenerator import CardGenerator


class Scraper:
    def __init__(self):
        pass

    def parseInnerUrl(self, url):
        with urllib.request.urlopen(url) as url:
            page = url.read()
            soup = BeautifulSoup(page, 'html.parser')

            header = soup.find('div', attrs={'class': 'panel-heading'}).find('h1').string
            answersCollection = soup.find('div', attrs={'class': 'articleContent'}).children

            answer = ""

            correctAnswer = soup.find('a', attrs={'title': 'Toggle display correct answer'})
            if correctAnswer:
                js = correctAnswer['href']
                index = int(js.find('getElementById') + 16)
                index2 = int(js[index:].find("')"))
                answerTag = js[index:index + index2]
                answer = soup.find('li', attrs={'id': answerTag}).text
            else:
                answer = soup.find('div', attrs={'class': 'articleContent'}).find('div').text


            return (header, answer)

    def scrape(self, baseurl, pageurl):
        cardGenerator = CardGenerator('C# Trivia')
        with urllib.request.urlopen(baseurl+pageurl) as url:
            page = url.read()
            soup = BeautifulSoup(page, 'html.parser')
            innerUrlsHtml = soup.findAll('div', attrs={'class': 'list-group-item-spacer'})

            for innerUrlHtml in innerUrlsHtml:
                innerUrl = innerUrlHtml.find('a')['href']
                data = self.parseInnerUrl(baseurl+innerUrl)
                cardGenerator.add_card(data[0], data[1])

        cardGenerator.output_deck('deck.apkg')






if __name__ == "__main__":
    scraper = Scraper()
    scraper.scrape("http://www.dotnetfunda.com", "/interviews/exclusive/cat/6/csharp")
