import yfinance as yt

tickers = ["AAPL", "MSFT", "NVDA"]

for ticker in tickers:
    stock = yt.Ticker(ticker)
    report = stock.get_earnings_dates(limit=12)
    if report is None or report.empty:
        continue

    print(f"--- {ticker} ---")
    print(report)
