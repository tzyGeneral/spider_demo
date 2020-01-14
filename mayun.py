import time
import requests
from pyquery import PyQuery as pq
from lxml import etree
import regex as re


class MayunSearch():
    '''
    爬取码云的关于java的代码段
    '''
    def __init__(self, fileName):
        self.url = 'https://gitee.com/search?page='
        self.header = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate, compress',
            'Accept-Language': 'en-us;q=0.5,en;q=0.3',
            'Cache-Control': 'max-age=0',
            'Connection': 'keep-alive',
            'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:22.0) Gecko/20100101 Firefox/22.0'
            }
        self.params = '&q=java&type=code&utf8=%E2%9C%93'
        self.data = []
        self.fileName = fileName
        self.txt = open(self.fileName,'w', encoding='utf-8')

    def getUrl(self, pageNum):
        return self.url + str(pageNum) + self.params

    def getHtml(self, url):
        time.sleep(0.5)
        try:
            response = requests.get(url, headers=self.header,timeout=5)
            if response.status_code == 200:
                return response.text
        except Exception:
            return None

    def getMsgTwo(self, html,url):
        doc = pq(html)
        title = doc('#tree-content-holder > div.cp-title').text()
        dataurl = '+'.join(title.split(' '))
        data = str(url) + '/raw?blob_name=' + str(dataurl)
        cede = self.getHtml(data)
        if cede is not None:
            self.txt.write(cede)
        print(cede)

    def getMsg(self, html):
        page = etree.HTML(html)
        # url1 = page.xpath('//div[@class="item-header"]//div[@class="metas"]/a[@class="item"]/@href')
        url1 = page.xpath('//div[@class="item-header"]//div[@class="metas"]/a[1]/@href')
        for url in url1:
            newUrl = 'https://gitee.com'+url
            # print(newUrl)
            # time.sleep(1)
            page = self.getHtml(newUrl)
            if not page:
                continue
            self.getMsgTwo(page,newUrl)
        doc = pq(html)

    def workOn(self):
        for pageNum in range(1,100):
            url = self.getUrl(pageNum)
            print(url)
            pageData = self.getHtml(url)
            if not pageData:
                continue
            page = self.getMsg(pageData)
            # page
        self.txt.close()


def dataprocess(file_path, newfile_path):
    pattern = re.compile('//|/\*|\*/|\s\*')
    p = re.compile('\S')
    z = re.compile('[\u4e00-\u9fa5]+')
    with open(file_path,'r', encoding='utf-8') as f:
        with open(newfile_path, 'w', encoding='utf-8') as nf:
            f = f.readlines()
            for line in f:
                w=line.strip('\n')
                if len(w) > 1 and  not w.startswith('/*') and  not w.startswith('//') and not w.startswith('*') and not w.endswith('*/'):
                    name = pattern.findall(w)
                    n=p.findall(w)
                    zw=z.findall(w)
                    if name==[] and n!=[] and zw==[]:
                        print(w)
                        nf.writelines(w+'\n')


if __name__ == "__main__":
    m = MayunSearch('Code4.txt')
    m.workOn()

    dataprocess('./Code4.txt', './newCode4.txt')