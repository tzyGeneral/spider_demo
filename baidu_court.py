import requests


class Court:
    """
    获取百度法院所有的3500个法院信息
    """
    def __init__(self):
        self.baseUrl = 'http://baike.baidu.com/cms/s/court/court-data.json?t=20200615'
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36",
        }
        self.data = []

    def _requests(self):
        response = requests.get(self.baseUrl, headers=self.headers)
        data = response.json()
        for one in data:
            if one == "size":
                break
            for n in data[one]['list']:
                court = n['courtName']
                self.data.append(court)

        print(self.data)
        print(len(self.data))
        return self.data


if __name__ == "__main__":
    court = Court()
    court._requests()
