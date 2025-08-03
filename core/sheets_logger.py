import gspread
from oauth2client.service_account import ServiceAccountCredentials

def setup_gsheet(sheet_name="TradeLogs"):
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name("credentials.json", scope)
    client = gspread.authorize(creds)

    sheet = client.open(sheet_name)
    logs = sheet.worksheet("Trades")
    pnl = sheet.worksheet("P&L")
    summary = sheet.worksheet("Summary")
    return logs, pnl, summary

def log_trades(df, logs_sheet):
    logs_sheet.clear()
    logs_sheet.append_row(["Date", "Close", "RSI", "MACD", "Buy Signal", "Prediction"])

    for idx, row in df.iterrows():
        buy = "Yes" if row["RSI"] < 30 and row["DMA_Cross"] == 1 else ""
        logs_sheet.append_row([
            idx.strftime("%Y-%m-%d"),
            round(row["close"], 2),
            round(row["RSI"], 2),
            round(row["MACD"], 2),
            buy,
            int(row.get("Prediction", 0))
        ])
