from pprint import pprint  ##pretty print
import pandas as pd
from bs4 import BeautifulSoup
import pyodbc  ##access to sql server


file = open('keys.txt','r',encoding='utf8')

filepath_dict = {}
for line in file:
    place = line.replace('\n','')
    filepath_dict[place] = ('html/' + place + '.txt')

file.close()

def ReadHtmlAsTable(path, place):
    """return a dataframe"""
    file = open(path,'r',encoding='utf8')
    html_text = file.read()
    file.close()
    
    soup = BeautifulSoup(html_text,'lxml')
    tables = soup.find_all('table')
    NeededTable = str(tables[4])

    df_hospitals = pd.read_html(NeededTable,encoding='utf8')[0]

    df_hospitals.columns =  df_hospitals.xs(0)
    df_hospitals.drop(0, inplace=True)
    df_hospitals['地區'] = place
    df_hospitals.drop('其他優惠',axis=1,inplace=True)
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
    df_hospitals.apply(ReplaceNanAndBool,axis=1)  ##axis=0: apply function to each item in each column, axis=1: apply function to each item in each row
    
    return df_hospitals



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