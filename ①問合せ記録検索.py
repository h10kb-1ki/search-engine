import pandas as pd
import sqlite3
from datetime import datetime
import streamlit as st

st.title('問合せ記録 横断検索')
kensaku = st.text_input('検索ワード（1単語のみ）を入力してください。  ※半角・全角は区別されます')
btn = st.button('検索')

st.write('===== データベース使用上の注意 =====')
st.write('問合せ記録は、過去の対応事例の内容を示すデータベースです。'
        +'対応時点で根拠とした医薬品情報が現在も同じエビデンスレベルで活用できるとは限らないことにご留意ください。  \n'
        +'※このページからは情報の修正はできません。修正が必要な場合は管理担当者へ連絡してください。' 
        )

if btn:
    kensaku = '%' + kensaku + '%'
    db = sqlite3.connect('toiawase.db')
    cur = db.cursor()    
    
    cur.execute("SELECT * FROM T_old WHERE category LIKE ? OR drug LIKE ? OR question LIKE ? OR answer LIKE ?", 
                [kensaku, kensaku, kensaku, kensaku])
    data = cur.fetchall()
    
    cur.execute("SELECT * FROM T_new WHERE category LIKE ? OR drug LIKE ? OR question LIKE ? OR answer LIKE ? OR reference LIKE ?", 
                [kensaku, kensaku, kensaku, kensaku, kensaku])
    data_n = cur.fetchall()
    cur.close()
    db.close()
    
    if len(data_n) == 0:
        st.write('-------------------------------------------------------------------')
        st.write('■2022年1月以降の問合せ記録：該当データなし')
        st.write('-------------------------------------------------------------------')
    else:
        st.write(f'■2022年1月以降の問合せ記録：{len(data_n)}')
        st.write('-------------------------------------------------------------------')
        for i in range(0, len(data_n)):
            tdatetime = datetime.strptime(data_n[i][0], '%Y-%m-%d %H:%M:%S') 
            tdate = tdatetime.date().strftime('%Y/%m/%d')
            st.write('【日付】' + tdate)
            st.write('【種別】' + data_n[i][1])
            st.write('【医薬品名】' + data_n[i][2])
            st.write(f'【質問】  \n{data_n[i][3]}')
            st.write(f'【回答】  \n{data_n[i][4]}')
            st.write(f'【参考文献】\n{data_n[i][5]}')
            st.write('-------------------------------------------------------------------')
    st.write('')
    
    if len(data) == 0:
        st.write('■2021年12月以前の問合せ記録：該当データなし')
        st.write('-------------------------------------------------------------------')
    else:    
        st.write(f'■2021年12月以前の問合せ記録：{len(data)}')
        st.write('-------------------------------------------------------------------')
        for i in range(0, len(data)):
            tdatetime = datetime.strptime(data[i][0], '%Y-%m-%d %H:%M:%S')
            tdate = tdatetime.date().strftime('%Y/%m/%d')
            st.write('【日付】' + tdate)
            st.write('【種別】' + data[i][1])
            st.write('【医薬品名】' + data[i][2])
            st.write(f'【質問】  \n{data[i][3]}')
            st.write(f'【回答】  \n{data[i][4]}')
            st.write('-------------------------------------------------------------------')