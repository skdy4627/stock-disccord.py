import requests
import time
from bs4 import BeautifulSoup
from pymongo import MongoClient

conn = MongoClient('mongodb://localhost:27017/')
jusik = conn.jusik
jusik_jusiks = jusik.jusiks

def jusik_re():
    #주식 코드
    arr = ['005930', '015760', '034220', '000660', '006400', '000270', '005380', '030200', '017670', '032640', '011200', '035720', '035420', '068270', '207940', '000720', '105560', '055550']

    # 주식 가격 불러오고 저장하는 코드
    for i in arr:
        url = f"https://finance.naver.com/item/main.nhn?code={i}"
        result = requests.get(url)
        bs_obj = BeautifulSoup(result.content, "html.parser")
        no_today = bs_obj.find("p", {"class": "no_today"}) # 태그 p, 속성값 no_today 찾기
        blind = no_today.find("span", {"class": "blind"}) # 태그 span, 속성값 blind 찾기
        now_price = blind.text
        jusik_jusiks.update_one({"code": i}, {"$set": {"price": now_price}})
        print(now_price)
    print("============")

while True:
        jusik_re()
        # sleep값 조절해서 주식 가격 갱신 시간 조절 가능
        time.sleep(878)
