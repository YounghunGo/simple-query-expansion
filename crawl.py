from bs4 import BeautifulSoup
import urllib.request
import requests
import re
import selenium
from selenium import webdriver
from selenium.webdriver import ActionChains

from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
import pandas as pd
import datetime
import os
import getpass
import json
import time
from elasticsearch import Elasticsearch
from elasticsearch import helpers

def insertData(es, index_name, jsonObj):
    es.index(index=index_name, doc_type='json', body=jsonObj)

def make_index(es, index_name):
    if es.indices.exists(index=index_name):
        print(es.indices.delete(index=index_name))
        print("index exists")
        exit()
    else:
        print(es.indices.create(index=index_name))

URL = 'https://ieeexplore.ieee.org/document/'

#driver = webdriver.Chrome(executable_path='chromedriver.exe')
#driver.implicitly_wait(15)

es = Elasticsearch("127.0.0.1:9200")
es.info()

#인덱스 생성
index_name = 'paper1'
#make_index(es, index_name)
cnt = 0

for i in range(25000, 100000):
    response = requests.get(URL + str(i))
    
    if response.status_code == 404:
        continue
    
    html = response.text
    soup = BeautifulSoup(html, 'html.parser')
    
    abstract = soup.select('script')
    
    #print(len(abstract))
    if len(abstract) < 11:
        continue
    script = abstract[11].get_text()
    text = script.split('xplGlobal.document.metadata=')[1]
    text = text.split('"};')[0] + '"}'

    #print(text)
    jsonObj = json.loads(text)

    #문서 추가
    insertData(es, index_name, jsonObj)
    cnt = cnt + 1
    print(cnt, "번째 문서", i, "번 문서")
    #time.sleep(0.5)


