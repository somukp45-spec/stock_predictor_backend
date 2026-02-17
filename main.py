from fastapi import FastAPI
import requests
import csv
from io import StringIO

app = FastAPI()

@app.get("/")
def home():
    return {"status": "Backend running"}

@app.get("/predict")
def predict(symbol: str):
    try:
        # Stooq uses lowercase symbols
        sym = symbol.lower()

        url = f"https://stooq.com/q/d/l/?s={sym}&i=d"
        r = requests.get(url, timeout=10)

        if r.status_code != 200 or len(r.text) < 50:
            return {"error": "Data not available"}

        f = StringIO(r.text)
        reader = list(csv.reader(f))

        # Last 2 closing prices
        last_close = float(reader[-1][4])
        prev_close = float(reader[-2][4])

        prediction = "UP" if last_close > prev_close else "DOWN"

        return {
            "symbol": symbol.upper(),
            "last_price": last_close,
            "prediction": prediction
        }

    except Exception as e:
        return {"error": "Invalid symbol"}
