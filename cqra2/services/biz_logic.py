from datetime import datetime, date
import numpy as np
import pandas as pd
import quantstats as qs

from cqra2.services.MP_gen import CQRA 


def run_cqra2_mp (ty):  

    # ticker [국고채3년, 단기채권, 단기통안채, kosdq, KOSPI, NASDAQ, S&P]
    tic = [ "114260.KS", "153130.KS", "157450.KS","229200.KS", "278530.KS", "379810.KS", "379800.KS"] 

    stock_data = CQRA (tic) 

    fromdate = "2021-04-05"
    todate = date.today().strftime("%Y-%m-%d")    
    data = stock_data.download_data(fromdate, todate,'1d') 
    data.Close.dropna(thresh = 6)
    df,ret = stock_data.clean()

    # odd_stock_w, odd_bond_w, even_stock_w, even_bond_w, even_passive_stock_w, even_passive_bond_w
    values = { 
        5: (1, 0, 1, 0, 1, 0),                  #공격형
        4: (0.7, 0.3, 0.7, 0.3, 0.7, 0.3),      #적극형
        3: (0.5, 0.5, 0.5, 0.5, 0.5, 0.5),      #중립형
        2: (0.3, 0.7, 0.3, 0.7, 0.3, 0.7),      #안정형
    }
    
    # Retrieve values based on ty
    odd_stock_w, odd_bond_w, even_stock_w, even_bond_w, even_passive_stock_w, even_passive_bond_w = values.get(ty, (None, None, None, None, None, None))

    #Bond, cash, mmf, kosdaq, KOSPI, NASDAQ, S&P
    #홀수11-4월 (코스닥60, 코스피40). 홀수 5-10월(나스닥50,S&P50)
    #짝수11-4월 (코스닥50, 코스피50). 짝수 5-10월(나스닥50,S&P50)
    odd_buy = np.array([(1/3*odd_bond_w), (1/3*odd_bond_w), (1/3*odd_bond_w), 0.6*odd_stock_w, 0.4*odd_stock_w, 0.0*odd_stock_w, 0.0*odd_stock_w])          # Even 11 - Odd 4. Active
    odd_hold = np.array([(1/3*odd_bond_w), (1/3*odd_bond_w), (1/3*odd_bond_w), 0.0*odd_stock_w, 0.0*odd_stock_w, 0.5*odd_stock_w, 0.5*odd_stock_w])         # Odd 5 - Odd 10. 
    even_buy = np.array([(1/3*even_bond_w), (1/3*even_bond_w), (1/3*even_bond_w), 0.5*even_stock_w, 0.5*even_stock_w, 0.0*even_stock_w, 0.0*even_stock_w])  # Odd 11 - Even 4. NOTE: Here, we shift Kospi weight to Nasdaq instead of S&P 500 to be consistent with our logic that 11-4 should be more aggressive than 5-10. 
    even_hold = np.array([(1/3*even_passive_bond_w), (1/3*even_passive_bond_w), (1/3*even_passive_bond_w), 0.0*even_passive_stock_w, 0.0*even_passive_stock_w, 0.5*even_passive_stock_w, 0.5*even_passive_stock_w])  # Even 5 - Even 10

    halloween_adj = stock_data.algo2(1000,odd_buy,odd_hold,even_buy,even_hold) #시큐라2 호출
    stock_data.results()[0]
    stock_data.results()[1]

    # 1. 일별수익률추이
    destination_file_path = rf'cqra2/templates/{ty}_일별수익률추이.csv'
    daily_ret = stock_data.daily_ret() 
    daily_ret.to_csv(destination_file_path)

    # 2. 월별수익률추이
    destination_file_path = rf'cqra2/templates/{ty}_월별수익률추이.csv'
    monthly_ret = stock_data.monthly_ret() 
    monthly_ret.to_csv(destination_file_path)
    
    # 3. 자산별투자비중추이
    destination_file_path = rf'cqra2/templates/{ty}_자산별투자비중추이.csv'   
    port_weights = stock_data.portfolio_by_asset_class() 
    port_weights = port_weights[1]
    port_weights.to_csv(destination_file_path)
    
    # 4. 종목별투자비중추이
    destination_file_path = rf'cqra2/templates/{ty}_종목별투자비중추이.csv'  
    cls_weight=stock_data.portfolio_by_ind_assets() 
    cls_weight.to_csv(destination_file_path)

    stock = daily_ret.iloc[:,9]  
    return stock


def run_cqra2_rpt(ty,df): 

    import warnings
    warnings.simplefilter(action='ignore', category=FutureWarning)

    qs.extend_pandas()
    html_file_path = rf'cqra2/templates/cqra2/cqra2_ty{ty}.html'

    qs.reports.html(df, benchmark="SPY", mode='basic', output=html_file_path, title=f'CQRA Type{ty} Performance Report')


def run_cqra2_range_rpt(type, df):  

    df['date'] = pd.to_datetime(df['date'])
    df['port_ret'] = pd.to_numeric(df['port_ret'], errors='coerce')

    stock  = df[['date', 'port_ret']].set_index('date')
    stock  = stock.sort_index()
                
    import warnings
    warnings.simplefilter(action='ignore', category=FutureWarning)

    qs.extend_pandas()
    html_file_path = rf'cqra2/templates/cqra2/cqra2_range_ty{type}.html'
    qs.reports.html(stock ['port_ret'], benchmark="SPY", mode='basic', output=html_file_path, title=f'CQRA Type{type} Performance Report')

    return html_file_path  
