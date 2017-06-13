import requests
from bs4 import BeautifulSoup
import pandas as pd

##送出Http請求，把請求回來的結果打包成re物件
re = requests.get("https://topet.net/vet_recommand.htm")

##設定re物件的讀取編碼(可以直接看網頁上的head的部分，找到編碼)
re.encoding = "big5"

##叫出re物件的text屬性，也就會是html原始檔
html_text = re.text

##用BeautifulSoup解析HTML文件(跑出的警告不用理他)
soup = BeautifulSoup(html_text,'lxml')

##用裡面的find_all方法，找出所有有<a>標籤的部分
a_list = soup.find_all("a")

##找出第二個到第十八個
href_dict = {}  ##用字典屬性可以儲存，ket以及value
for i in range(2,19):
    href_dict[a_list[i].string] = 'https://topet.net/' + a_list[i]['href']


def AddDownToAbove(df_hospital):
    addIndex =  df_hospital[pd.isnull(df_hospital[0])].index

    index = 100
    duplicateLi = []
    for i in addIndex:
        if i == index+1:
            duplicateLi.append(i)
        index = i
    ##當沒有連號時就回回傳空list，h3g6dk3u3uwl4jt joc6fm0
    if (duplicateLi==[]):
        return False
    
    duplicateLi.sort(reverse=True)
    for i in duplicateLi:
        row = df_hospital.xs(i-1)
        row[1] = df_hospital[1].xs(i-1)+", "+df_hospital[1].xs(i)
        df_hospital.drop(i, inplace=True)
    
    return True


def ConverTableToDict(path, name):
    df_hospital = pd.read_html(path, encoding='big5')[0]

    df_hospital.drop(0, inplace=True)
    if len(df_hospital.columns) >2:
        df_hospital.drop(df_hospital.columns[2:],axis=1,inplace=True)

    dropTableIndexs = df_hospital[pd.isnull(df_hospital[1])].index
    df_hospital.drop(dropTableIndexs,inplace = True)

    while(AddDownToAbove(df_hospital)):
        print(True)

    addIndex =  df_hospital[pd.isnull(df_hospital[0])].index
    for i in addIndex:
        row = df_hospital.xs(i-1)
        row[1] = df_hospital[1].xs(i-1)+", "+df_hospital[1].xs(i)
        df_hospital.drop(i, inplace=True)


    df_hospital.index
    def replaceSpecialChar(item):
        return item.replace("：","")
    df_hospital.index = df_hospital[0].apply(replaceSpecialChar)

    Dict_Hospital = pd.Series(df_hospital[1]).to_dict()
    Dict_Hospital['醫院名稱'] = name
    return Dict_Hospital




##對每個連結發出請求，並存成html檔
import re as regex
HospitalDetailDictLi = []
for key, value in href_dict.items():    #.items()的方法，可以直接在迴圈中叫用key跟value
    re= requests.get(value)
    re.encoding = 'big5'
    
    soup = BeautifulSoup(re.text,'lxml')
    a_list1 = soup.find_all('a')
    
    NamePathDict = {}
    for tag in a_list1:
        if tag.string != None:
            if regex.match("[\u4e00-\u9fa5+]",tag.string) and tag.string != '優質動物醫院':
                NamePathDict[tag.string] = "https://topet.net/vet_list/" + str(tag['href'])

    for name, path in NamePathDict.items():
        HospitalDetailDict = ConverTableToDict(path, name)
        HospitalDetailDictLi.append(HospitalDetailDict)



import json
jsonstring = json.dumps(HospitalDetailDictLi,ensure_ascii=False)
file = open("HospitalDetail.txt",'w',encoding='utf8')
file.write(jsonstring)
file.close()