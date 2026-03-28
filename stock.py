import yfinance as yf
import pandas as pd
from company import get_stock

chosenstock = []
stocks = []
chosenstock, stocks = get_stock()

def YangSwallow(data):
    data["Price_Difference"] = data["Open"] - data["Close"].shift(1)
    data["Price_Difference2"] = data["Close"] - data["Open"].shift(1)
    filtered_data = data[(data["Price_Difference"] < 0) &
                          (data["Price_Difference2"] > 0) &
                          ((data["Close"].shift(1)-data["Open"].shift(1)) < 0) &
                          ((data["Close"]-data["Open"]) > 0)]
    
    if filtered_data.empty:
        return []
    else:
        return filtered_data.index.strftime('%Y-%m-%d').tolist()

def InSwallow(data):
    data["Price_Difference"] = data["Close"] - data["Open"].shift(1)
    data["Price_Difference2"] = data["Open"] - data["Close"].shift(1)
    filtered_data = data[(data["Price_Difference"] < 0) &
                          (data["Price_Difference2"] > 0) &
                          ((data["Close"].shift(1)-data["Open"].shift(1)) > 0) &
                          ((data["Close"]-data["Open"]) < 0)]

    if filtered_data.empty:
        return []
    else:
        return filtered_data.index.strftime('%Y-%m-%d').tolist()

def threesolderBlack(data):
    data["Price_Lower"] = data["Close"] - data["Close"].shift(1)
    data["Price_Lower2"] = data["Close"].shift(1) - data["Close"].shift(2)
    data["Price_Lower3"] = data["Close"].shift(2) - data["Close"].shift(3)
    data["Price_Lowera"] = data["Open"] - data["Open"].shift(1)
    data["Price_Lowera2"] = data["Open"].shift(1) - data["Open"].shift(2)
    data["Price_Lowera3"] = data["Open"].shift(2) - data["Open"].shift(3)
    
    filtered_data = data[(data["Price_Lower"] < 0) &
                         (data["Price_Lower2"] < 0) &
                         (data["Price_Lower3"] < 0) &
                         (data["Price_Lowera"] < 0) &
                         (data["Price_Lowera2"] < 0) &
                         (data["Price_Lowera3"] < 0) &
                         ((data["Close"] - data["Open"]) < 0) &
                         ((data["Close"].shift(1) - data["Open"].shift(1)) < 0) &
                         ((data["Close"].shift(2) - data["Open"].shift(2)) < 0)]

    if filtered_data.empty:
        return []
    else:
        return filtered_data.index.strftime('%Y-%m-%d').tolist()

def threesolderRed(data) :
    data["Price_Higher"] = data["Close"] - data["Close"].shift(1)
    data["Price_Higher2"] = data["Close"].shift(1) - data["Close"].shift(2)
    data["Price_Highera"] = data["Open"] - data["Open"].shift(1)
    data["Price_Highera2"] = data["Open"].shift(1) - data["Open"].shift(2)
    
    filtered_data = data[(data["Price_Higher"] > 0) &
                          (data["Price_Higher2"] > 0) &
                          (data["Price_Highera"] > 0) &
                          (data["Price_Highera2"] > 0) &
                          ((data["Close"].shift(2)-data["Open"].shift(2)) > 0) &
                          ((data["Close"].shift(1)-data["Open"].shift(1)) > 0) &
                          ((data["Close"]-data["Open"]) > 0)]

    if filtered_data.empty:
        return []
    else:
        return filtered_data.index.strftime('%Y-%m-%d').tolist()


def create_ticker(symbol):
    ticker = yf.Ticker(symbol)
    return ticker


print("你好呀!這裡是股票檢測小幫手，我們會預先幫你檢測台股喔!\n這邊還可以加多支自選股喔!\n")
print("你想加幾支呢?")
indexn = int(input())
if indexn != 0:
    for i in range(0, indexn):
        symbol = input("請輸入您想額外檢測的股票代碼: ")
        stocks.append(symbol)
        tmp = create_ticker(symbol)
        chosenstock.append(tmp)

for i in range(0, len(chosenstock)) :
    chosenstock[i] = chosenstock[i].history(period="2mo")

summary_results = {
    "陽吞": {},
    "陰吞": {},
    "黑三兵": {},
    "紅三兵": {}
}

print("\n--- 開始檢測 ---")
for i in range(0, len(chosenstock)) :
    stock = chosenstock[i]
    symbol = stocks[i]
    
    if stock.empty:
        print(f"{symbol}：沒有這支股票捏;w;，再找找別的八")
        continue

    dates_yang = YangSwallow(stock)
    dates_in = InSwallow(stock)
    dates_black = threesolderBlack(stock)
    dates_red = threesolderRed(stock)
    
    if dates_yang: summary_results["陽吞"][symbol] = dates_yang
    if dates_in:   summary_results["陰吞"][symbol] = dates_in
    if dates_black: summary_results["黑三兵"][symbol] = dates_black
    if dates_red:  summary_results["紅三兵"][symbol] = dates_red

print("\n" + "="*40)
print("📊 最終檢測結果總結")
print("="*40)

for pattern_name, result_dict in summary_results.items():
    print(f"\n【{pattern_name}】")
    if not result_dict:
        print("  無股票出現此型態。")
    else:
        for sym, dates in result_dict.items():
            dates_str = ", ".join(dates)
            print(f"  📌 {sym}: {dates_str}")

print("\n檢測完成！祝你投資順利！")