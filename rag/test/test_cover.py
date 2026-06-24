import os

import cover
import requests
def test_conver():
    cover.conver()  # 现在能找到了

def test_requests():
    # response = requests.get("http://localhost:8000/api/v2/auth/identity")
    # print(response.json())  # 应该返回你截图中的 JSON

    print("http_proxy:", os.environ.get('http_proxy'))
    print("no_proxy:", os.environ.get('no_proxy'))

    proxies = {"http": None, "https": None}

    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36",
        "Accept": "application/json",

    }
    resp = requests.get("http://localhost:8000/api/v2/auth/identity", headers=headers,    proxies=proxies)
    print(resp.status_code)
    print(resp.text)
    print(resp.headers)