import keyring
import requests
import json
import pandas as pd

def get_app_key():
    keyring.set_password('real_app_key', 'kannie', 'PSnvAltwjE5ZrOaITkVgetxCutSSexVH4qEw')
    keyring.set_password('real_app_secrect', 'kannie', 'LLhGO6tUDaepjBRFtocxjcYPZbkLfR5mKRFJrPccIkOBVfLsUhkVMFNWy7h7bWAD4CSq3nPowAYX/MMocSI9MAXrbNximason8X8V44iWkrrH/+IJT7E8CAN6fiCQwcnuHLZi/ryI/AzgHLHxwf56cCj/jEMtjrvxf6aITV5WrzSSmYLNOg=')

    keyring.set_password('mock_app_key', 'kannie', 'PSnwe2lboWhKABz4afYQUf5Cnm0x6IlBxt6F')
    keyring.set_password('mock_app_secret', 'kannie', 'zFilo09//IcL6SKcVd+VHCxiGuhmVhu+llV1emGjL+J202Y9w1hxyFszqhvzBXjcM34t3QTULxOxM5heeVPCJJQSTSaiZEYMHXyddWCaLVwZiT93dpzgwfnOC0Stc1pmvlxbBAzux5ASV+hZuiYAZ6KTYKxexelADUlR3mIBDbeNfBkNuiw=')

    app_key = keyring.get_password('mock_app_key', 'kannie')
    get_app_key = app_key

    return get_app_key
    
def get_app_secret():
    keyring.set_password('real_app_key', 'kannie', 'PSnvAltwjE5ZrOaITkVgetxCutSSexVH4qEw')
    keyring.set_password('real_app_secrect', 'kannie', 'LLhGO6tUDaepjBRFtocxjcYPZbkLfR5mKRFJrPccIkOBVfLsUhkVMFNWy7h7bWAD4CSq3nPowAYX/MMocSI9MAXrbNximason8X8V44iWkrrH/+IJT7E8CAN6fiCQwcnuHLZi/ryI/AzgHLHxwf56cCj/jEMtjrvxf6aITV5WrzSSmYLNOg=')

    keyring.set_password('mock_app_key', 'kannie', 'PSnwe2lboWhKABz4afYQUf5Cnm0x6IlBxt6F')
    keyring.set_password('mock_app_secret', 'kannie', 'zFilo09//IcL6SKcVd+VHCxiGuhmVhu+llV1emGjL+J202Y9w1hxyFszqhvzBXjcM34t3QTULxOxM5heeVPCJJQSTSaiZEYMHXyddWCaLVwZiT93dpzgwfnOC0Stc1pmvlxbBAzux5ASV+hZuiYAZ6KTYKxexelADUlR3mIBDbeNfBkNuiw=')

    app_secret = keyring.get_password('mock_app_secret','kannie')
    get_app_secret = app_secret

    return get_app_secret

def get_ak (app_key, app_secret):

    url_base = "https://openapivts.koreainvestment.com:29443" #모의투자
    path = "oauth2/tokenP"
    headers ={"content-type":"application/json"}
    body = {
        "grant_type": "client_credentials",
        "appkey": app_key,
        "appsecret": app_secret,
    }

    url = f"{url_base}/{path}"
    res = requests.post(url, headers=headers, data=json.dumps(body))
    

    access_token = res.json()['access_token']
    
    return str(access_token)

def checkbalance(app_key, app_secret, access_token):
    url_base = "https://openapivts.koreainvestment.com:29443" #모의투자
    path = "/uapi/domestic-stock/v1/trading/inquire-balance"
    url = f"{url_base}/{path}"

    headers = {
        "Content-Type": "application/json",
        "authorization": f"Bearer {access_token}",
        "appKey": app_key,
        "appSecret": app_secret,
        "tr_id": "VTTC8434R"
    }

    params = {
        "CANO": "50102070",  # 계좌번호 앞 8지리
        "ACNT_PRDT_CD": "01",  # 계좌번호 뒤 2자리
        "AFHR_FLPR_YN": "N",  # 시간외단일가여부
        "OFL_YN": "",  # 공란
        "INQR_DVSN": "01",  # 조회구분
        "UNPR_DVSN": "01",  # 단가구분
        "FUND_STTL_ICLD_YN": "N",  # 펀드결제분포함여부
        "FNCG_AMT_AUTO_RDPT_YN": "N",  # 융자금액자동상환여부        
        "PRCS_DVSN": "00",  # 처리구분(00: 전일매매포함)
        "CTX_AREA_FK100": "",  # 연속조회검색조건
        "CTX_AREA_NK100": ""  # 연속조회키
    }

    res = requests.get(url, headers=headers, params=params)

    res.json()['output2']

    checkbalance=pd.DataFrame.from_records(res.json()['output2'])

    return checkbalance



# def hashkey(datas):
#     path="uapi/hashkey"
#     url = f"{url_base}/{path}"
#     headers = {
#         'content-Type': 'application/json',
#         'appKey': app_key,
#         'appSecret': app_secret,
#     }
#     res = requests.post(url, headers=headers, data=json.dumps(datas))
#     hashkey = res.json()["HASH"]
#     return hashkey

#현재가 조회
# path = "uapi/domestic-stock/v1/quotations/inquire-price"
# url = f"{url_base}/{path}"

# headers = {
#     "Content-Type": "application/json",
#     "authorization": f"Bearer {access_token}",
#     "appKey": app_key,
#     "appSecret": app_secret,
#     "tr_id": "FHKST01010100"
# }

# params = {"fid_cond_mrkt_div_code": "J", "fid_input_iscd": "035420"} #005930 삼성전자. 035420 네이버

# res = requests.get(url, headers=headers, params=params)
# res.json()['output']['stck_prpr']
 
# a=res.json()['output']['stck_prpr']
# print(a)
##

#계좌조회

def checkbalance(app_key, app_secret, access_token):
    url_base = "https://openapivts.koreainvestment.com:29443" #모의투자
    path = "/uapi/domestic-stock/v1/trading/inquire-balance"
    url = f"{url_base}/{path}"

    headers = {
        "Content-Type": "application/json",
        "authorization": f"Bearer {access_token}",
        "appKey": app_key,
        "appSecret": app_secret,
        "tr_id": "VTTC8434R"
    }

    params = {
        "CANO": "50102070",  # 계좌번호 앞 8지리
        "ACNT_PRDT_CD": "01",  # 계좌번호 뒤 2자리
        "AFHR_FLPR_YN": "N",  # 시간외단일가여부
        "OFL_YN": "",  # 공란
        "INQR_DVSN": "01",  # 조회구분
        "UNPR_DVSN": "01",  # 단가구분
        "FUND_STTL_ICLD_YN": "N",  # 펀드결제분포함여부
        "FNCG_AMT_AUTO_RDPT_YN": "N",  # 융자금액자동상환여부        
        "PRCS_DVSN": "00",  # 처리구분(00: 전일매매포함)
        "CTX_AREA_FK100": "",  # 연속조회검색조건
        "CTX_AREA_NK100": ""  # 연속조회키
    }

    res = requests.get(url, headers=headers, params=params)

    res.json()['output2']

    checkbalance=pd.DataFrame.from_records(res.json()['output2'])

    return checkbalance

