import urllib.request
from urllib.error import HTTPError
from bs4 import BeautifulSoup
from PIL import Image
import boto3
import os

ACCESS_KEY = 'AWS_ACCESS_KEY'
SECRET_KEY = 'AWS_SECRET_KEY'
BUCKET_NAME = 'BUCKET_NAME'
web_url = "http://www.whichfaceisreal.com"
s3 = boto3.client('s3')

for i in range(200000,300000):
    xtest = i
    with urllib.request.urlopen(web_url) as response:
        html = response.read()
        soup = BeautifulSoup(html, 'html.parser')
        left_div = soup.find_all("img")
        for j in left_div:
            new_url = web_url
            new_url += "/%s" % j.get("src")
            file_src = j.get("src")
            if not file_src.find("fakeimages") == -1:
                fileoname = j.get("src").replace("fakeimages/","")
                urllib.request.urlretrieve(new_url,"gen_photo/%s" % fileoname)
                image = Image.open("gen_photo/%s" % fileoname)
                resize_image = image.resize((500,500))
                resize_image.save("gen_photo/%s" % fileoname, "jpeg", quality=95)
                # s3에 저장
                s3.upload_file("gen_photo/%s" % fileoname, BUCKET_NAME, "gen_photo/%s" % fileoname)
                # 서버에서 파일 삭제 조치
                os.remove("gen_photo/%s" % fileoname)
