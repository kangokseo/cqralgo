import psycopg2
import pandas as pd
from datetime import datetime

conn = psycopg2.connect(
    host="localhost",
    database="cqralgo2",
    user="postgres",
    password="eugene99"
)

class cqrDB:
    def __init__(self):
        curObj = conn.cursor()
        print("Constructor will print this") 
      
    def update_daily_weights(self):
        curObj = conn.cursor()

        #sqlst = "insert into portfolio_portfolio values (12, '안정형','b')"

        df = pd.read_csv(r'C:\Users\kango\Desktop\cqralgo\cqrsite\portfolio\cvs\종목별투자비중추이20240208.csv')
        df=df.rename(columns={'KODEX 200 mkt val':'KODEX200', 'KODEX 국고채3년 mkt val':'국고채3','TIGER 미국나스닥100 mkt val':'나스닥100', 
                      'TIGER 미국S&P500선물(H) mkt val':'SP500', 'KODEX 단기채권 mkt val':'단기채', 'TIGER 단기통안채 mkt val':'통안채',
                      'KODEX 코스닥150 mkt val':'코스닥150', 'cash_rem':'cash', 'total':'total'})
        df=df[['Date','코스닥150','KODEX200','나스닥100','SP500','국고채3','단기채','통안채','cash','total']]

        for idx in range (len(df)):
            s_date = df.Date.values[idx][:10]
            i_port_id = 1
            f_item1_val = round(float(df.코스닥150.values[idx].rstrip('%'))/100,6)
            f_item2_val = round(float(df.KODEX200.values[idx].rstrip('%'))/100,6)
            f_item3_val = round(float(df.나스닥100.values[idx].rstrip('%')) / 100,6)
            f_item4_val = round(float(df.SP500.values[idx].rstrip('%')) / 100,6)
            f_item5_val = round(float(df.국고채3.values[idx].rstrip('%')) / 100,6)
            f_item6_val = round(float(df.단기채.values[idx].rstrip('%')) / 100,6)
            f_item7_val = round(float(df.통안채.values[idx].rstrip('%')) / 100,6)
            f_item8_val = round(float(df.cash.values[idx].rstrip('%')) / 100,6)
            f_item9_val = round(float(df.total.values[idx].rstrip('%')) / 100,6)
            #sqlst = f"INSERT INTO portfolio_dailympvalue (date, port_id, item1_val) values ('{s_date}', {i_port_id}, {f_item1_val})"

            sqlst = f"INSERT INTO portfolio_dailyMPweight " \
                         f"(date, port_id, item1_val, item2_val, item3_val, item4_val, item5_val, item6_val, item7_val, item8_val, port_total) values " \
                         f"('{s_date}', {i_port_id}, {f_item1_val}, {f_item2_val}, {f_item3_val}, {f_item4_val}, {f_item5_val},{f_item6_val}, {f_item7_val}, {f_item8_val}, {f_item9_val})"
            curObj.execute(sqlst)
            print (s_date )
            print (f_item1_val )
            print (f_item2_val )
           
            print(sqlst)



        conn.commit()
        conn.close()


    def update_clsweight(self):
        curObj = conn.cursor()

        df = pd.read_csv(r'C:\Users\kango\Desktop\cqralgo\cqrsite\portfolio\cvs\자산별투자비중추이20240208.csv')
        df=df.rename(columns={'5':'cls5', '3':'cls3','2':'cls2', '1':'cls1'})
        #df=df[['Date','5','3','2','11','total','위험자산비중']]

        for idx in range (len(df)):
            s_date = df.Date.values[idx][:10]
            i_port_id = 1
            item5_val = round(float(df.cls5.values[idx].rstrip('%'))/100,6)
            item4_val =0
            item3_val = round(float(df.cls3.values[idx].rstrip('%'))/100,6)
            item2_val = round(float(df.cls2.values[idx].rstrip('%')) / 100,6)
            item1_val = round(float(df.cls1.values[idx].rstrip('%')) / 100,6)
            tot_val = round(float(df.total.values[idx].rstrip('%')) / 100,6)
            risk_val = round(float(df.위험자산비중.values[idx].rstrip('%')) / 100,6)

            sqlst = f"INSERT INTO portfolio_MPclsweight " \
                         f"(date, port_id, cls5_val, cls4_val, cls3_val, cls2_val, cls1_val, total, risk_val) values " \
                         f"('{s_date}', {i_port_id}, {item5_val}, {item4_val}, {item3_val}, {item2_val}, {item1_val},{tot_val}, {risk_val})"
            curObj.execute(sqlst)
            print (s_date )
           
            print(sqlst)

        conn.commit()
        conn.close()


    def update_daily_value(self):
        curObj = conn.cursor()


        df = pd.read_csv(r'C:\Users\kango\Desktop\cqralgo\cqrsite\portfolio\cvs\일별수익률추이20240208.csv')
        df=df[['Date','port_val','일별수익률', '누적수익률']]

        for idx in range (len(df)):
            s_date = df.Date.values[idx][:10]
            item1_val = round(df.port_val.values[idx],6)
            item2_val = round(df.일별수익률.values[idx],6)

            sqlst = f"INSERT INTO portfolio_dailyMPvalue " \
                         f"(date, port_val, port_ret) values " \
                         f"('{s_date}', {item1_val}, {item2_val})"
            curObj.execute(sqlst)
           
            print(sqlst)


        conn.commit()
        conn.close()


    def update_monthly_value(self):
        curObj = conn.cursor()


        df = pd.read_csv(r'C:\Users\kango\Desktop\cqralgo\cqrsite\portfolio\cvs\월별수익률추이20240208.csv')
        df=df[['Date','port_val']]

        for idx in range (len(df)):
            s_date = df.Date.values[idx][:10]
            port_id = 1
            port_ret = round(df.port_val.values[idx],6)

            sqlst = f"INSERT INTO portfolio_monthlyMPvalue " \
                         f"(date, port_id, port_ret) values " \
                         f"('{s_date}', { port_id}, {port_ret})"
            curObj.execute(sqlst)
           
            print(sqlst)

        conn.commit()
        conn.close()


