import requests
from bs4 import BeautifulSoup
from pprint import pprint  ##pretty print


##送出Http請求，把請求回來的結果打包成re物件
re = requests.get("https://topet.net/vet_recommand.htm")

##設定re物件的讀取編碼(可以直接看網頁上的head的部分，找到編碼)，這個部分要很注意，大部分網頁都已經使用utf8，cp950、big5比較少見
re.encoding = "big5"

##叫出re物件的text屬性，也就會是html原始檔
html_text = re.text

##用BeautifulSoup解析HTML文件(跑出的警告不用理他)
soup = BeautifulSoup(html_text,'lxml')

##用裡面的find_all方法，找出所有有<a>標籤的部分
a_list = soup.find_all("a")


##可以得到如下結果
#pprint(a_list)
###[<a href="vet_recommand.htm"><img border="0" src="top_header_new1.gif"/></a>,
### <a href="mailto:topet@topet.net">topet@topet.net</a>,
### <a href="vet_list/vet_Taipei.htm"><font size="3">台北市</font></a>,
### <a href="vet_list/vet_Changhwa.htm"><font size="3">彰化縣市</font></a>,
### <a href="vet_list/vet_Pingtung.htm"><font size="3">屏東縣市</font></a>,
### <a href="vet_list/vet_NewTaipei.htm"><font size="3">新北市</font></a>,
### <a href="vet_list/vet_Jiayee.htm"><font size="3">嘉義縣市</font></a>,
### <a href="vet_list/vet_Hwalien.htm">花蓮縣市</a>,
### <a href="vet_list/vet_Tainan.htm"><font size="3">台南市</font></a>,
### <a href="vet_list/vet_Hsinchu.htm"><font size="3">新竹縣市</font></a>,
### <a href="vet_list/vet_Taitung.htm">台東縣市</a>,
### <a href="vet_list/vet_Kaohsiung.htm"><font size="3">高雄市</font></a>,
### <a href="vet_list/vet_Keelung.htm"><font size="3">基隆市</font></a>,
### <a href="vet_list/vet_Yuenlin.htm">雲林縣</a>,
### <a href="vet_list/vet_Taichung.htm"><font size="3">台中市</font></a>,
### <a href="vet_list/vet_Miaolee.htm"><font size="3">苗栗縣市</font></a>,
### <a href="vet_list/vet_Yeelan.htm">宜蘭縣</a>,
### <a href="vet_list/vet_TaoYuan.htm"><font size="3">桃園市</font></a>,
### <a href="vet_list/vet_Nantou.htm"><font size="3">南投縣市</font></a>,
### <a href="index.htm"><img border="0" src="index.9.gif"/></a>,
### <a href="https://www.facebook.com/groups/461801927314512/"><img border="0" height="43" src="index.10.gif" width="139"/></a>,
### <a href="https://www.facebook.com/Topet.net?ref=bookmarks"><img border="0" height="46" src="index.12.gif" width="165"/></a>,
### <a href="mailto:topet@topet.net">topet@topet.net</a>]

##找出第二個到第十八個
href_list = []
href_dict = {}  ##用字典屬性可以儲存，ket以及value
for i in range(2,19):
    href_list.append('https://topet.net/' + a_list[i]['href'])
    href_dict[a_list[i].string] = 'https://topet.net/' + a_list[i]['href']


#pprint(href_list)
#pprint(href_dict)
###['https://topet.net/vet_list/vet_Changhwa.htm',
### 'https://topet.net/vet_list/vet_Pingtung.htm',
### 'https://topet.net/vet_list/vet_NewTaipei.htm',
### 'https://topet.net/vet_list/vet_Jiayee.htm',
### 'https://topet.net/vet_list/vet_Hwalien.htm',
### 'https://topet.net/vet_list/vet_Tainan.htm',
### 'https://topet.net/vet_list/vet_Hsinchu.htm',
### 'https://topet.net/vet_list/vet_Taitung.htm',
### 'https://topet.net/vet_list/vet_Kaohsiung.htm',
### 'https://topet.net/vet_list/vet_Keelung.htm',
### 'https://topet.net/vet_list/vet_Yuenlin.htm',
### 'https://topet.net/vet_list/vet_Taichung.htm',
### 'https://topet.net/vet_list/vet_Miaolee.htm',
### 'https://topet.net/vet_list/vet_Yeelan.htm',
### 'https://topet.net/vet_list/vet_TaoYuan.htm']
###{'台中市': 'https://topet.net/vet_list/vet_Taichung.htm',
### '台南市': 'https://topet.net/vet_list/vet_Tainan.htm',
### '台東縣市': 'https://topet.net/vet_list/vet_Taitung.htm',
### '嘉義縣市': 'https://topet.net/vet_list/vet_Jiayee.htm',
### '基隆市': 'https://topet.net/vet_list/vet_Keelung.htm',
### '宜蘭縣': 'https://topet.net/vet_list/vet_Yeelan.htm',
### '屏東縣市': 'https://topet.net/vet_list/vet_Pingtung.htm',
### '彰化縣市': 'https://topet.net/vet_list/vet_Changhwa.htm',
### '新北市': 'https://topet.net/vet_list/vet_NewTaipei.htm',
### '新竹縣市': 'https://topet.net/vet_list/vet_Hsinchu.htm',
### '桃園市': 'https://topet.net/vet_list/vet_TaoYuan.htm',
### '花蓮縣市': 'https://topet.net/vet_list/vet_Hwalien.htm',
### '苗栗縣市': 'https://topet.net/vet_list/vet_Miaolee.htm',
### '雲林縣': 'https://topet.net/vet_list/vet_Yuenlin.htm',
### '高雄市': 'https://topet.net/vet_list/vet_Kaohsiung.htm'}


##對每個連結發出請求，並存成html檔(自己重新跑一次的話，記得先做一個資料夾，命名為html)
for key, value in href_dict.items():    #.items()的方法，可以直接在迴圈中叫用key跟value
    re= requests.get(value)
    re.encoding = 'big5'
    html_text = re.text
    file = open('html/' + key+'.txt','w',encoding='utf8')  #open:打開一個文件，key+'.txt':檔名，'w':寫入模式('r':讀取模式)，encoding:打開文件的編碼
    file.write(html_text)
    file.close()


##為了等等叫用html檔方便，先把檔案名稱存起來
file = open('keys.txt','w',encoding='utf8')
for key in href_dict:
    file.writelines(key + '\n')

file.close()

