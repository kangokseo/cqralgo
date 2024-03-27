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

    def __init__(self, key_name, secret_name, ID, mock, cano):

        path = "oauth2/tokenP"
        if mock == "1":
            self.url_base = "https://openapivts.koreainvestment.com:29443" # 모의투자
        else:
            self.url_base = "https://openapi.koreainvestment.com:9443" # 실전 투자  
        
        url = f"{self.url_base}/{path}"

        self.app_key = keyring.get_password(key_name, ID)
        self.app_secret = keyring.get_password(secret_name, ID)

        headers = {"content-type": "application/json"}
        body = {
            "grant_type": "client_credentials",
            "appkey": self.app_key,
            "appsecret": self.app_secret
        }
        res = requests.post(url, headers=headers, data=json.dumps(body))
        time.sleep(0.1)

        self.ID = ID
        self.mock = mock
        self.cano = cano
        self.kst_tz = pytz.timezone('Asia/Seoul') # timezone 

        self.mp1 = pd.DataFrame({   # 포트폴리오 Define. 
            '종목코드': [
                "069500", #KODEX 200
                "229200", #KODEX 코스닥150
                "133690", #TIGER 미국나스닥100
                "143850", #TIGER 미국S&P500선물(H)
                "114260", #KODEX 국고채3년
                "153130", #KODEX 단기채권
                "157450", #TIGER 단기통안채
            ],
            '이름': ["KODEX 200", "KODEX 코스닥150", "TIGER 미국나스닥100", "TIGER 미국S&P500선물(H)", 
                "KODEX 국고채3년", "KODEX 단기채권", "TIGER 단기통안채"],
            '홀수 비중 11-4': [1*0.4, 1*0.6, 1*0.0, 1*0.0, 0*(1/3), 0*(1/3), 0*(1/3)],
            '홀수 비중 5-10': [1*0, 1*0, 1*0.5, 1*0.5, 0*(1/3), 0*(1/3), 0*(1/3)],
            '짝수 비중 11-4': [1*0.4, 1*0.6, 1*0.0, 1*0.0, 0*(1/3), 0*(1/3), 0*(1/3)],
            '짝수 비중 5-10': [1*0.0, 1*0.0, 1*0.5, 1*0.5, 0*(1/3), 0*(1/3), 0*(1/3)]
        })

        print("json:", res.json())

        self.access_token = res.json()['access_token']      
        self.access_token_token_expired = res.json()['access_token_token_expired']      
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

        if self.mock == "1": #mock
            tr_id = "VTTC8434R"
        else:
            tr_id = "TTTC8434R" # 실전 

        while True:
            path = "/uapi/domestic-stock/v1/trading/inquire-balance"
            url = f"{self.url_base}/{path}"

            headers = {
                "Content-Type": "application/json",
                "authorization": f"Bearer {self.access_token}",
                "appKey": self.app_key,
                "appSecret": self.app_secret,
                "tr_id": tr_id
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
            print("json:", res.json())

            output1.append(pd.DataFrame.from_records(res.json()['output1']))

            CTX_AREA_NK100 = res.json()['ctx_area_nk100'].strip()

            if CTX_AREA_NK100 == '':
                output2.append(res.json()['output2'][0])
                break

        if not output1[0].empty:
            res1 = pd.concat(output1)[['pdno',
                                    'hldg_qty']].rename(columns={
                                        'pdno': '종목코드',
                                        'hldg_qty': '보유수량'
                                    }).reset_index(drop=True)
        else:
            res1 = pd.DataFrame(columns=['종목코드', '보유수량'])

        res2 = output2[0]

        return [res1, res2]

   # 투자 알고리즘에 의한 리벨런싱을 위한 투자수량 계산. 
    def main(self): 
        # 보유 종목과 aum 불러오기
        ap, account = self.check_account()

        # 매매 구성
        target = self.mp1.merge(ap, on='종목코드', how='outer')
        target['보유수량'] = target['보유수량'].fillna(0).apply(pd.to_numeric)

        # 현재가 확인
        target['현재가'] = target.apply(lambda x: self.get_price(x.종목코드), axis=1)

        # 날짜
        kst_tz = pytz.timezone('Asia/Seoul')
        today = datetime.datetime.now().astimezone(kst_tz)

        if (target['보유수량'] == 0).all(): 
            # 진입
            weights = target['홀수 비중 11-4']  # Note: Change here. weight = input
            
        else: 
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
    

    # 수량 지정가능 주문
    def trading_at_once(self, ticker, tr_id, trade_type, qty, price):

        path = "uapi/domestic-stock/v1/trading/order-cash"
        url = f"{self.url_base}/{path}"

        data = {
            "CANO": self.cano, # 계좌번호 앞 8지리
            "ACNT_PRDT_CD": "01",
            "PDNO": ticker,     # 종목코드
            "ORD_DVSN": trade_type,   # 주문 방법     NOTE: Change type of transaction here. 
            "ORD_QTY": str(int(qty)),     # 주문 수량
            "ORD_UNPR": "0" #"0" if trade_type == "01" else str(int(price))   # 주문 단가 (시장가의 경우 0)
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

        res = requests.post(url, headers=headers, data=json.dumps(data)) 
        print("result:", res.json())

        return schedule.CancelJob
    
    # 한종목당 한꺼번에 주문 넣으려면 rebalancing_trade_at_once(). 책대로 한종목당 한주씩 주문 넣으려면 rebalancing().
    # 리벨런싱 스케줄 추가. (모든 수량 한꺼번에) 
    def rebalancing_trade_at_once(self):
        
        target_day = self.main()       

        print(target_day)
        today = datetime.datetime.now().astimezone(self.kst_tz)

        # 시간 분할. 시스템 실행 시간 9:10AM - 3:00PM. 
        startDt1 = datetime.datetime.now().astimezone(self.kst_tz) + timedelta(minutes=1)
        startDt2 = datetime.datetime.now().astimezone(self.kst_tz).replace(hour=9,minute=10,second=0,microsecond=0)
        startDt = max(startDt1, startDt2)
        self.endDt = datetime.datetime.now().astimezone(self.kst_tz).replace (hour=15,minute=36,second=0,microsecond=0)
        
        schedule.clear() # 스케줄 초기화

        time_list = pd.date_range(startDt, self.endDt, periods = target_day.shape[0])    
        time_list = time_list.round(freq = 's').tolist()    
        time_list_sec = [s.strftime('%H:%M:%S') for s in time_list]      

        print(f"startDt: {startDt}, endDT: {self.endDt}")
        print("time_list_sec:", time_list_sec)
            
        # 스케줄 등록
        for t in range(target_day.shape[0]) :        
            n = target_day.loc[t, '투자수량']                    # Define quantity
            
            if self.mock == "1": #mock
                position = 'VTTC0802U' if n > 0 else 'VTTC0801U' #모의 (Sell: VTTC0802U or Buy: VTTC0802U)
            else:
                position = 'TTTC0802U' if n > 0 else 'TTTC0801U' #실전        
            
            ticker = target_day.loc[t, '종목코드']                # Define ticker 
            price  = target_day.loc[t, '현재가'] 

            schedule.every().day.at(time_list_sec[t],"Asia/Seoul").do(self.trading_at_once, ticker, position, "06", n, price) # 01:시장가, 03:최유리지정가, 04:최우선지정가
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

   # 주문
    # def trading(self, ticker, tr_id, trade_type):
    #     # tr_id [실전투자]TTTC0802U :주식현금매수주문,TTTC0801U:주식현금매도 문, [모의투자]VTTC0802U:주식현금매수주문,VTTC0801U:주식현금매도주문
    #     # trade_type:주문방법 (00:지정가, 01:시장가, 02:조건부지정가,03:최유리지정가, 06:장후시간외(15:30~16:00), 07:시간외단일가(16:00~18:00))
    #     # custtype: B : 법인, P : 개인

    #     path = "/uapi/domestic-stock/v1/trading/order-cash"
    #     url = f"{self.url_base}/{path}"

    #     data = {
    #        # "CANO": "50102559", # 계좌번호 앞 8지리
    #         "CANO": self.cano,
    #         "ACNT_PRDT_CD": "01",
    #         "PDNO": ticker,     # 종목코드
    #         "ORD_DVSN": trade_type,  # (00:지정가, 01:시장가)
    #         "ORD_QTY": "1",     # 주문 수량
    #         "ORD_UNPR": "0",    # 주문 단가 (시장가의 경우 0)
    #     }
    #     headers = {
    #         "Content-Type": "application/json",
    #         "authorization": f"Bearer {self.access_token}",
    #         "appKey": self.app_key,
    #         "appSecret": self.app_secret,
    #         "tr_id": tr_id, 
    #         "custtype": "P",
    #         "hashkey": self.hashkey(data)
    #     }

    #     res = requests.post(url, headers=headers, data=json.dumps(data)) 
    #     return schedule.CancelJob

        
    # # 실제 리벨런싱 스케줄 추가. 
    # def rebalancing(self):
    #     # Rebalancing weights
    #     target_day = self.main()
    #     print(target_day)

    #     today = datetime.datetime.now().astimezone(self.kst_tz)

    #     # 시간 분할. 시스템 실행 시간 9:10AM - 3:00PM. 
    #     startDt1 = datetime.datetime.now().astimezone(self.kst_tz) + timedelta(minutes=1)
    #     startDt2 = datetime.datetime.now().astimezone(self.kst_tz).replace(hour=9,minute=10,second=0,microsecond=0)
    #     startDt = max(startDt1, startDt2)
    #     self.endDt = datetime.datetime.now().astimezone(self.kst_tz).replace(hour=15,minute=0,second=0,microsecond=0)

    #     # 스케줄 초기화
    #     schedule.clear()

    #     # 스케줄 등록
    #     for t in range(target_day.shape[0]) :
            
    #         n = target_day.loc[t, '투자수량']                    # Define quantity
    #         position = 'VTTC0802U' if n > 0 else 'VTTC0801U' # Sell: VTTC0802U or Buy: VTTC0802U
    #         ticker = target_day.loc[t, '종목코드']                # Define ticker 

    #         time_list = pd.date_range(startDt, self.endDt, periods = abs(n))    
    #         time_list = time_list.round(freq = 's').tolist()    
    #         time_list_sec = [s.strftime('%H:%M:%S') for s in time_list]                 

    #         for i in time_list_sec:
    #             schedule.every().day.at(i,"Asia/Seoul").do(self.trading, ticker, position, "01") 
    #             # 01:시장가, 06:장후시간외(15:30~16:00), 07:시간외단일가(16:00~18:00)
