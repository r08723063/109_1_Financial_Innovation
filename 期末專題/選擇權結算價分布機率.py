def third_wen(y,m):#算當月結算日
    import datetime as dt
    day=21-(dt.date(y,m,1).weekday()+4)%7         #   weekday函數 禮拜一為0;禮拜日為6
    return y,m,day


def get_left_day(year,month,day):
    import datetime as dt
    
    if third_wen(year,month)[2] > day and month != 12:
        left_day_ = dt.date(int(third_wen(year,month)[0]),int(third_wen(year,month)[1]),int(third_wen(year,month)[2])) - dt.date(year,month,day)
    elif third_wen(year,month)[2] > day and month == 12:
        left_day_ = dt.date(int(third_wen(year,month)[0]),int(third_wen(year,month)[1]),int(third_wen(year,month)[2])) - dt.date(year,month,day)
    elif third_wen(year,month)[2] <= day and month != 12:
        left_day_ = dt.date(int(third_wen(year,month+1)[0]),int(third_wen(year,month+1)[1]),int(third_wen(year,month+1)[2])) - dt.date(year,month,day)
    elif third_wen(year,month)[2] <= day and month == 12:
        left_day_ = dt.date(int(third_wen(year+1,1)[0]),int(third_wen(year+1,1)[1]),int(third_wen(year+1,1)[2])) - dt.date(year,month,day)
        
    #print(str(left_day.days))
    return int(str(left_day_.days))


def craw_new_data(year,month,date):
    import requests
    import pandas as pd
    from bs4 import BeautifulSoup
    import numpy
    import csv
    import time

            
    info = f'{year}/{month}/{date}'
    url = 'https://www.taifex.com.tw/cht/3/optDailyMarketReport'
    payload = {'queryType':'2',
               'marketCode':'0',
               'dateaddcnt':'',
               'commodity_id':'TXO',
               'commodity_id2':'',
               'MarketCode':'0',
               'commodity_idt':'TXO',
               'commodity_id2t':'',
               'commodity_id2t2':'',
               'queryDate':info
              }
    encoding = 'utf8'
    r = requests.post(url,data=payload)
    r.encoding = encoding
    soup = BeautifulSoup(r.content, 'html.parser')

    data = pd.DataFrame(columns=['契約','到期月份(週別)','履約價','買賣權','開盤價','最高價','最低價','最後成交價','結算價','盤後交易時段成交量','一般交易時段成交量','合計成交量','未沖銷契約量'])
    append_list = {}
    count = 0
    for i in soup.find_all('tr'):
        for j in i.find_all('td',class_ = '12bk'):
            count+=1
            if count > 18:
                if (count-18)%13 == 0:
                    data = data.append(append_list, ignore_index=True)
                    append_list = {}
                    append_list['契約'] = j.text.replace('\n','').replace(' ','').replace('\t','').replace('\r','')
                elif (count-18)%13 == 1:
                    append_list['到期月份(週別)'] = j.text.replace('\n','').replace(' ','').replace('\t','').replace('\r','')
                elif (count-18)%13 == 2:
                    append_list['履約價'] = j.text.replace('\n','').replace(' ','').replace('\t','').replace('\r','')
                elif (count-18)%13 == 3:
                    append_list['買賣權'] = j.text.replace('\n','').replace(' ','').replace('\t','').replace('\r','')
                elif (count-18)%13 == 4:
                    append_list['開盤價'] = j.text.replace('\n','').replace(' ','').replace('\t','').replace('\r','')
                elif (count-18)%13 == 5:
                    append_list['最高價'] = j.text.replace('\n','').replace(' ','').replace('\t','').replace('\r','')
                elif (count-18)%13 == 6:
                    append_list['最低價'] = j.text.replace('\n','').replace(' ','').replace('\t','').replace('\r','')
                elif (count-18)%13 == 7:
                    append_list['最後成交價'] = j.text.replace('\n','').replace(' ','').replace('\t','').replace('\r','')
                elif (count-18)%13 == 8:
                    append_list['結算價'] = j.text.replace('\n','').replace(' ','').replace('\t','').replace('\r','')
                elif (count-18)%13 == 9:
                    append_list['盤後交易時段成交量'] = j.text.replace('\n','').replace(' ','').replace('\t','').replace('\r','')
                elif (count-18)%13 == 10:
                    append_list['一般交易時段成交量'] = j.text.replace('\n','').replace(' ','').replace('\t','').replace('\r','')
                elif (count-18)%13 == 11:
                    append_list['合計成交量'] = j.text.replace('\n','').replace(' ','').replace('\t','').replace('\r','')
                elif (count-18)%13 == 12:
                    append_list['未沖銷契約量'] = j.text.replace('\n','').replace(' ','').replace('\t','').replace('\r','')

    data.to_csv(f'option_data_{year}_{month}_{date}.csv',index=False,encoding='cp950')


def detect_lastest_data(year,month,date):
    from os import listdir
    mypath = "./"
    files = listdir(mypath)
    if f'option_data_{year}_{month}_{date}.csv' in files:
        return True
    elif f'option_data_{year}_{month}_{date}.csv' not in files:
        return False


def distr_formula(r,k1,k2,k3,left_day,distance):#johnhull公式
    import math
    from scipy import integrate
    c1 = float(k1)
    c3 = float(k3)
    c2 = float(k2)
    T = left_day/365
    g = (math.exp(r*T))*(c1  + c3 - 2*c2)/(distance)
    return g


def process_df(year,month,date):#載入資料
    import pandas as pd
    import xlrd
    data = pd.read_csv(f'option_data_{year}_{month}_{date}.csv',encoding='cp950')
    #data = data[data['交易時段']!='盤後']

    if third_wen(year,month)[2] > date and month != 12:
        month = str(month).rjust(2,'0')
        data = data[data['到期月份(週別)'] == f'{year}{month}']
        data = data.reset_index()
        del data['index']
    elif third_wen(year,month)[2] > date and month == 12:
        month = str(month).rjust(2,'0')
        data = data[data['到期月份(週別)'] == f'{year}{month}']
        data = data.reset_index()
        del data['index']
    elif third_wen(year,month)[2] <= date and month != 12:
        month = str(month+1).rjust(2,'0')
        data = data[data['到期月份(週別)'] == f'{year}{month}']
        data = data.reset_index()
        del data['index']
    elif third_wen(year,month)[2] <= date and month == 12:
        data = data[data['到期月份(週別)'] == f'{year+1}01']
        data = data.reset_index()
        del data['index']
    #data_process = data[data['Unnamed: 0']== f'{year}/{month}/{date}']
    data_buy = data[data['買賣權']=='Call']
    data_buy = data_buy.reset_index()
    del data_buy['index']
    data_sell = data[data['買賣權']=='Put']
    data_sell = data_sell.reset_index()
    del data_sell['index']
    data_buy['結算價'] = [float(x) for x in data_buy['結算價']]
    data_sell['結算價'] = [float(x) for x in data_sell['結算價']]
    k = data_sell['履約價']
    
    return data_buy,data_sell,k#回傳買權、賣權表格跟K是履約價數列


def get_future_price(year,month,date):#尋找當日小台期貨收盤價
    import pandas as pd
    import xlrd
    import requests
    from bs4 import BeautifulSoup
    import numpy
    import csv
    
    info = f'{year}/{month}/{date}'
    url = 'https://www.taifex.com.tw/cht/3/futDailyMarketReport'
    payload = {'queryType':'2',
               'marketCode':'0',
                'dateaddcnt':'',
                'commodity_id':'MTX',
                'commodity_id2':'',
                'MarketCode':'0',
                'commodity_idt':'MTX',
                'commodity_id2t':'',
                'commodity_id2t2':'',
                'queryDate':info
                }
    encoding = 'utf8'
    r = requests.post(url,data=payload)
    r.encoding = encoding
    soup = BeautifulSoup(r.content, 'html.parser')
    a = []
    for i in soup.find_all('tr'):
        for j in i.find_all('td',class_ = '12bk'):
            a.append(j.text.replace('\n','').replace('\t','').replace(' ',''))
    print(f'期貨收盤價為{int(a[24])}')
    return int(a[24])
    #data = pd.read_csv('future_test.csv',encoding='cp950')
    #data = data[data['交易時段']!='盤後']
    #data = data[data['到期月份(週別)'] == f'{year}{month}']
    #data = data.reset_index()
    #del data['index']
    #data = data[data['Unnamed: 0']== f'{year}/{month}/{date}']
    #return int(data['結算價'])


def correct_IV_put(futures_price,data_sell,left_day,k):#修正put的隱波
    import mibian
    import pandas as pd
    import numpy as np
    import statsmodels.api as sm
    
    IV_sell = []
    for i in range(len(data_sell)):
        try:
            #先用真實價格套入BS模型回推隱波
            a = mibian.BS([futures_price, float(data_sell['履約價'][i]), 0.003, left_day], putPrice= float(data_sell['結算價'][i]))
            IV_sell.append(a.impliedVolatility)
        except:
            pass
    weights_sell = np.polyfit(k, IV_sell, 6)#用6次式回歸修正
    model_sell = np.poly1d(weights_sell)
    b = list(range(min(data_sell['履約價']),max(data_sell['履約價'])+100,100))
    pred_sell = model_sell(b)#套回修正過的回歸式回傳新的隱波
    
    return pred_sell, b#回傳


def correct_IV_call(futures_price,data_buy,left_day,k):#修正call的隱波
    import mibian
    import pandas as pd
    import numpy as np
    import statsmodels.api as sm
    
    IV_buy = []
    for i in range(len(data_buy)):
        try:
            #先用真實價格套入BS模型回推隱波
            a = mibian.BS([futures_price, float(data_buy['履約價'][i]), 0.003, left_day], callPrice= float(data_buy['結算價'][i]))
            IV_buy.append(a.impliedVolatility)
        except:
            pass
    weights_buy = np.polyfit(k, IV_buy, 6)#用6次式回歸修正
    model_buy = np.poly1d(weights_buy)
    b = list(range(min(data_buy['履約價']),max(data_buy['履約價'])+100,100))
    pred_buy = model_buy(b)#套回修正過的回歸式回傳新的隱波
    
    return pred_buy, b


def predict_call_price(futures_price,data_buy,left_day,k):#修正新的call價格
    import mibian
    import pandas as pd
    import numpy as np
    import statsmodels.api as sm
    
    pred_buy, b = correct_IV_call(futures_price,data_buy,left_day,k)#先尋找修正後的call隱波
    whole_buy_price = []
    for i in range(len(b)):
        #用修正後的隱波套入BS模型得到價格並回傳
        call_price = mibian.BS([futures_price,b[i],0.3,left_day],pred_buy[i]).callPrice
        whole_buy_price.append(call_price)
    return whole_buy_price


def predict_put_price(futures_price,data_sell,left_day,k):#修正新的put價格
    import mibian
    import pandas as pd
    import numpy as np
    import statsmodels.api as sm
    
    pred_sell,b = correct_IV_put(futures_price,data_sell,left_day,k)#先尋找修正後的put隱波
    whole_sell_price = []
    for i in range(len(b)):
        #用修正後的隱波套入BS模型得到價格並回傳
        put_price = mibian.BS([futures_price,b[i],0.3,left_day],pred_sell[i]).putPrice
        whole_sell_price.append(put_price)
    return whole_sell_price


def turn_k_into_return(k,futures_price):#轉換履約價成小台期的報酬率
    a = []
    for i in k:
        a.append(float((i-futures_price)/futures_price))
    return a


def produce_pic(left_day,whole_buy_price,whole_sell_price,k,month,date,futures_price):
    import matplotlib.pyplot as plt
    #先來把put_johnhull一下
    r = 0.0003
    k1 = list(whole_sell_price[0:len(whole_sell_price)-2])
    k2 = list(whole_sell_price[1:len(whole_sell_price)-1])
    k3 = list(whole_sell_price[2:len(whole_sell_price)])
    ans1 = []
    for i in range(len(k1)):
        #distance = (k[i+2]-k[i])/2  #抓johnhull的分母
        #print(f'distance:{distance}')
        #if distance == 75:
        #distance = 100
        a = distr_formula(r=r,k1=k1[i],k3=k3[i],k2=k2[i],left_day=left_day,distance=100)
        if a < 0:
            a = 0
        ans1.append(a)
        #print(f'k1:{k1[i]} k2:{k2[i]} k3:{k3[i]}')
        
    #print('----------------')
    
    plt.figure(figsize = (20,10))
    plt.title(f'{month}/{date} put/call mix', fontsize = 25)
    #plt.plot(k,ans1,'s-',color = 'g', label="put_option")
    
    #再把call_johnhull一下
    k1 = list(whole_buy_price[0:len(whole_buy_price)-2])
    k2 = list(whole_buy_price[1:len(whole_buy_price)-1])
    k3 = list(whole_buy_price[2:len(whole_buy_price)])
    ans2 = []
    for i in range(len(k1)):
        #distance = (k[i+2]-k[i])/2
        #print(f'distance:{distance}')
        #if distance == 75:
            #distance = 100
        a = distr_formula(r=r,k1=k1[i],k3=k3[i],k2=k2[i],left_day=left_day,distance=100)
        if a < 0:
            a = 0
        ans2.append(a)
        #print(f'k1:{k1[i]} k2:{k2[i]} k3:{k3[i]}')
    #print('----------------')
        
    #把put跟call兩條作合併，小於當天收盤價用put，大於等於用call
    ans3 = []
    k_ = list(range(min(k)+100, max(k),100))
    #print(k_)
    for i in range(0,len(k_)):
        #print(i)
        if int(k_[i]) < int(futures_price):
            ans3.append(ans1[i])
        elif int(k_[i]) >= int(futures_price):
            ans3.append(ans2[i])
    k_ = turn_k_into_return(k_,futures_price)
    #plt.plot(k_,ans1,'s-',color = 'b', label="mix_option")
    #plt.plot(k_,ans2,'s-',color = 'r', label="mix_option")
    plt.plot(k_,ans3,'s-',color = 'y', label="mix_option")
    plt.show()


def calculate():
    import pandas as pd
    import numpy as np
    import statsmodels.api as sm
    import matplotlib.pyplot as plt
    import mibian
    import datetime as dt
    
    appoint_date = dt.date(int(comboExample1.get()),int(comboExample2.get()),int(comboExample3.get()))
    now = dt.date(int(dt.datetime.now().strftime('%Y-%m-%d-%H').split('-')[0]),int(dt.datetime.now().strftime('%Y-%m-%d-%H').split('-')[1]),int(dt.datetime.now().strftime('%Y-%m-%d-%H').split('-')[2]))
    check_if_ok = appoint_date-now
    
    if int(str((check_if_ok).days)) >= 0:
        now = dt.datetime.now()
        if int(now.strftime('%Y-%m-%d-%H').split('-')[3]) <16:
            now += dt.timedelta(days = -1)
    elif int(str((check_if_ok).days)) < 0:
        now = appoint_date

    weekday = now.weekday()
    if weekday == 5:
        now += dt.timedelta(days = -1)
    elif weekday == 6:
        now += dt.timedelta(days = -2)
    else:
        pass


    time_line = now.strftime('%Y-%m-%d').split('-')
    year = int(time_line[0])
    month = int(time_line[1])
    date_ = int(time_line[2])

    if not detect_lastest_data(year, month, date_):
        craw_new_data(year,month,date_)
    else:
        pass

    try:
    #if True:
        result_label1.configure(text='計算中請耐心稍等')
        data_buy, data_sell, k = process_df(year,month,date_)
        futures_price = get_future_price(year,month,date_)
        left_day = get_left_day(year,month,date_)
        whole_buy_price = predict_call_price(futures_price,data_buy,left_day,k)
        whole_sell_price = predict_put_price(futures_price,data_sell,left_day,k)
        produce_pic(left_day,whole_buy_price,whole_sell_price,k,month,date_,futures_price)
    except:
        result_label1.configure(text='選別天拉，那天沒交易')


import tkinter as tk
from tkinter import ttk
import pandas as pd

window = tk.Tk()
window.title('台指選擇權機率分配')
window.geometry('540x75')
window.configure(background='white')
header_label = tk.Label(window, text='台指選擇權機率分配' )
header_label.grid(column=0, row=0 ,columnspan = 4,sticky=tk.NW + tk.SE)

comboExample0_label = tk.Label(window, text='選擇日期')
comboExample0_label.grid(column=0, row=1,sticky=tk.NW + tk.SE)

comboExample1 = ttk.Combobox(window, 
                            values=[2002,2003,2004,2005,2006,2007,2008,2009,2010,
                                    2011,2012,2013,2014,2015,2016,2017,2018,2019,2020] ,state="readonly")
comboExample1.grid(column=1, row=1)
comboExample1.current(0)

comboExample2 = ttk.Combobox(window, 
                            values=[1,2,3,4,5,6,7,8,9,10,11,12] ,state="readonly")
comboExample2.grid(column=2, row=1)
comboExample2.current(0)

comboExample3 = ttk.Combobox(window, 
                             values=[1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21
                                    ,22,23,24,25,26,27,28,29,30,31] ,state="readonly")
comboExample3.grid(column=3, row=1)
comboExample3.current(0)


calculate_btn = tk.Button(window, text='開始計算', command=calculate)
calculate_btn.grid(column=3, row=3,sticky=tk.NW+ tk.SE,columnspan =4)

result_label1 = tk.Label(window)
result_label1.grid(column=0, row=3,sticky=tk.NW+ tk.SE,columnspan =3)

window.mainloop()




