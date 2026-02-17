@app.get("/predict")
def predict(symbol: str):
    url = f"https://query1.finance.yahoo.com/v8/finance/chart/{symbol}?range=5d&interval=1d"

    headers = {
        "User-Agent": "Mozilla/5.0",
        "Accept": "application/json"
    }

    r = requests.get(url, headers=headers, timeout=10)

    if r.status_code != 200:
        return {"error": "Failed to fetch data from Yahoo"}

    try:
        data = r.json()
        prices = data["chart"]["result"][0]["indicators"]["quote"][0]["close"]

        last_price = prices[-1]
        prev_price = prices[-2]

        prediction = "UP" if last_price > prev_price else "DOWN"

        return {
            "symbol": symbol,
            "last_price": last_price,
            "prediction": prediction
        }

    except Exception as e:
        return {"error": "Invalid symbol or Yahoo blocked data"}
