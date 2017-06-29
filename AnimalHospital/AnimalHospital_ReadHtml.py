from pprint import pprint  ##pretty print
import pandas as pd
from bs4 import BeautifulSoup
import pyodbc  ##access to sql server


file = open('keys.txt','r',encoding='utf8')

##把檔案名稱轉換成list
filepath_dict = {}
for line in file:
    place = line.replace('\n','')
    filepath_dict[place] = ('html/' + place + '.txt')

file.close()

##定義一個輸入html的檔案名稱，輸出裡面你要的table的dataframe的方法
##dataframe是pandas套件中處理資料一個很好用的工具，很值得一學
def ReadHtmlAsTable(path, place):
    """return a dataframe"""
    
    ##打開文件
    file = open(path,'r',encoding='utf8')
    html_text = file.read()
    file.close()
    
    ##把文件中需要的table節取出來
    soup = BeautifulSoup(html_text)
    #soup = BeautifulSoup(html_text,'lxml')

    tables = soup.find_all('table')
    NeededTable = str(tables[4])

    ##把節取出的table轉換成dataframe型別
    ##請注意，這是pandas最厲害的地方，他可以直接把html格式的table轉換成可被處理的dataframe
    ##另外，如果表格形式簡單的話，可以直接把html url傳進去，會回傳包括網也上的所有table的list回來
    ##(C#我此時上網找了一下，還沒有那麼好用的套件，要自己拆tag)
    df_hospitals = pd.read_html(NeededTable,encoding='utf8')[0]

##df_hospitals.head()
##到此為止table會長這個樣子(可以輸出df_hospitals試試看，可以用df_hospitals.head()方法只取前面五行)
#   0	                1	        2	                          3	            4          	5
#0	醫院名稱	        電 話	    地 址	                      優質動物醫院	現金抵用	其他優惠
#1	太僕動物醫院	    02-25170902	台北市中山區龍江路260號	      ●	        ●	        NaN
#2	天母太僕動物醫院	02-28732070	台北市士林區天母西路48號	  ●	        ●	        NaN
#3	南京太僕動物醫院	02-27562005	台北市松山區南京東路五段286號 ●	        ●	        NaN
#4	安安動物醫院	    02-27281315	台北市松德路57號	          ●	        NaN	        NaN

    ##因為html不是用<thead寫的>，所以第一個row不會被自動修正成為column header，要手動把第一個row變成column header
    df_hospitals.columns =  df_hospitals.xs(0)
    ##第一個row變成column header，就可以丟掉了
    df_hospitals.drop(0, inplace=True)

    ##把傳入的參數place變成一個欄位，因為當前的df_hospitals並沒有'地區'這個欄位，所以會新建一個欄位，裡面的值都是place
    df_hospitals['地區'] = place

    ##我發現'其他優惠'藍沒有任何有意義的資訊，所以丟了，axis是指索引到column header'其他優惠'，然後丟掉這個column
    ## inplace=1 == df_hospitals = df_hospitals.drop('其他優惠',axis=1)
    df_hospitals.drop('其他優惠',axis=1,inplace=True)

    ##定義一個可以被下面一行df_hospitals apply的方法
    def ReplaceNanAndBool(row):
        if pd.isnull(row['優質動物醫院']):  ## To replace its special character　with bool type value
            row['優質動物醫院']=False
        else:
            row['優質動物醫院']=True
        if pd.isnull(row['現金抵用']):
            row['現金抵用']=False
        else:
            row['現金抵用']=True
        return row

    ##apply方法，可以把傳入的方法套用在每一個元素之上(這裡是套用在每一個row上面，比較簡單的function也可以用lambda運算式處理)
    df_hospitals.apply(ReplaceNanAndBool,axis=1)  ##axis=0: apply function to each item in each column, axis=1: apply function to each item in each row
    
    return df_hospitals


##輸出的table會長這個樣子
#   醫院名稱	        電 話	    地 址	                        優質動物醫院	現金抵用	地區
#1	太僕動物醫院	    02-25170902	台北市中山區龍江路260號	         True	        True	    台北市
#2	天母太僕動物醫院	02-28732070	台北市士林區天母西路48號	     True	        True	    台北市
#3	南京太僕動物醫院	02-27562005	台北市松山區南京東路五段286號    True	        True	    台北市
#4	安安動物醫院	    02-27281315	台北市松德路57號	             True	        False    	台北市
#5	仁愛動物醫院     	02-27029165	台北市大安區仁愛路四段228-3號    True           False	    台北市


##定義一個方法，把dataframe放入，可以把dataframe逐行insert進去sql server
def WriteDfIntoSql(df):
    conn = pyodbc.connect(
        r'DRIVER={ODBC Driver 13 for SQL Server};'  ## if sql server 2014 DRIVER={ODBC Driver 11 for SQL Server};
        r'SERVER=.;'
        r'DATABASE=AnimalHospitals;'  ##You should change db name
        r'Trusted_Connection=yes;'  ##I tried to connect with user and password, but in vain. If you want to try "https://github.com/mkleehammer/pyodbc/wiki/Connecting-to-SQL-Server-from-Windows"
        )
    cursor = conn.cursor()
    
    def InserIntoSql(row):
        InsertParams = (row['醫院名稱'],row['電 話'],row['地 址'],row['優質動物醫院'],row['現金抵用'],row['地區'])
        SqlCmd =  "insert into Hospitals([HospitalName],[Phone],[Address],[Professional],[CashCoupon],[PlaceClassification]) Values (?,?,?,?,?,?)" 
        cursor.execute(SqlCmd,InsertParams)
    
    df.apply(InserIntoSql,axis=1)

    cursor.commit()
    cursor.close()
    conn.close()

def WriteDfIntoCsv(key, df):
    df.to_csv(key)



##每個html檔都跑過上面定義的兩個方法
for key, value in filepath_dict.items():
    df = ReadHtmlAsTable(value,key)
    
    ## There are two choice:
    ## if you want to insert into MS Sql, take off this nnote mark
    #WriteDfIntoSql(df)
    
    ## Second, to csv
    WriteDfIntoCsv(key, df)
