from flask import Flask
import yfinance as yf
import openai
from datetime import datetime

app = Flask(__name__)
openai.api_key = "sk-請填入你的金鑰"

def get_stock_price(symbol):
    try:
        stock = yf.Ticker(symbol)
        todays_data = stock.history(period="1d")
        price = todays_data['Close'][0]
        volume = todays_data['Volume'][0]
        return f"股價 {round(price, 2)}，成交量 {round(volume/1_000_000)}M"
    except:
        return "無法取得資料"

def get_gpt_news():
    prompt = "請用中文摘要今天 AI 技術與量子電腦領域的全球重大新聞..."
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}]
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return "【GPT 錯誤】" + str(e)

@app.route("/daily_report", methods=["GET"])
def daily_report():
    date = datetime.today().strftime("%Y/%m/%d")
    output = [f"[{date} 股市追蹤]\n"]

    output.append("【AI 領域】\n國內：")
    for stock in ["3661.TW", "3443.TW", "3035.TW"]:
        output.append(f"世芯-KY({stock})：{get_stock_price(stock)}" if stock == "3661.TW" else
                      f"創意({stock})：{get_stock_price(stock)}" if stock == "3443.TW" else
                      f"智原({stock})：{get_stock_price(stock)}")

    output.append("\n國外：")
    for name, symbol in [("NVIDIA", "NVDA"), ("AMD", "AMD"), ("Palantir", "PLTR")]:
        output.append(f"{name}({symbol})：{get_stock_price(symbol)}")

    output.append("\n【QC 領域】\n國內：")
    for name, symbol in [("聯發科", "2454.TW"), ("光寶科", "2301.TW"), ("穩懋", "3105.TW")]:
        output.append(f"{name}({symbol})：{get_stock_price(symbol)}")

    output.append("\n國外：")
    for name, symbol in [("IonQ", "IONQ"), ("Rigetti", "RGTI"), ("D-Wave", "QBTS")]:
        output.append(f"{name}({symbol})：{get_stock_price(symbol)}")

    output.append("\n【每日新聞摘要】")
    output.append(get_gpt_news())
    output.append("\n來源：Yahoo Finance, OpenAI GPT-4")

    return "\n".join(output)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
