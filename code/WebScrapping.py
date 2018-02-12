from bs4 import BeautifulSoup
import requests
from pprint import pprint
from urllib.parse import quote
import re
import googleimagesearch
from Logger import lggr

class MyInstantsWebScrapping:
    def __init__(self):
        self.linkBasis = 'https://www.myinstants.com'
        self.searchLinkBasis = self.linkBasis + '/search/?name='

    def search(self, completeLink, maxresults):
        lggr.logPrint('>>> Searching sounds at: ' + completeLink)
        page = requests.get(completeLink)
        soup = BeautifulSoup(page.content, 'html.parser')
        instants = soup.find_all('div', class_='instant')

        rsp = []
        cont = 0
        for ins in instants:
            if cont == maxresults:
                return rsp
            name = ins.find('a').get_text()
            link = self.linkBasis + ins.find('div', class_='small-button')['onmousedown'].replace('play(\'',
                                                                                                  '').replace('\')', '')

            rsp.append({'name': name, 'link': link})

            cont += 1
        return rsp


    def getUrlForKeyword(self, keyword):
        keyword = quote(keyword, safe='')
        completeLink = '{}{}'.format(self.searchLinkBasis, keyword)
        return completeLink

    def getUrlForCounty(self, countryId):
        completeLink = '{}{}{}'.format(self.linkBasis, '/index/', countryId)
        return completeLink

    def getTopByCountry(self, countryId, maxresults=3):
        completeLink = self.getUrlForCounty(countryId)
        return self.search(completeLink, maxresults)

    def searchByKeyWord(self, keyword, maxresults=3):
        completeLink = self.getUrlForKeyword(keyword)
        return self.search(completeLink, maxresults)


class DogPileImagesWebScrapping():
    def searchFirst(self, query):
        query = quote(querySimplify(query), safe='')
        link = 'http://www.dogpile.com/dogpilecontrol/search/images?q={}'.format(query)
        lggr.logPrint('>>> Searching images at: {}'.format(link))
        page = requests.get(link)
        soup = BeautifulSoup(page.content, 'html.parser')

        img = soup.find('img', class_='resultThumbnail')
        if img:
            return img['src']
        else:
            return None

#'https://yandex.com/images/search?text={}' (do not allow webscrapping)
#'https://www.google.com.br/search?source=imghp&sout=1&q={}&tbm=isch' (changes itself to the classic google images version)

class GoogleImagesWebScrapping:
    def searchFirst(self, query):
        aux = query
        query = quote(querySimplify(query), safe='')
        link = 'https://www.google.com.br/search?source=imghp&sout=1&q={}&tbm=isch'.format(query)

        lggr.logPrint('>>> Searching images at: {}'.format(link))
        page = requests.get(link)
        soup = BeautifulSoup(page.content, 'html.parser')

        imgs = soup.find_all('img')



        if imgs:
            for img in imgs:
                if img['src'].startswith('https://'):
                    return img['src']
        else:
            return None

class generalImageScrapper:
    def __init__(self, searchStr, imgTagClass):
        self.site = searchStr
        self.tagClass = imgTagClass
        pass

    def searchFirst(self, query):
        query = quote(querySimplify(query), safe='')
        link = self.site.format(query)

        lggr.logPrint('>>> Searching images at: {}'.format(link))
        page = requests.get(link)
        soup = BeautifulSoup(page.content, 'html.parser')

        img = soup.find('img', class_=self.tagClass)
        if img:
            return img['src']
        else:
            return None


def querySimplify(query):
    query = re.sub('[^A-Za-z0-9 À-úçÇ]+', '', query)
    return query


