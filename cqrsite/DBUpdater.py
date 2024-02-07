import pandas as pd
import pymysql

class PortfolioDB:
    def __init__(self):
        self.conn = pymysql.connect(host='localhost', user='', password='', db='', charset='utf8')
        self.close={}
        self.get_info()

    def __del__(self):
        self.conn.close()

    def get_info(self):
        sql = "select * from account"

    def get_portfolio(self, code, start_date=None, end_date=None):
        sql = "select * from portfolio"
        df = pd.read_sql(sql, self.conn)
        df.index = df['date']
        return df