# -*- coding: utf-8 -*-
import multiprocessing
import random
import time
import json
import requests
from requests import RequestException

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver import ActionChains
from multiprocessing.dummy import Pool
from config import ACCOUNTURL, PROCESSNUM


class TaoBao:

    # 初始化
    def __init__(self, username, passwd):
        self.url = "https://login.taobao.com/member/login.jhtml"
        self.keyword_list = ["外套", "男鞋", "运动鞋", "T恤"]
        self.username = username
        self.passwd = passwd

        options = webdriver.ChromeOptions()
        # 不加载图片,加快访问速度（不加载图片会导致一些bug）
        # options.add_experimental_option("prefs", {"profile.managed_default_content_settings.images": 2})
        options.add_experimental_option('excludeSwitches', ['enable-automation'])
        options.add_argument('--disable-blink-features=AutomationControlled')
        options.add_experimental_option('useAutomationExtension', False)
        options.add_argument('user-agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36"') #
        options.add_argument('--no-sandbox')  # 解决DevToolsActivePort文件不存在的报错
        options.add_argument('--disable-gpu')  # 谷歌文档提到需要加上这个属性来规避bug
        self.js_str = "Object.defineProperty(navigator,'webdriver',{get: ()=> false,});"

        self.browser = webdriver.Chrome(options=options)
        self.browser.maximize_window()
        self.wait = WebDriverWait(self.browser, 10)

    def run(self, id=0):
        login_error = ''
        try:
            login_error = self.login()
            time.sleep(random.randint(1, 2))
            # 点击淘宝首页
            nav_button = self.wait.until(EC.presence_of_element_located((By.XPATH, '//div[@class="site-nav-menu-hd"]/a[@href="//www.taobao.com/"]')))
            nav_button.click()
            time.sleep(random.randint(1, 3))

            # 下拉鼠标
            self.scroll_down()

            # 点击分类
            # types_button = self.browser.find_element_by_xpath('//ul[@class="service-bd"]/li[@data-groupid="{}"]/a'.format(random.randint(1, 10)))
            # self.browser.execute_script("arguments[0].click();", types_button)
            # window_list = self.browser.window_handles  # 获取窗口列表
            # self.browser.switch_to.window(window_list[1])  # 将browser的指针转移到新打开的商品详情页面
            # 检查是否有滑块验证
            # self.slide_block_thr()

            # 点击推荐商品
            is_check = False
            for _ in range(10):
                # 随机点击首页的一件商品
                self.click_goods()

                # 检查是否有滑块验证
                check = self.slide_block_two()
                if check == "error":  # 说明点击当商品不存在，则继续点击
                    self.browser.close()
                    window_list = self.browser.window_handles
                    self.browser.switch_to.window(window_list[0])
                    continue
                elif check == True:  # 说明没有出现滑块
                    self.scroll_down(num=2)
                    is_check = False
                    break
                else:  # 说明有出现滑块
                    is_check = True
                    break
            time.sleep(40)

            dictCookies = self.browser.get_cookies()
            cookiestr = json.dumps(dictCookies, ensure_ascii=False)
            # cookie = [item["name"] + "=" + item["value"] for item in dictCookies]
            # cookiestr = '; '.join(item for item in cookie)

        except Exception as e:
            if not login_error: login_error = "未知错误，请查看日志"
            cookiestr = ''
            is_check = True
        finally:
            time.sleep(10)
            self.close()

        return {"id": id, "cookie": cookiestr, "is_check": is_check, "login_error": login_error}

    def login(self):
        self.browser.get(self.url)
        # 等待 账号登陆 出现
        password_login = self.browser.find_element_by_xpath('//form[@id="login-form"]//input[@name="fm-login-id"]')
        password_login.click()
        time.sleep(1)
        password_login.send_keys(self.username)

        # 等待 密码 出现
        pwd = self.browser.find_element_by_xpath('//form[@id="login-form"]//input[@name="fm-login-password"]')
        pwd.click()
        pwd.send_keys(self.passwd)

        # 判断是否有登陆滑块验证码
        try:
            time.sleep(1)
            slide = self.browser.find_element_by_xpath('//button[@class="fm-button fm-submit password-login fm-button-disabled"]')
        except Exception as e:
            print(e)
        else: self.slide_block(slide)

        # 等待 登陆按钮 出现
        submit = self.browser.find_element_by_xpath('//button[@class="fm-button fm-submit password-login"]')
        submit.click()
        time.sleep(2)
        if self.browser.title == "登录-身份验证":
            return "需要手机号短信认证"
        try:
            error_msg = self.browser.find_element_by_xpath('//div[@class="login-error-msg"]')
        except Exception as e:
            print(e)
            return "正常登陆"
        else: return error_msg.text

    def click_goods(self):
        """随机点击首页的一件商品"""
        goods = self.browser.find_element_by_xpath('//div[@aria-posinset="{}"]//div[@class="img-wrapper"]/img'.format(random.randint(10, 60)))
        self.browser.execute_script("arguments[0].click();", goods)
        window_list = self.browser.window_handles  # 获取窗口列表
        self.browser.switch_to.window(window_list[1])  # 将browser的指针转移到新打开的商品详情页面

    def slide_block(self, slide):
        """滑动滑块"""
        time.sleep(3)
        # 找到滑块
        # 检查是否出现了滑动验证码
        try:
            slider = self.browser.find_element_by_xpath('//span[contains(@class, "btn_slide")]')
            slider.click()
            ActionChains(self.browser).click_and_hold(slider).perform()
            ActionChains(self.browser).move_by_offset(xoffset=258, yoffset=0).perform()
            ActionChains(self.browser).pause(0.5).release().perform()
        except Exception as e:
            print(e)
            pass

    def slide_block_two(self):
        """页面内滑块"""
        print(self.browser.title)
        if self.browser.title == "click.mz.simba.taobao.com":
            time.sleep(2)
            return "error"
        try:
            iframe = self.wait.until(EC.presence_of_element_located((By.XPATH, '//iframe[@id="baxia-dialog-content" or @id="sufei-dialog-content"]')))
        except Exception as e:
            # 没有则说明没有出现滑块验证
            print("没有滑块验证")
            return True
        else:
            return False

    def slide_block_thr(self):
        """滑块验证"""
        time.sleep(random.randint(1,2))
        if self.browser.title == "验证码拦截":
            try:
                warring = self.browser.find_element_by_xpath('//div[@class="warnning-text"]')

                slider = self.wait.until(EC.presence_of_element_located((By.XPATH, '//span[contains(@class, "btn_slide")]')))
                ActionChains(self.browser).click_and_hold(slider).perform()
                track = self.get_track(distanc=265)
                for x in track:
                    ActionChains(self.browser).move_by_offset(xoffset=x, yoffset=0).perform()
                time.sleep(random.randint(2,4))
                ActionChains(self.browser).pause(0).release().perform()
            except Exception as e:
                print("错误信息", e)
                pass


    def scroll_down(self, num=9):
        """鼠标下拉"""
        y_plus = 450
        y = 0
        for i in range(num):
            y += y_plus
            self.browser.execute_script("window.scroll(0,{})".format(y))
            time.sleep(0.4)

    def get_track(self, distanc):
        """模拟轨迹"""
        # 移动轨迹
        track = []
        # 当前位移
        current = 0
        # 减速阈值
        mid = distanc * 3 / 5
        # 计算间隔
        t = random.randint(4, 8) / 10
        # 初速度
        v = 0

        while current < distanc:
            if current < mid:
                # 加速度为正2
                a = 6
            else:
                # 加速度为负3
                a = -4
            v0 = v
            # 当前速度v = v0+at
            v = v0 + a * t
            # 移动距离x=v0*t+1/2*a*t*t
            move = v0 * t + 1 / 2 * a * t * t
            # 当前位移
            current += move
            # 加入轨迹
            track.append(round(move))
        return track

    def close(self):
        """关闭浏览器"""
        self.browser.quit()


def multi_browser(args: dict):
    username = args["username"]
    passwd = args["passwd"]
    tool = TaoBao(username, passwd)
    cookies = tool.run(id=args["id"])
    return cookies


if __name__ == "__main__":

    # 获取所有淘宝账户信息
    try:
        response = requests.get(ACCOUNTURL).json()
    except RequestException:
        response = {}
        print("接口请求失败")
    user_passwd_list = response.get("data", [])
    user_passwd_list = user_passwd_list[:34]

    pool = Pool(PROCESSNUM)
    result = pool.map(multi_browser, user_passwd_list)
    pool.close()
    pool.join()

    # 将最后的结果更新同步到数据库
    result = [x for x in result if x]
    try:
        response = requests.put(ACCOUNTURL,
                                data={"data": json.dumps(result, ensure_ascii=False)}).json()
    except RequestException:
        response = {}
        print("情况上传失败")
    if response["code"] == 200:
        print("上传结果成功")
