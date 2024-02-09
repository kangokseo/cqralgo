import psycopg2

conn = psycopg2.connect(
    host="localhost",
    database="cqralgo",
    user="postgres",
    password="eugene99"
)

curObj = conn.cursor()

# curObj.execute ("create database cqralgo")
# curObj.execute("select * from portfolio_account")
# data = curObj.fetchall()

curObj.execute("insert into portfolio_dailyMPvalue values ('2024/02/08', 1, 0.4, 0.3, 0,3)")

conn.commit()

# 연결 종료
conn.close()

#print (data)