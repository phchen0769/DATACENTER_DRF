# -*- coding: utf-8 -*-
import yfinance as yf
import time

# 指定股票代码（建设银行H股）
ccb = yf.Ticker("0939.HK")

# 自动重试获取分红数据
for i in range(5):
    try:
        dividends = ccb.dividends
        print(dividends.tail(3))  # 查看最近3次分红记录
        break
    except Exception as e:
        print(f"第{i+1}次尝试失败：{e}")
        time.sleep(30)  # 等待30秒后重试
else:
    print("多次尝试后仍然失败，请稍后再试。")
