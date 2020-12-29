import datetime
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import tkinter as tk
from tkinter import ttk


data = pd.read_csv("TXF1.txt")  # 台指期資料位置
data.columns = ['Date','Time','Open','High','Low','Close','Volume']
data["datetime"]=0 # 日期
data['moving_avg']=0 # 均線的價格
data['moving_avg_updown']=0 # 收盤在該均線上或下
data['up_down']=0 # 當日漲或跌
data['end_price']=0  # 持有到結束時的收盤價
data['reture_percent']=0 # 報酬率


def printblank():  # 視窗顯示時 清空內容用
    result_label1.configure(text='')
    result_label2.configure(text='')
    result_label3.configure(text='')
    result_label4.configure(text='')
    result_label5.configure(text='')
    result_label7.configure(text='')
    result_label8.configure(text='')
    
    
    
def calculate():  # 真實計算內容皆放於此
    

    temp_do = 0  # 暫存用,當為0時表示可以計算回測
    holddays = 1  # 持有天數 預設1
    moving_avg = 1   # 均線濾網長度 預設1
    moving_avg_updown = int(Value1.get())  #0不篩選 1為篩選收均線以上 -1為篩選收均線以下
    up_down = int(Value.get())  # 0不篩選漲跌, 1為篩上漲, 2為篩下跌 



    try:  # 確定輸入的持有天數為正整數
        holddays = int(hold_entry.get())
        if holddays<=0:
            result_label6.configure(text= '持有天數應為正整數')
            printblank()
            temp_do +=1 
    except:
        result_label6.configure(text= '持有天數應為正整數')
        printblank()
        temp_do +=1 
        

    if moving_avg_updown != 0 : # 確定輸入的均線濾網長度為正整數
        try:
            moving_avg = int(length_entry.get())
            if moving_avg<=0:
                result_label6.configure(text= '均線濾網長度應為正整數')
                printblank()
                temp_do +=1 
        except:
            result_label6.configure(text= '均線濾網長度應為正整數')
            printblank()
            temp_do +=1 



    start_year = int(comboExample1.get() )
    start_month = int(comboExample2.get() )
    start_day = int(comboExample3.get() )
    end_year = int(comboExample4.get() )
    end_month = int(comboExample5.get() )
    end_day = int(comboExample6.get() )
    startdatetime = datetime.datetime(start_year, start_month, start_day)  # 回測開始日期
    enddatetime = datetime.datetime(end_year, end_month, end_day)  # 回測結束日期
    
    
    # 確定結束日期後於起始日期
    if ( enddatetime- startdatetime).days < 0:
        result_label6.configure(text= '結束日期應大於開始日期')
        printblank()
        temp_do +=1 

    if temp_do == 0 :  # 確定輸入的開始結束日期及長度

    

        if ( enddatetime- startdatetime).days < holddays:
            result_label6.configure(text= '回測日期長度應大於持有天數')
            printblank()
            temp_do +=1 

        if ( enddatetime- startdatetime).days < holddays:
            result_label6.configure(text= '回測日期長度應大於持有天數')
            printblank()
            temp_do +=1 

    if temp_do == 0 :
        if ( enddatetime- startdatetime).days < moving_avg  :
            result_label6.configure(text= '回測日期長度應大於均線濾網長度')
            printblank()
            temp_do +=1 
            


    if temp_do == 0:  # 表示前方輸入資料都沒問題 開始計算回測
    
        for i in range(0,data.shape[0]):  # 讀取資料 填入欄位資料：日期 均線平均 均線上下 持有到到期價格等
            data.loc[i, 'datetime'] = datetime.datetime.strptime(data.loc[i][0],"%Y/%m/%d")
            if i >= moving_avg-1:
                sum_temp = 0
                for j in range(moving_avg):
                    sum_temp += data.loc[i-j,'Close']
                if moving_avg != 0:
                    data.loc[i, 'moving_avg'] = sum_temp/moving_avg

                if  data.loc[i,'Close'] > data.loc[i, 'moving_avg']:
                    data.loc[i, 'moving_avg_updown'] = 1
                elif data.loc[i,'Close'] < data.loc[i, 'moving_avg']:
                    data.loc[i, 'moving_avg_updown'] = -1

            if i > 0:
                if data.loc[i,'Close'] > data.loc[i-1,'Close']:
                    data.loc[i, 'up_down'] = 1
                elif data.loc[i,'Close'] < data.loc[i-1,'Close']:
                    data.loc[i, 'up_down'] = 2

            if i+holddays < data.shape[0]:
                data.loc[i, 'end_price'] = data.loc[i+holddays,'Close']
                data.loc[i, 'reture_percent'] = 100* ((data.loc[i, 'end_price'] - data.loc[i,'Close'])/data.loc[i,'Close'])


        temp0 = 0
        temp1 = 0
        temp2 = 0
        temp3 = data.shape[0]
        data0 = []
        data1 = []
        data2 = []
        data3 = []
        
        # 取得設定的開始及結束日期內的資料
        for i in range(0,data.shape[0]):
            if temp0 == 0:
                if (data.loc[i,'datetime']-startdatetime).days>=0:
                    temp0 = 1
                    temp2 = i
                    #data0 = data[i:]
            if temp0 == 1 and temp1 == 0:
                if (data.loc[i,'datetime']-enddatetime).days>0:
                    temp1 = 1
                    temp3 = i
        data0 = data[temp2:temp3]  
        

        # 取得要的濾網及漲跌資料
        if up_down != 0:
            data1 = data0[data0["up_down"]==up_down]
        else:
            data1 = data0

        if moving_avg_updown != 0:
            data2 = data1[data1["moving_avg_updown"]==moving_avg_updown]
        else:
            data2 = data1
        data3 = data2[data2["end_price"]!=0] 

        if len(data3)>=1:
        
            reture_count  = list(data3['reture_percent'].to_numpy())


            import math
            # 以下數行為輸出敘述統計量資料
            result_label1.configure(text=('mean:',round(data3['reture_percent'].mean(),3)))
            result_label2.configure(text=('min:',round(data3['reture_percent'].min(),3)))
            result_label3.configure(text=('max:',round(data3['reture_percent'].max(),3)))
            result_label4.configure(text=('std:',round(data3['reture_percent'].std(),3)))
            result_label5.configure(text=('var:',round(data3['reture_percent'].var(),3)))
            result_label6.configure(text=('skew:',round(data3['reture_percent'].skew(),3)))
            result_label7.configure(text=('kurtosis:',round(data3['reture_percent'].kurtosis(),3)))
            result_label8.configure(text=('medium:',round(data3['reture_percent'].median(),3)))


            endpoints = []

            # 以下數行轉換長條圖到折線位置上
            for i in range(int(10*data3['reture_percent'].min())-1, int(10*data3['reture_percent'].max())+1, 1):
                endpoints.append(i/10)

            n, bins, patches = plt.hist(reture_count, bins = endpoints, density=1, facecolor = "gray", edgecolor = "black")
            plt.cla()
            n = n/10

            bins2 = []
            for i in range(len(bins)-1):
                bins2.append((bins[i]+bins[i+1])/2)


            # 以下數行為輸出結果的折線圖
            plt.plot(bins2, n) 
            plt.xlabel("Reture (percent)")
            plt.ylabel("Probability")
            plt.title("Probability Function")
            plt.xlim(data3['reture_percent'].min(), data3['reture_percent'].max()) # 要顯示的範圍(報酬百分比)
            plt.ylim(0)
            plt.show()
        
        else:
            printblank()
            result_label6.configure(text= '符合回測條件的開盤天數為0')










# 以下為視窗介面使用者輸入資料用

window = tk.Tk()
window.title('台灣加權指數期貨回測')
window.geometry('565x256')
window.configure(background='white')


header_label = tk.Label(window, text='台灣加權指數期貨回測' )
header_label.grid(column=0, row=0 ,columnspan = 4,sticky=tk.NW + tk.SE)


comboExample0_label = tk.Label(window, text='開始日期')
comboExample0_label.grid(column=0, row=1,sticky=tk.NW + tk.SE)


comboExample1_label = tk.Label(window, text='結束日期')
comboExample1_label.grid(column=0, row=2,sticky=tk.NW + tk.SE)



comboExample1 = ttk.Combobox(window, 
                            values=[2000, 2001,2002,2003,2004,2005,2006,2007,2008,2009,2010,
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


comboExample4 = ttk.Combobox(window, 
                            values=[2000, 2001,2002,2003,2004,2005,2006,2007,2008,2009,2010,
                                    2011,2012,2013,2014,2015,2016,2017,2018,2019,2020] ,state="readonly")
comboExample4.grid(column=1, row=2)
comboExample4.current(0)


comboExample5 = ttk.Combobox(window, 
                            values=[1,2,3,4,5,6,7,8,9,10,11,12] ,state="readonly")
comboExample5.grid(column=2, row=2)
comboExample5.current(0)


comboExample6 = ttk.Combobox(window, 
                             values=[1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21
                                    ,22,23,24,25,26,27,28,29,30,31] ,state="readonly")
comboExample6.grid(column=3, row=2)
comboExample6.current(0)



Value = tk.IntVar() 

updown_label = tk.Label(window, text='當日漲跌濾網')
updown_label.grid(column=0, row=3,sticky=tk.NW + tk.SE)
 
rdioOne = tk.Radiobutton(window, text='不需漲跌濾網', variable=Value, value=0) 
rdioTwo = tk.Radiobutton(window, text='當日漲', variable=Value, value=1) 
rdioThree = tk.Radiobutton(window, text='當日跌', variable=Value, value=2)

rdioOne.grid(column=1, row=3,sticky=tk.NW + tk.SE)
rdioTwo.grid(column=2, row=3,sticky=tk.NW + tk.SE)
rdioThree.grid(column=3, row=3,sticky=tk.NW+ tk.SE)



Value1 = tk.IntVar() 

avg_label = tk.Label(window, text='均線濾網')
avg_label.grid(column=0, row=4,sticky=tk.NW + tk.SE)
 
rdioOne1 = tk.Radiobutton(window, text='不需均線濾網', variable=Value1, value=0) 
rdioTwo1 = tk.Radiobutton(window, text='收均線以上', variable=Value1, value=1) 
rdioThree1 = tk.Radiobutton(window, text='收均線以下', variable=Value1, value=-1)

rdioOne1.grid(column=1, row=4,sticky=tk.NW + tk.SE)
rdioTwo1.grid(column=2, row=4,sticky=tk.NW + tk.SE)
rdioThree1.grid(column=3, row=4,sticky=tk.NW+ tk.SE)



length_label = tk.Label(window, text='均線濾網長度')
length_label.grid(column=0, row=5,sticky=tk.NW+ tk.SE)

length_entry = tk.Entry(window)
length_entry.grid(column=1, row=5,sticky=tk.NW+ tk.SE,columnspan =2)

length_label = tk.Label(window, text='')
length_label.grid(column=2, row=5,sticky=tk.NW+ tk.SE,columnspan =2)



hold_1_label = tk.Label(window, text='持有天數')
hold_1_label.grid(column=0, row=6,sticky=tk.NW+ tk.SE)

hold_entry = tk.Entry(window)
hold_entry.grid(column=1, row=6,sticky=tk.NW+ tk.SE,columnspan =1)

hold_label = tk.Label(window, text='')
hold_label.grid(column=2, row=6,sticky=tk.NW+ tk.SE)


calculate_btn = tk.Button(window, text='開始計算', command=calculate)
calculate_btn.grid(column=3, row=6,sticky=tk.NW+ tk.SE,columnspan =4)


# 以下為最下方敘述統計量輸出位置
result_label1 = tk.Label(window)
result_label1.grid(column=0, row=7,sticky=tk.NW+ tk.SE,columnspan =2)

result_label2 = tk.Label(window)
result_label2.grid(column=0, row=8,sticky=tk.NW+ tk.SE,columnspan =2)

result_label3 = tk.Label(window)
result_label3.grid(column=0, row=9,sticky=tk.NW+ tk.SE,columnspan =2)

result_label4 = tk.Label(window)
result_label4.grid(column=2, row=7,sticky=tk.NW+ tk.SE,columnspan =2)

result_label5 = tk.Label(window)
result_label5.grid(column=2, row=8,sticky=tk.NW+ tk.SE,columnspan =2)

result_label6 = tk.Label(window)
result_label6.grid(column=2, row=9,sticky=tk.NW+ tk.SE,columnspan =2)

result_label7 = tk.Label(window)
result_label7.grid(column=2, row=10,sticky=tk.NW+ tk.SE,columnspan =2)

result_label8 = tk.Label(window)
result_label8.grid(column=0, row=10,sticky=tk.NW+ tk.SE,columnspan =2)

window.mainloop()
