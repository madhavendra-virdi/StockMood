import requests
import pandas as pd

pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)
pd.set_option('display.colheader_justify', 'center')

url = "https://contentapi.accordwebservices.com/RawData/GetRawDataJSON"
params = {
    "filename": "Insider_trading",
    "date": "30092022",  # Replace with your desired date
    "section": "Corporateaction",
    "sub": "",
    "token": "fMqHkvwLKoN6rTyt_j7F3HNgnvhBtWWE"  # Replace with your real token
}



#  filename : Indicesmaster, Company_master , Comp_Indexpart , 2022093001
#  section : Master(1), BSEStocksLive(2), BSEIndicesLive
response = requests.get(url, params=params)

if response.ok:
    data = response.json()
    df = pd.DataFrame(data['Table'])
    print(df)
else:
    print("Failed to fetch data:", response.status_code)
