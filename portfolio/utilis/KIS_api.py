import requests
import json
import keyring
import pandas as pd
import time
import numpy as np
import datetime
from datetime import timedelta
import schedule
import pytz


class systemtrade:

    def  __init__(self, **kwargs):

        #set default values
        self.app_key = kwargs.get('app_key', 'Unknown')
        self.app_secret = kwargs.get('app_secret', 'Unknown')
        self.ID = kwargs.get('ID', 'Unknown')
        self.cano = kwargs.get('cano', 'Unknown')
        self.mock = kwargs.get('mock', 'Unknown')
        self.custtype = kwargs.get('custtype', 'P')
        self.port_subtype = kwargs.get('port_subtype', '5')

        path = "oauth2/tokenP" # 접근토큰발급
        if self.mock == "1":
            self.url_base = "https://openapivts.koreainvestment.com:29443" # 모의투자
        else:
            self.url_base = "https://openapi.koreainvestment.com:9443" # 실전 투자  
        url = f"{self.url_base}/{path}" 

        self.app_key = keyring.get_password(self.app_key, self.ID)
        self.app_secret = keyring.get_password(self.app_secret, self.ID)

        headers = {"content-type": "application/json"}
        body = {
            "grant_type": "client_credentials",
            "appkey": self.app_key,
            "appsecret": self.app_secret
        }
        res = requests.post(url, headers=headers, data=json.dumps(body))
        time.sleep(0.1)

        self.kst_tz = pytz.timezone('Asia/Seoul') # timezone 
        self.access_token = res.json()['access_token']      
        self.access_token_token_expired = res.json()['access_token_token_expired']  

        #홀수11-4월 (코스닥60, 코스피40). 홀수 5-10월(나스닥50,S&P50)
        #짝수11-4월 (코스닥50, 코스피50). 짝수 5-10월(나스닥50,S&P50)
        # tic = [ "114260.KS", "153130.KS", "157450.KS","229200.KS", "278530.KS", "379810.KS", "379800.KS"] 
        # Bond, cash, mmf, kosdq, KOSPI, NASDAQ, S&P

        values = {
            5: (1, 0, 1, 0, 1, 0),                  #공격형
            4: (0.7, 0.3, 0.7, 0.3, 0.7, 0.3),      #적극형
            3: (0.5, 0.5, 0.5, 0.5, 0.5, 0.5),      #중립형
            2: (0.3, 0.7, 0.3, 0.7, 0.3, 0.7),      #안정형
        }
        odd_stock_w, odd_bond_w, even_stock_w, even_bond_w, even_passive_stock_w, even_passive_bond_w = values.get(int(self.port_subtype), (None, None, None, None, None, None))

        self.mp1 = pd.DataFrame({   # 포트폴리오 Define. 
            '종목코드': [
                "278530", #KODEX 200TR
                "229200", #KODEX 코스닥150
                "379810", #KODEX 미국나스닥100TR
                "379800", #KODEX 미국S&P500TR
                "114260", #KODEX 국고채3년
                "153130", #KODEX 단기채권
                "157450", #TIGER 단기통안채
            ],
            '이름': ["KODEX 200TR", "KODEX 코스닥150", "KODEX 미국나스닥100TR", "KODEX 미국S&P500TR", 
                "KODEX 국고채3년", "KODEX 단기채권", "TIGER 단기통안채"],
            '홀수 비중 11-4': [odd_stock_w*0.4, odd_stock_w*0.6, odd_stock_w*0.0, odd_stock_w*0.0, odd_bond_w*(1/3), odd_bond_w*(1/3), odd_bond_w*(1/3)],
            '홀수 비중 5-10': [odd_stock_w*0, odd_stock_w*0, odd_stock_w*0.5, odd_stock_w*0.5, odd_bond_w*(1/3), odd_bond_w*(1/3), odd_bond_w*(1/3)],
            '짝수 비중 11-4': [even_stock_w*0.5, even_stock_w*0.5, even_stock_w*0.0, even_stock_w*0.0, even_bond_w*(1/3), even_bond_w*(1/3), even_bond_w*(1/3)],
            '짝수 비중 5-10': [even_passive_stock_w*0.0, even_passive_stock_w*0.0, even_passive_stock_w*0.5, even_passive_stock_w*0.5, even_passive_bond_w*(1/3), even_passive_bond_w*(1/3), even_passive_bond_w*(1/3)]
        })
        #print(self.mp1)
        #print("json:", res.json())   
        #print(datetime.datetime.now().astimezone(self.kst_tz))



    # 현재가 구하기
    def get_price(self, ticker):
        path = "uapi/domestic-stock/v1/quotations/inquire-price"
        url = f"{self.url_base}/{path}"

        headers = {
            "Content-Type": "application/json",
            "authorization": f"Bearer {self.access_token}",
            "appKey": self.app_key,
            "appSecret": self.app_secret,
            "tr_id": "FHKST01010100" #현재가
        }
        params = {"fid_cond_mrkt_div_code": "J", "fid_input_iscd": ticker}

        res = requests.get(url, headers=headers, params=params)
        price = res.json()['output']['stck_prpr']
        price = int(price)
        time.sleep(0.1)

        return price
    
    # 트레이딩때 필요한 hash key 받기
    def hashkey(self, datas):
        path = "uapi/hashkey"
        url = f"{self.url_base}/{path}"

        headers = {
            'content-Type': 'application/json',
            'appKey': self.app_key,
            'appSecret': self.app_secret,
        }
        res = requests.post(url, headers=headers, data=json.dumps(datas))
        hashkey = res.json()["HASH"]

        return hashkey

    # 계좌 잔고 조회
    def check_account(self):

        output1 = []
        output2 = []
        CTX_AREA_NK100 = ''
        CTX_AREA_FK100 = ''

        if self.mock == "1": #[실전투자]TTTC8434R: 주식잔고조회, [모의투자]VTTC8434R: 주식잔고조회
            tr_id = "VTTC8434R" 
        else:
            tr_id = "TTTC8434R" 

        while True:
            path = "/uapi/domestic-stock/v1/trading/inquire-balance" #주식잔고조회
            url = f"{self.url_base}/{path}"

            headers = {
                "Content-Type": "application/json",
                "authorization": f"Bearer {self.access_token}",
                "appKey": self.app_key,
                "appSecret": self.app_secret,
                "tr_id": tr_id,
                "custtype": self.custtype,
            }

            params = {
                "CANO": self.cano,
                "ACNT_PRDT_CD": "01",
                "AFHR_FLPR_YN": "N",
                "OFL_YN": "N",
                "INQR_DVSN": "01",
                "UNPR_DVSN": "01",
                "FUND_STTL_ICLD_YN": "N",
                "FNCG_AMT_AUTO_RDPT_YN": "N",                              
                "PRCS_DVSN": "01",
                "CTX_AREA_FK100": '',
                "CTX_AREA_NK100": CTX_AREA_NK100
            }

            res = requests.get(url, headers=headers, params=params)
            if res.status_code == 200:
                print("계좌 조회 성공:")
                #print(res.json())
            else:
                print("계좌 조회 실패, 상태 코드:", res.status_code)
                print(res.text)

            output1.append(pd.DataFrame.from_records(res.json()['output1']))

            CTX_AREA_NK100 = res.json()['ctx_area_nk100'].strip()

            if CTX_AREA_NK100 == '':
                output2.append(res.json()['output2'][0])
                break

        if not output1[0].empty:
            res1 = pd.concat(output1)[['pdno','hldg_qty']].rename(columns={
                                        'pdno': '종목코드',
                                        'hldg_qty': '보유수량'
                                    }).reset_index(drop=True)
        else:
            res1 = pd.DataFrame(columns=['종목코드', '보유수량'])

        res2 = output2[0]
        #print(res2)

        return [res1, res2]


   # 투자 알고리즘에 의한 리벨런싱을 위한 목표/투자 수량
    def rebalance_target(self): 
        
        ap, account = self.check_account() # 계좌잔고조회: 보유 종목과 aum 불러오기

        # 매매 구성
        target = self.mp1.merge(ap, on='종목코드', how='outer')
        target['보유수량'] = target['보유수량'].fillna(0).apply(pd.to_numeric)

        # 현재가 확인
        target['현재가'] = target.apply(lambda x: self.get_price(x.종목코드), axis=1)

        # 날짜
        kst_tz = pytz.timezone('Asia/Seoul')
        today = datetime.datetime.now().astimezone(kst_tz)

        if today.date().day < 5: #월초 리밸런싱
             # Define Strategy (i.e. Porftolio Weights)
            if ((today.date().month in [11,12]) & (today.date().year%2 == 0)) or ((today.date().month in [1,2,3,4]) & (today.date().year%2 == 1)): 
                weights = target['홀수 비중 11-4']
            elif ((today.date().month in [5,6,7,8,9,10]) & (today.date().year%2 == 1)): 
                weights = target['홀수 비중 5-10']
            elif ((today.date().month in [11,12]) & (today.date().year%2 == 1)) or ((today.date().month in [1,2,3, 4]) & (today.date().year%2 == 0)): 
                weights = target['짝수 비중 11-4']
            elif ((today.date().month in [5,6,7,8,9,10]) & (today.date().year%2 == 0)): 
                weights = target['짝수 비중 5-10']           
        else: #월말 리밸런싱
            # Define Strategy (i.e. Porftolio Weights)
            if ((today.date().month in [10,11,12]) & (today.date().year%2 == 0)) or ((today.date().month in [1,2,3]) & (today.date().year%2 == 1)): 
                weights = target['홀수 비중 11-4']
            elif ((today.date().month in [4,5,6,7,8,9]) & (today.date().year%2 == 1)): 
                weights = target['홀수 비중 5-10']
            elif ((today.date().month in [10,11,12]) & (today.date().year%2 == 1)) or ((today.date().month in [1,2,3]) & (today.date().year%2 == 0)): 
                weights = target['짝수 비중 11-4']
            elif ((today.date().month in [4,5,6,7,8,9]) & (today.date().year%2 == 0)): 
                weights = target['짝수 비중 5-10']
            

        # 주당 투자 금액
        invest_per_stock = int(account['tot_evlu_amt']) * 0.97

        # 목표수량 및 투자수량 입력
        target['목표수량'] = np.where(target['종목코드'].isin(self.mp1['종목코드'].tolist()),
                                np.floor(invest_per_stock*weights / target['현재가']), 0)
        target['투자수량'] = target['목표수량'] - target['보유수량']
        
        return target
    

    # 수량 지정 주문
    def trade_at_once(self, ticker, tr_id, trade_type, qty, price):

        path = "uapi/domestic-stock/v1/trading/order-cash"
        url = f"{self.url_base}/{path}"

        data = {
            "CANO": self.cano, # 계좌번호 앞 8지리
            "ACNT_PRDT_CD": "01",
            "PDNO": ticker,     # 종목코드
            "ORD_DVSN": trade_type,   # 주문 방법     NOTE: Change type of transaction here. 
            "ORD_QTY": str(int(qty)),     # 주문 수량
            "ORD_UNPR": str(int(price))   # 주문 단가 (시장가의 경우 0)
        }

        headers = {
            "Content-Type": "application/json",
            "authorization": f"Bearer {self.access_token}",
            "appKey": self.app_key,
            "appSecret": self.app_secret,
            "tr_id": tr_id,
            "custtype": "P",
            "hashkey": self.hashkey(data)
        }


        print(data)
        res = requests.post(url, headers=headers, data=json.dumps(data)) 

        print(res.json())
        return schedule.CancelJob
    
    # 리밸런싱 스케줄 메인. 지정가 "00"
    def schedule_rebalancing_00(self):
        
        target_day = self.rebalance_target()       #목표/투자 수량

        print(target_day)
        today = datetime.datetime.now().astimezone(self.kst_tz)
        today_plus_two = today + datetime.timedelta(minutes=2)
        today_plus_three = today + datetime.timedelta(minutes=2, seconds=40)

        # 06 : 장후 시간외 (15:30~16:00)
        # 05: 장전시간외(08:30-8:40. 8:20부터 주문가능). 전일종가
        startDt = datetime.datetime.now().astimezone(self.kst_tz).replace( hour=today_plus_two.hour, 
            minute=today_plus_two.minute, 
            second=today_plus_two.second, 
            microsecond=today_plus_two.microsecond)
        self.endDt = datetime.datetime.now().astimezone(self.kst_tz).replace( hour=today_plus_three.hour, 
            minute=today_plus_three.minute, 
            second=today_plus_three.second, 
            microsecond=today_plus_three.microsecond)
        
        schedule.clear() # 스케줄 초기화

        time_list = pd.date_range(startDt, self.endDt, periods = target_day.shape[0])    
        time_list = time_list.round(freq = 's').tolist()    
        time_list_sec = [s.strftime('%H:%M:%S') for s in time_list]      
        print("time_list_sec:", time_list_sec)
        #print(f"startDt: {startDt}, endDT: {self.endDt}")
        
            
        # 스케줄 등록
        for t in range(target_day.shape[0]) :        
            n = target_day.loc[t, '투자수량']                    # Define quantity
            
            if self.mock == "1": #모의 (Buy: VTTC0802U, Sell: VTTC0801U)
                if n > 0:   
                    position = 'VTTC0802U' 
                else:
                    position = 'VTTC0801U' 
                    n = -n
            else:  #실전 (TTTC0802U: 주식현금 매수주문, TTTC0801U: 주식현금 매도주문)  
                if n > 0:
                    position = 'TTTC0802U' 
                else:
                    position = 'TTTC0801U'    
                    n = -n
            
            ticker = target_day.loc[t, '종목코드']                # Define ticker 
            price  = target_day.loc[t, '현재가'] 

            # 00:지정가, 01:시장가, 03:최유리지정가, 04:최우선지정가, 05:장전시간외, 06: 장후시간외
            schedule.every().day.at(time_list_sec[t],"Asia/Seoul").do(self.trade_at_once, ticker, position, "00", n, price) 
            
            print("schedule:", time_list_sec[t], ticker, position, n, price)
        return schedule
       
    def schedule_rebalancing_06(self):  #06: 장후시간외
        
        target_day = self.rebalance_target()       #목표/투자 수량

        print(target_day)
        today = datetime.datetime.now().astimezone(self.kst_tz)

        # 06 : 장후 시간외 (15:30~16:00)
        # 05: 장전시간외(08:30-8:40. 8:20부터 주문가능). 전일종가 15시40분
        startDt = datetime.datetime.now().astimezone(self.kst_tz).replace(hour=15,minute=40,second=10,microsecond=0)
        self.endDt = datetime.datetime.now().astimezone(self.kst_tz).replace(hour=15,minute=40,second=40,microsecond=0)
        
        schedule.clear() # 스케줄 초기화

        time_list = pd.date_range(startDt, self.endDt, periods = target_day.shape[0])    
        time_list = time_list.round(freq = 's').tolist()    
        time_list_sec = [s.strftime('%H:%M:%S') for s in time_list]      
        print("time_list_sec:", time_list_sec)
        #print(f"startDt: {startDt}, endDT: {self.endDt}")
        
            
        # 스케줄 등록
        for t in range(target_day.shape[0]) :        
            n = target_day.loc[t, '투자수량']                    # Define quantity
            
            if self.mock == "1": #모의 (Buy: VTTC0802U, Sell: VTTC0801U)
                if n > 0:   
                    position = 'VTTC0802U' 
                else:
                    position = 'VTTC0801U' 
                    n = -n
            else:  #실전 (TTTC0802U: 주식현금 매수주문, TTTC0801U: 주식현금 매도주문)  
                if n > 0:
                    position = 'TTTC0802U' 
                else:
                    position = 'TTTC0801U'    
                    n = -n
            
            ticker = target_day.loc[t, '종목코드']                # Define ticker 
            price  = target_day.loc[t, '현재가'] 

            # 00:지정가, 01:시장가, 03:최유리지정가, 04:최우선지정가, 05:장전시간외, 06: 장후시간외
            schedule.every().day.at(time_list_sec[t],"Asia/Seoul").do(self.trade_at_once, ticker, position, "06", n, price) 
            
            print("schedule:", time_list_sec[t], ticker, position, n, price)
        return schedule
       
    # 스케줄 실행
    def execute(self):
        while True:
            schedule.run_pending()    
            if datetime.datetime.now().astimezone(self.kst_tz) > self.endDt :
                print('거래가 완료되었습니다')        
                schedule.clear()
                break

  