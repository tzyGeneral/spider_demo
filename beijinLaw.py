from pyquery import PyQuery as pq
import requests
from urllib import parse
from lxml import etree
import re
import time,random


class RipperVip():
    def __init__(self):
        self.header = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate, compress',
            'Accept-Language': 'en-us;q=0.5,en;q=0.3',
            'Cache-Control': 'max-age=0',
            'Connection': 'close',
            'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:22.0) Gecko/20100101 Firefox/22.0'
        }
        self.baseUrl = 'http://www.bjcourt.gov.cn/cpws/index.htm'
        # 翻页
        # http://www.bjcourt.gov.cn/cpws/index.htm?page=3

    def getHtml(self, url):
        time.sleep(0.5)
        try:
            response = requests.get(url, headers=self.header)
            if response.status_code == 200:
                return response.text
        except Exception:
            return None

    def filter_html(self,html):
        """
        :param html: html
        :return: 返回去掉html的纯净文本
        """
        dr = re.compile(r'<[^>]+>', re.S)
        dd = dr.sub('', html).strip()
        return dd

    def getDetailMsg(self,data):

        doc = pq(data)
        text = doc('#cc').text()
        text = str(text)
        text = self.filter_html(text)
        data = text.encode().decode('unicode_escape')
        print(data)

    def getMsg(self, html):
        page = etree.HTML(html)

        urlList = page.xpath('//li[@class="refushCpws"]//a/@href')
        for url in urlList:
            newUrl = 'http://www.bjcourt.gov.cn' + url
            print(newUrl)
            data = self.getHtml(newUrl)
            if not data:
                continue
            self.getDetailMsg(data)

    def workOn(self):
        time.sleep(0.5)
        pageData = self.getHtml(self.baseUrl)
        if not pageData:
            pass
        self.getMsg(pageData)


if __name__ == "__main__":
    m = RipperVip()
    m.workOn()