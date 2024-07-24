import psycopg2
import pandas as pd
from datetime import datetime, date
from django.db import connection

from dotenv import load_dotenv
import os

load_dotenv()

class accountDB:    # 계좌데이타
    # def __init__(self, **kwargs):
    #     try:
    #         self.conn = psycopg2.connect(
    #             host=os.environ.get("DB_HOST"),
    #             database=os.environ.get("DB_NAME"),
    #             user=os.environ.get("DB_USER"), 
    #             password=os.environ.get("DB_PASSWORD")
    #         )
    #         curObj = self.conn.cursor()
    #         self.user_id = kwargs.get('user_id', 'Unknown')
    #         print("Connection established")
    #     except Exception as e:
    #         print(f"Error connecting to the database: {e}")

    # def __del__(self):
    #     try:
    #         self.conn.close()
    #         print("Connection closed")
    #     except AttributeError:
    #         print("Failed to close the connection because it was never established.")

    def get_account_list(self):
        try:
            with connection.cursor() as cursor:
                sql = """
                SELECT auth_user.username AS user_name, 
                    portfolio_account.계좌명 AS account_name, 
                    portfolio_account.cano, 
                    portfolio_account.app_key, 
                    portfolio_account.app_secret, 
                    portfolio_portfolio.title AS portfolio_title, 
                    portfolio_portfolio.sub_type_desc AS portfolio_type_desc,  
                    portfolio_portfolio.sub_type AS portfolio_type,  
                    portfolio_account.id 
                FROM auth_user, portfolio_account, portfolio_portfolio 
                WHERE auth_user.username = portfolio_account.user_id AND 
                    portfolio_account.portfolio_id = portfolio_portfolio.portfolio_id
                """
                cursor.execute(sql)
                return cursor.fetchall()
        except Exception as e:
            print(f"Error executing query: {e}")
            return None

class cqra2_TBL:        # 'CQRA2' 
    def __init__(self, **kwargs):
        self.type = kwargs.get('type', 5)

    def add_daily_weights(self): #종목별투자비중추이 일일업데이트

        with connection.cursor() as cursor:

            # curObj = self.conn.cursor()
            file_path = rf'cqra2/templates/{self.type}_종목별투자비중추이.csv'
            df = pd.read_csv(file_path)
            df=df.rename(columns={  '114260.KS mkt val':'국고채3',
                                    '153130.KS mkt val':'단기채', 
                                    '157450.KS mkt val':'통안채',
                                    '229200.KS mkt val':'코스닥150', 
                                    '278530.KS mkt val':'KODEX200', 
                                    '379810.KS mkt val':'나스닥100', 
                                    '379800.KS mkt val':'SP500', 
                                    'cash_rem':'cash', 'port_val':'value'})
            df=df[['Date','코스닥150','KODEX200','나스닥100','SP500','국고채3','단기채','통안채','cash','value']]

            sql = f"select max(date) from cqra2_dailyMPweight where port_id='{self.type}'"

            cursor.execute(sql)
            rs = cursor.fetchone()

            todate = rs[0].strftime("%Y-%m-%d")

            for idx in range (len(df)):  
                s_date = df.Date.values[idx][:10]

                if s_date > todate:
                    i_port_id = self.type
                    f_item1_val = round(float(df.코스닥150.values[idx].rstrip('%'))/100,6)
                    f_item2_val = round(float(df.KODEX200.values[idx].rstrip('%'))/100,6)
                    f_item3_val = round(float(df.나스닥100.values[idx].rstrip('%'))/100,6)
                    f_item4_val = round(float(df.SP500.values[idx].rstrip('%'))/100,6)
                    f_item5_val = round(float(df.국고채3.values[idx].rstrip('%'))/100,6)
                    f_item6_val = round(float(df.단기채.values[idx].rstrip('%'))/100,6)
                    f_item7_val = round(float(df.통안채.values[idx].rstrip('%'))/100,6)
                    f_item8_val = round(float(df.cash.values[idx].rstrip('%'))/100,6)
                    f_item9_val = round(float(df.value.values[idx].rstrip('%'))/100,6)

                    sqlst = f"INSERT INTO cqra2_dailyMPweight " \
                                f"(date, port_id, item1_val, item2_val, item3_val, item4_val, item5_val, item6_val, item7_val, item8_val, port_total) values " \
                                f"('{s_date}', {i_port_id}, {f_item1_val}, {f_item2_val}, {f_item3_val}, {f_item4_val}, {f_item5_val},{f_item6_val}, {f_item7_val}, {f_item8_val}, {f_item9_val})"
                    try:
                        cursor.execute(sqlst)
                        print(sqlst)
                    except Exception as e:
                        print(f"An error occurred while inserting record: {s_date}")
                        break  

    def add_clsweight(self): #자산별투자비중추이 일일업데이트
        with connection.cursor() as curObj:

            file_path = rf'cqra2/templates/{self.type}_자산별투자비중추이.csv'
            df = pd.read_csv(file_path)
            df=df.rename(columns={'6':'cls6', '5':'cls5','2':'cls2', '1':'cls1'})
            df['cls6'] = df['cls6'].str.rstrip('%').astype(float) / 100
            df['cls5'] = df['cls5'].str.rstrip('%').astype(float) / 100
            df['cls2'] = df['cls2'].str.rstrip('%').astype(float) / 100
            df['cls1'] = df['cls1'].str.rstrip('%').astype(float) / 100

            sql = f"select max(date) from cqra2_MPclsweight where port_id='{self.type}'"
            curObj.execute(sql)
            rs = curObj.fetchone()
            todate = rs[0].strftime("%Y-%m-%d")

            for idx in range (len(df)):
                s_date = df.Date.values[idx][:10]

                if s_date > todate:
                    i_port_id = self.type

                    item5_val = round(df['cls6'].values[idx] + df['cls5'].values[idx], 6)
                    item4_val = 0
                    item3_val = 0
                    item2_val = round(df['cls2'].values[idx] + df['cls1'].values[idx], 6)
                    item1_val = 0

                    tot_val = round(float(df.total.values[idx].rstrip('%'))/100,6)
                    risk_val = round(float(df.위험자산비중.values[idx].rstrip('%'))/100,6)

                    sqlst = f"INSERT INTO cqra2_MPclsweight " \
                                f"(date, port_id, cls5_val, cls4_val, cls3_val, cls2_val, cls1_val, total, risk_val) values " \
                                f"('{s_date}', {i_port_id}, {item5_val}, {item4_val}, {item3_val}, {item2_val}, {item1_val},{tot_val}, {risk_val})"
                    try:
                        curObj.execute(sqlst)
                    except Exception as e:
                        print(f"An error occurred while inserting record: {e}")
                        # curObj.rollback() 
                        break  

            # self.conn.commit()

    def add_daily_value(self): #일별수익률추이 일일업데이트
        with connection.cursor() as curObj:
            # curObj = self.conn.cursor()

            file_path = rf'cqra2/templates/{self.type}_일별수익률추이.csv'
            df = pd.read_csv(file_path)
            df=df.rename(columns={ '114260.KS mkt val':'국고채3',
                                    '153130.KS mkt val':'단기채', 
                                    '157450.KS mkt val':'통안채',
                                    '229200.KS mkt val':'코스닥150', 
                                    '278530.KS mkt val':'KODEX200', 
                                    '379810.KS mkt val':'나스닥100', 
                                    '379800.KS mkt val':'SP500', 
                                    'cash_rem': 'cash',
                            })
            df=df[['Date','코스닥150','KODEX200','나스닥100','SP500','국고채3','단기채','통안채','cash','port_val','일별수익률','누적수익률']]

            sql = f"select max(date) from cqra2_dailyMPvalue where port_id='{self.type}'"
            curObj.execute(sql)
            rs = curObj.fetchone()
            todate = rs[0].strftime("%Y-%m-%d")

            for idx in range (len(df)):
                s_date = df.Date.values[idx][:10]

                if s_date > todate:
                    port_id = self.type
                    item1_val = round(df.코스닥150.values[idx],6)
                    item2_val = round(df.KODEX200.values[idx],6)
                    item3_val = round(df.나스닥100.values[idx],6)
                    item4_val = round(df.SP500.values[idx],6)
                    item5_val = round(df.국고채3.values[idx],6)
                    item6_val = round(df.단기채.values[idx],6)
                    item7_val = round(df.통안채.values[idx],6)
                    item8_val = round(df.cash.values[idx],6)
                    port_val = round(df.port_val.values[idx],6)
                    port_ret = round(df.일별수익률.values[idx],6)
                    acum_ret = round(df.누적수익률.values[idx],6)

                    sqlst = f"INSERT INTO cqra2_dailyMPvalue " \
                                f"(date, port_id, item1_val, item2_val, item3_val, item4_val, item5_val, item6_val, item7_val, item8_val, port_val, port_ret, acum_ret) values " \
                                f"('{s_date}', { port_id}, {item1_val}, {item2_val}, {item3_val}, {item4_val}, {item5_val}, {item6_val}, {item7_val}, {item8_val}, {port_val}, {port_ret}, {acum_ret})"            
                    try:
                        curObj.execute(sqlst)
                    except Exception as e:
                        print(f"An error occurred while inserting record: {e}")
                        # curObj.rollback() 
                        break  

            # self.conn.commit()  

    def add_monthly_value(self): #월별수익률추이 일일업데이트
        with connection.cursor() as curObj:
                
            # curObj = self.conn.cursor()
            file_path = rf'cqra2/templates/{self.type}_월별수익률추이.csv'
            df = pd.read_csv(file_path)        
            df=df.rename(columns={  '114260.KS mkt val':'국고채3',
                                    '153130.KS mkt val':'단기채', 
                                    '157450.KS mkt val':'통안채',
                                    '229200.KS mkt val':'코스닥150', 
                                    '278530.KS mkt val':'KODEX200', 
                                    '379810.KS mkt val':'나스닥100', 
                                    '379800.KS mkt val':'SP500', 
                                    'cash_rem': 'cash',
                        })
            df=df[['Date','코스닥150','KODEX200','나스닥100','SP500','국고채3','단기채','통안채','cash','port_val','월별수익률','누적수익률']]

            try:               
                sql = f"DELETE FROM cqra2_monthlyMPvalue WHERE date = (SELECT MAX(date) FROM cqra2_monthlyMPvalue WHERE port_id='{self.type}') AND port_id='{self.type}'"
                curObj.execute(sql)
                # curObj.commit()  
            except Exception as e:
                print(f"An error occurred while deleting records: {e}")
                # curObj.rollback()  

            sql = f"select max(date) from cqra2_monthlyMPvalue where port_id='{self.type}'"
            curObj.execute(sql)
            rs = curObj.fetchone()
            todate = rs[0].strftime("%Y-%m-%d") # max(date)        

            for idx in range (len(df)):
                s_date = df.Date.values[idx][:10]

                if s_date > todate:
                    port_id = self.type
                    item1_val = round(df.코스닥150.values[idx],6)
                    item2_val = round(df.KODEX200.values[idx],6)
                    item3_val = round(df.나스닥100.values[idx],6)
                    item4_val = round(df.SP500.values[idx],6)
                    item5_val = round(df.국고채3.values[idx],6)
                    item6_val = round(df.단기채.values[idx],6)
                    item7_val = round(df.통안채.values[idx],6)
                    item8_val = round(df.cash.values[idx],6)
                    port_val = round(df.port_val.values[idx],6)
                    port_ret = round(df.월별수익률.values[idx],6)
                    acum_ret = round(df.누적수익률.values[idx],6)

                    sqlst = f"INSERT INTO cqra2_monthlyMPvalue " \
                                f"(date, port_id, item1_val, item2_val, item3_val, item4_val, item5_val, item6_val, item7_val, item8_val, port_val, port_ret, acum_ret) values " \
                                f"('{s_date}', { port_id}, {item1_val}, {item2_val}, {item3_val}, {item4_val}, {item5_val}, {item6_val}, {item7_val}, {item8_val}, {port_val}, {port_ret}, {acum_ret})"           
                    try:
                        curObj.execute(sqlst)
                    except Exception as e:
                        print(f"An error occurred while inserting record: {e}")
                        # curObj.rollback() 
                        break  
                    
            # self.conn.commit()

    def update_daily_weights(self): #종목별투자비중추이 초기업데이트
        with connection.cursor() as curObj:
            try:
                curObj.execute(f"DELETE FROM cqra2_dailyMPweight WHERE port_id = '{self.type}'")
                print(f"Success delete_종목별투자비중_{self.type}")
                # curObj.commit()  
            except Exception as e:
                print(f"An error occurred while deleting cqra2_dailyMPweight records: {e}")
                # curObj.rollback()  


            #Date,069500.KS mkt val,114260.KS mkt val,133690.KS mkt val,143850.KS mkt val,153130.KS mkt val,157450.KS mkt val,229200.KS mkt val,cash_rem,port_val
            #KODEX, Bonds, NASDAQ, S&P, Cash, MMF, KOSDAQ
            file_path = rf'cqra2/templates/{self.type}_종목별투자비중추이.csv'

            df = pd.read_csv(file_path)
            df=df.rename(columns={'114260.KS mkt val':'국고채3',
                                    '153130.KS mkt val':'단기채', 
                                    '157450.KS mkt val':'통안채',
                                    '229200.KS mkt val':'코스닥150', 
                                    '278530.KS mkt val':'KODEX200', 
                                    '379810.KS mkt val':'나스닥100', 
                                    '379800.KS mkt val':'SP500', 
                                    'cash_rem':'cash', 'port_val':'value'})
            df=df[['Date','코스닥150','KODEX200','나스닥100','SP500','국고채3','단기채','통안채','cash','value']]

            for idx in range (len(df)):
                s_date = df.Date.values[idx][:10]
                i_port_id = self.type 
                f_item1_val = round(float(df.코스닥150.values[idx].rstrip('%'))/100,6)
                f_item2_val = round(float(df.KODEX200.values[idx].rstrip('%'))/100,6)
                f_item3_val = round(float(df.나스닥100.values[idx].rstrip('%'))/100,6)
                f_item4_val = round(float(df.SP500.values[idx].rstrip('%'))/100,6)
                f_item5_val = round(float(df.국고채3.values[idx].rstrip('%'))/100,6)
                f_item6_val = round(float(df.단기채.values[idx].rstrip('%'))/100,6)
                f_item7_val = round(float(df.통안채.values[idx].rstrip('%'))/100,6)
                f_item8_val = round(float(df.cash.values[idx].rstrip('%'))/100,6)
                f_item9_val = round(float(df.value.values[idx].rstrip('%'))/100,6)

                sqlst = f"INSERT INTO cqra2_dailyMPweight " \
                            f"(date, port_id, item1_val, item2_val, item3_val, item4_val, item5_val, item6_val, item7_val, item8_val, port_total) values " \
                            f"('{s_date}', {i_port_id}, {f_item1_val}, {f_item2_val}, {f_item3_val}, {f_item4_val}, {f_item5_val},{f_item6_val}, {f_item7_val}, {f_item8_val}, {f_item9_val})"
                
                try:
                    curObj.execute(sqlst)
                    
                except Exception as e:
                    print(f"An error occurred while inserting record: {e}")
                    # curObj.rollback()  
                    break  

            print(f"Success init_종목별투자비중_{self.type}")

    def update_clsweight(self): #자산별투자비중추이 초기업데이트
        with connection.cursor() as curObj:
            try:
                curObj.execute(f"DELETE FROM cqra2_MPclsweight WHERE port_id = '{self.type}'")
                print(f"Success delete_자산별투자비중_{self.type}")
                # curObj.commit()  
            except Exception as e:
                print(f"An error occurred while deleting cqra2_MPclsweight records: {e}")
                # curObj.rollback()  

            file_path = rf'cqra2/templates/{self.type}_자산별투자비중추이.csv'
            df = pd.read_csv(file_path)
            df=df.rename(columns={'6':'cls6', '5':'cls5','2':'cls2', '1':'cls1'})
            df['cls6'] = df['cls6'].str.rstrip('%').astype(float) / 100
            df['cls5'] = df['cls5'].str.rstrip('%').astype(float) / 100
            df['cls2'] = df['cls2'].str.rstrip('%').astype(float) / 100
            df['cls1'] = df['cls1'].str.rstrip('%').astype(float) / 100
           # df=df.rename(columns={'5':'cls5', '3':'cls3','2':'cls2', '1':'cls1'})

            for idx in range (len(df)):
                s_date = df.Date.values[idx][:10]
                i_port_id = self.type 

                item5_val = round(df['cls6'].values[idx] + df['cls5'].values[idx], 6)
                item4_val = 0
                item3_val = 0
                item2_val = round(df['cls2'].values[idx] + df['cls1'].values[idx], 6)
                item1_val = 0

                tot_val = round(float(df.total.values[idx].rstrip('%'))/100,6)
                risk_val = round(float(df.위험자산비중.values[idx].rstrip('%'))/100,6)

                sqlst = f"INSERT INTO cqra2_MPclsweight " \
                            f"(date, port_id, cls5_val, cls4_val, cls3_val, cls2_val, cls1_val, total, risk_val) values " \
                            f"('{s_date}', {i_port_id}, {item5_val}, {item4_val}, {item3_val}, {item2_val}, {item1_val},{tot_val}, {risk_val})"
                try:
                    curObj.execute(sqlst)
                    
                except Exception as e:
                    print(f"An error occurred while inserting record: {e}")
                    # curObj.rollback() 
                    break  
            print(f"Success init_자산별투자비중_{self.type}")       

    def update_daily_value(self): #일별수익률추이 초기업데이트
        with connection.cursor() as curObj:
            try:
                curObj.execute(f"DELETE FROM cqra2_dailyMPvalue WHERE port_id = '{self.type}'")
                print(f"Success delete_일별수익률_{self.type}")
                # curObj.commit()  
            except Exception as e:
                print(f"An error occurred while deleting cqra2_dailyMPvalue records: {e}")
                # curObj.rollback() 

            #Date,069500.KS mkt val,114260.KS mkt val,133690.KS mkt val,143850.KS mkt val,153130.KS mkt val,
            #157450.KS mkt val,229200.KS mkt val,cash_rem,port_val,일별수익률,누적수익률

            file_path = rf'cqra2/templates/{self.type}_일별수익률추이.csv'
            df = pd.read_csv(file_path)
            df=df.rename(columns={'114260.KS mkt val':'국고채3',
                                    '153130.KS mkt val':'단기채', 
                                    '157450.KS mkt val':'통안채',
                                    '229200.KS mkt val':'코스닥150', 
                                    '278530.KS mkt val':'KODEX200', 
                                    '379810.KS mkt val':'나스닥100', 
                                    '379800.KS mkt val':'SP500', 
                                    'cash_rem': 'cash',
                            })
            df=df[['Date','코스닥150','KODEX200','나스닥100','SP500','국고채3','단기채','통안채','cash','port_val','일별수익률','누적수익률']]

            for idx in range (len(df)):
                s_date = df.Date.values[idx][:10]
                port_id = self.type 
                item1_val = round(df.코스닥150.values[idx],6)
                item2_val = round(df.KODEX200.values[idx],6)
                item3_val = round(df.나스닥100.values[idx],6)
                item4_val = round(df.SP500.values[idx],6)
                item5_val = round(df.국고채3.values[idx],6)
                item6_val = round(df.단기채.values[idx],6)
                item7_val = round(df.통안채.values[idx],6)
                item8_val = round(df.cash.values[idx],6)
                port_val = round(df.port_val.values[idx],6)
                port_ret = round(df.일별수익률.values[idx],6)
                acum_ret = round(df.누적수익률.values[idx],6)

                sqlst = f"INSERT INTO cqra2_dailyMPvalue " \
                            f"(date, port_id, item1_val, item2_val, item3_val, item4_val, item5_val, item6_val, item7_val, item8_val, port_val, port_ret, acum_ret) values " \
                            f"('{s_date}', { port_id}, {item1_val}, {item2_val}, {item3_val}, {item4_val}, {item5_val}, {item6_val}, {item7_val}, {item8_val}, {port_val}, {port_ret}, {acum_ret})"            
                try:
                    curObj.execute(sqlst)
                    
                except Exception as e:
                    print(f"An error occurred while inserting record: {e}")
                    # curObj.rollback() 
                    break  
            print(f"Success init_일별수익률_{self.type}")      

    def update_monthly_value(self): #월별수익률추이 초기업데이트
        with connection.cursor() as curObj:
            try:
                curObj.execute(f"DELETE FROM cqra2_monthlyMPvalue WHERE port_id = '{self.type}'")
                print(f"Success delete_월별수익률_{self.type}")
                # curObj.commit()  
            except Exception as e:
                print(f"An error occurred while deleting cqra2_monthlyMPvalue records: {e}")
                # curObj.rollback()  
            
            #Date,069500.KS mkt val,114260.KS mkt val,133690.KS mkt val,143850.KS mkt val,153130.KS mkt val,157450.KS mkt val,
            #229200.KS mkt val,cash_rem,port_val,월별수익률,누적수익률
                
            file_path = rf'cqra2/templates/{self.type}_월별수익률추이.csv'
            df = pd.read_csv(file_path)
            df=df.rename(columns={'114260.KS mkt val':'국고채3',
                                    '153130.KS mkt val':'단기채', 
                                    '157450.KS mkt val':'통안채',
                                    '229200.KS mkt val':'코스닥150', 
                                    '278530.KS mkt val':'KODEX200', 
                                    '379810.KS mkt val':'나스닥100', 
                                    '379800.KS mkt val':'SP500', 
                                'cash_rem': 'cash',
                        })
            df=df[['Date','코스닥150','KODEX200','나스닥100','SP500','국고채3','단기채','통안채','cash','port_val','월별수익률','누적수익률']]

            for idx in range (len(df)):
                s_date = df.Date.values[idx][:10]
                port_id = self.type
                item1_val = round(df.코스닥150.values[idx],6)
                item2_val = round(df.KODEX200.values[idx],6)
                item3_val = round(df.나스닥100.values[idx],6)
                item4_val = round(df.SP500.values[idx],6)
                item5_val = round(df.국고채3.values[idx],6)
                item6_val = round(df.단기채.values[idx],6)
                item7_val = round(df.통안채.values[idx],6)
                item8_val = round(df.cash.values[idx],6)
                port_val = round(df.port_val.values[idx],6)
                port_ret = round(df.월별수익률.values[idx],6)
                acum_ret = round(df.누적수익률.values[idx],6)

                sqlst = f"INSERT INTO cqra2_monthlyMPvalue " \
                            f"(date, port_id, item1_val, item2_val, item3_val, item4_val, item5_val, item6_val, item7_val, item8_val, port_val, port_ret, acum_ret) values " \
                            f"('{s_date}', { port_id}, {item1_val}, {item2_val}, {item3_val}, {item4_val}, {item5_val}, {item6_val}, {item7_val}, {item8_val}, {port_val}, {port_ret}, {acum_ret})"           
                try:
                    curObj.execute(sqlst)
                except Exception as e:
                    print(f"An error occurred while inserting record: {e}")
                    # curObj.rollback() 
                    break  
                
            print(f"Success init_월별수익률_{self.type}")
        
    def search_daily_value(self,r_fromdate, r_todate): 
        try:
            with connection.cursor() as cursor:
                sql = f"SELECT date, port_id, port_val, port_ret " \
                    f"FROM cqra2_dailyMPvalue " \
                    f"WHERE date between '{r_fromdate}' and '{r_todate}' " \
                    f"and port_id='{self.type}' order by date asc"
                cursor.execute(sql)
                rows = cursor.fetchall()

                columns = [col[0] for col in cursor.description]
                df = pd.DataFrame(rows, columns=columns)

                return df
                
        except Exception as e:
            print(f"Error executing query: {e}")
            return None

