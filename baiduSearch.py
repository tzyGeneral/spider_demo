from selenium import webdriver
from selenium.webdriver.common.keys import Keys


class BaiduSearch():
    '''
    获取百度搜索词的第一页的标题内容  以手机页面进行采集
    '''
    def __init__(self, keyword):
        self.chrome_driver = r'D:\chromedriver_win32\chromedriver.exe'
        self.mobile_emulation = {'deviceName': 'iPhone 6'}
        self.options = webdriver.ChromeOptions()
        self.options.add_experimental_option("mobileEmulation", self.mobile_emulation)
        self.browser = webdriver.Chrome(executable_path=self.chrome_driver, chrome_options=self.options)
        self.keyword = keyword
        self.data = []

    def workOn(self):
        self.browser.get("https://www.baidu.com")
        self.browser.find_element_by_css_selector('#index-kw').send_keys(self.keyword)
        self.browser.find_element_by_css_selector('#index-kw').send_keys(Keys.ENTER)

        for num in range(1,21):
            try:
                # a = self.browser.find_element_by_css_selector('#results > div:nth-child('+str(num)+') > div.c-result-content > article > header > div > a > h3 > span')
                a = self.browser.find_element_by_css_selector('#results > div:nth-child('+str(num)+') > div.c-result-content > article > section > div:nth-child(3) > div > div > span')
                #                                              #results > div:nth-child(2) > div.c-result-content > article > section > div:nth-child(3) > div > div > span
            except:
                continue
            self.data.append(a.text)
            print(a.text)

        pages = self.browser.find_element_by_css_selector('#page-controller > div > a')
        self.browser.execute_script("arguments[0].click();", pages)
        for num in range(1,21):
            try:
                b = self.browser.find_element_by_css_selector('#results > div:nth-child('+str(num)+') > div.c-result-content > article > section > div:nth-child(3) > div > div > span')
            except:
                continue
            self.data.append(b.text)
            print(b.text)
        self.data = list(set(self.data))
        data = []
        for url in self.data:
            if 'www' in url:
                data.append(url)
        print(data)
        return self.data


if __name__ == "__main__":
    m = BaiduSearch('姚明')
    m.workOn()