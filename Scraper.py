import urllib.request
import urllib.error
from bs4 import BeautifulSoup

from CardGenerator import CardGenerator


class Scraper:
    def __init__(self):
        self.pageCount = 1
        self.ansCount = 0

    def parseInnerUrl(self, url):
        with urllib.request.urlopen(url) as url:
            page = url.read()
            soup = BeautifulSoup(page, 'html.parser')

            header = soup.find('div', attrs={'class': 'panel-heading'}).find('h1').text
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

            # This should not happen, but on the off chance, this will stop it from crashing when generating cards
            if header is None:
                header = ""
            if answer is None:
                answer = ""

            return header, answer

    def scrape(self, base_url, page_url, pagenum_url, card_generator):
        try:
            with urllib.request.urlopen(base_url + page_url + pagenum_url) as url:
                page = url.read()
                soup = BeautifulSoup(page, 'html.parser')
                inner_urls_html = soup.findAll('div', attrs={'class': 'list-group-item-spacer'})
                if not inner_urls_html:
                    return

                for innerUrlHtml in inner_urls_html:
                    inner_url = innerUrlHtml.find('a')['href']
                    data = self.parseInnerUrl(base_url + inner_url)
                    card_generator.add_card(data[0], data[1])

            self.pageCount += 1
            self.ansCount += 20

            self.scrape(base_url, page_url, '/{0}/{1}'.format(self.ansCount, self.pageCount), card_generator)
        except urllib.error.HTTPError as err:
            if err.code == 404:
                return


if __name__ == "__main__":
    cardGenerator = CardGenerator('C# Trivia')
    scraper = Scraper()
    scraper.scrape("http://www.dotnetfunda.com", "/interviews/exclusive/cat/6/csharp", "", cardGenerator)
    cardGenerator.output_deck('deck.apkg')
