import requests
from bs4 import BeautifulSoup

url = "https://loigiaihay.com/giai-bai-3-trang-6-sach-bai-tap-toan-6-canh-dieu-a95992.html"

response = requests.get(url)
soup = BeautifulSoup(response.content, "html.parser")
tags_p = soup.find_all("p")

i=float("inf")
for index, p in enumerate(tags_p):
    text = p.get_text(strip=True)
    if "Lời giải chi tiết" == text:
        i=index
    if "Lời giải hay" == text:
        i=99999
    if index>i:
        print(text)

