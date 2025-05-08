from flask import Flask, Response
import openai
import datetime
import yfinance as yf

app = Flask(__name__)

# OpenAI GPT API 金鑰
openai.api_key = "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"

STOCKS = {
    "AI": {
        "TW": [("世芯-KY", "3661.TW"), ("創意", "3443.TW"), ("智原", "3035.TW")],
        "US": [("NVIDIA", "NVDA"), ("AMD", "AMD"), ("Palantir", "PLTR")]
    },
    "QC": {
        "TW": [("聯發科", "2454.TW"), ("光寶科", "2301.TW"), ("穩懋", "3105.TW")],
        "US": [("IonQ", "IONQ"), ("Rigetti", "RGTI"), ("D-Wave", "QBTS")]
    }
}

def fetch_price(stock_list):
    result = []
    for name, code in stock_list:
        try:
            data = yf.Ticker(code)
            price = data.history(period="1d")['Close'].iloc[-1]
            vol = data.history(period="1d")['Volume'].iloc[-1]
            result.append(f"{name}({code}): 股價 {round(price, 2)}，成交量 {int(vol/1e6)}M")
        except:
            result.append(f"{name}({code}): 無法取得資料")
    return result

def get_gpt_news():
    prompt = "請用中文摘要今天 AI 技術與量子電腦領域的全球重大新聞，各寫 1 條，不要贅詞，50 字內即可。"
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}]
        )
        return response.choices[0].message.content.strip()
    except:
        return "無法取得 GPT 新聞摘要。"

@app.route("/daily_report", methods=["GET"])
def daily_report():
    today = datetime.datetime.now().strftime("%Y/%m/%d")
    content = f"[{today} 股市追蹤]\n\n"
    for domain in ["AI", "QC"]:
        content += f"【{domain} 領域】\n"
        for region in ["TW", "US"]:
            area = "國內" if region == "TW" else "國外"
            content += f"{area}：\n"
            content += "\n".join(fetch_price(STOCKS[domain][region])) + "\n\n"
    content += "【每日新聞摘要】\n"
    content += get_gpt_news() + "\n"
    content += "\n來源：Yahoo Finance, OpenAI GPT-4"
    return Response(content, mimetype='text/plain')

if __name__ == "__main__":
    app.run()
