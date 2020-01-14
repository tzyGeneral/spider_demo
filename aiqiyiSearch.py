import time
import requests
from lxml import etree
from pyquery import PyQuery as pq


class AutoIqiyi():
    def __init__(self):
        self.header = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36'
        }
        self.baseUrl = 'http://so.iqiyi.com/so/q_'

    def getHtml(self, url):
        time.sleep(0.5)
        try:
            response = requests.get(url, headers=self.header)
            if response.status_code == 200:
                return response.text
        except Exception:
            return None

    def getUrl(self, word):
        return self.baseUrl + (str(word))

    def getMsg(self, html):
        page = etree.HTML(html)
        doc = pq(html)
        dic = {}

        poster = doc('body > div.page-search > div.container.clearfix > div.search_result_main > div > div.mod_search_result > div > ul > li:nth-child(1) > a > img').attr('src')
        poster = str(poster).replace('//', 'https://')
        name = doc('body > div.page-search > div.container.clearfix > div.search_result_main > div > div.mod_search_result > div > ul > li:nth-child(1) > a > img').attr('title')
        url1 = page.xpath('//a[@class="album_link"]/@href')
        url = list(url1)[0]

        dic['title'] = name
        dic['poster'] = poster
        dic['url'] = url

        return dic

    def workOn(self,word):

        url = self.getUrl(str(word))
        # print(url)
        time.sleep(0.5)
        pageData = self.getHtml(url)
        if not pageData:
            pass
        self.getMsg(pageData)


if __name__ == "__main__":
    m = AutoIqiyi()
    m.workOn('西游记')