from alpha_vantage.timeseries import TimeSeries
import pandas as pd

api_key = "PZZTS0M15ZWI311J"
ts = TimeSeries(key=api_key, output_format='pandas')

nifty50_companies = {
    "RELIANCE.BSE": "Reliance Industries",
    "INFY.BSE": "Infosys",
    "HDFCBANK.BSE": "HDFC Bank"
}

all_data = pd.DataFrame()

for symbol, company_name in nifty50_companies.items():
    print(f"Fetching Data for {company_name} ({symbol})...")

    try:
        data, meta_data = ts.get_daily(symbol=symbol, outputsize="full")

        data["Company"] = company_name
        data["Symbol"] = symbol

        data.reset_index(inplace=True)

        all_data = pd.concat([all_data, data], ignore_index=True)

    except Exception as e:
        print(f"Error fetching data for {company_name} ({symbol}): {e}")

all_data.to_csv("nifty50_stock_data.csv", index=False)
print("Data saved to nifty50_stock_data.csv")