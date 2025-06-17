import requests
from bs4 import BeautifulSoup
import pandas as pd


def extractor(input):
    rows = soup.find_all('tr')
    numbers = []

    # Iterate through rows and check for the presence of "Operating Profit"
    for row in rows:
        # Check if the row contains the text "Operating Profit"
        if row.find('td', class_='text') and input in row.find('td', class_='text').get_text():
            # Extract all numbers (values inside <td> tags except the first one)
            profits = [td.get_text().strip() for td in row.find_all('td')[1:]]
            numbers.extend(profits)
    return numbers[22:-1]



def extractor2(input):
    rows = soup.find_all('tr')
    numbers = []

    # Iterate through rows and check for the presence of the input text
    for row in rows:
        if row.find('td', class_='text') and input.strip().lower() in row.find('td', class_='text').get_text().strip().lower():
            # Extract all numbers (values inside <td> tags except the first one)
            profits = [td.get_text().strip() for td in row.find_all('td')[1:]]
            numbers.extend(profits)
    return numbers[9:-1]


def extractor3(input):
    rows = soup.find_all('tr')
    numbers = []

    # Iterate through rows and check for the presence of the input text
    for row in rows:
        if row.find('td', class_='text') and input.strip().lower() in row.find('td', class_='text').get_text().strip().lower():
            # Extract all numbers (values inside <td> tags except the first one)
            profits = [td.get_text().strip() for td in row.find_all('td')[1:]]
            numbers.extend(profits)
    return numbers[9:]


def extractor4(input):
    items = soup.find_all('li', class_='flex flex-space-between')  # Find all relevant list items
    numbers = []

    # Iterate through the list items
    for item in items:
        name = item.find('span', class_='name')
        if name and input.strip().lower() in name.get_text().strip().lower():
            # Extract the value inside the 'number' span
            value = item.find('span', class_='number')
            if value:
                numbers.append(value.get_text().strip())
    return numbers


def extractor5(input_text):
    rows = soup.find_all('tr')
    numbers = []

    # Iterate through rows and check for the presence of the input text
    for row in rows:
        # Locate the 'td' with class 'text' and extract its text
        text_td = row.find('td', class_='text')
        if text_td and input_text.strip().lower() in text_td.get_text(strip=True).lower():
            # Extract all numbers from the <td> tags except the first one
            profits = [td.get_text(strip=True) for td in row.find_all('td')[1:]]
            numbers.extend(profits)

    return numbers[20:]


# Ensure all rows and columns of the DataFrame are displayed
pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)
pd.set_option('display.colheader_justify', 'center')

columns = [
    'Name', 'Ticker', 'Sub-Industry', 'Industry',
     'sales_2022', 'sales_2023', 'sales_2024',
    'expenses_2022', 'expenses_2023', 'expenses_2024',
    'other_income_2022','other_income_2023','other_income_2024',
    'interest_2022','interest_2023','interest_2024',
    'depreciation_2022','depreciation_2023','depreciation_2024',
    'tax%_2022', 'tax%_2023', 'tax%_2024',
    'div_payout%_2022', 'div_payout%_2023', 'div_payout%_2024',
    'equity_capital_2022', 'equity_capital_2023', 'equity_capital_2024',
    'reserves_2022', 'reserves_2023', 'reserves_2024',
    'borrowings_2022', 'borrowings_2023', 'borrowings_2024',
    'other_liabilities_2022', 'other_liabilities_2023', 'other_liabilities_2024',
    'fixed_assets_2022', 'fixed_assets_2023', 'fixed_assets_2024',
    'cwip_2022', 'cwip_2023', 'cwip_2024',
    'investments_2022', 'investments_2023', 'investments_2024',
    'other_assets_2022', 'other_assets_2023', 'other_assets_2024',
    'cfo_2022', 'cfo_2023', 'cfo_2024',
    'cfi_2022', 'cfi_2023', 'cfi_2024',
    'cff_2022', 'cff_2023', 'cff_2024',
    'MCap','Price','P/E', 'PromoterHold','About'

]

df = pd.DataFrame(columns=columns)

bse = pd.read_csv('bse_short.csv')
tickers1 = bse.iloc[:, 1]
tickers1 = tickers1.str.split(':').str[1]
#print(tickers1)

for index, row in bse.iterrows():
    print(row["Ticker"].split(':')[1])




tickers = ['AFFLE','PANACEABIO']

for index, row in bse.iterrows():
#for ticker in tickers:
    try:

        ticker = row["Ticker"].split(':')[1]
        url = f'https://www.screener.in/company/{ticker}/consolidated/#cash-flow'

        response = requests.get(url)

                # Parse the HTML content of the page
        soup = BeautifulSoup(response.content, "html.parser")
        #print(soup)


        # Find the row containing the 'Sales' keyword with 'profit-loss'
        row1 = soup.find('button', onclick=lambda x: x and 'Sales' in x and 'profit-loss' in x).find_parent('tr')
        row2 = soup.find('button', onclick=lambda x: x and 'Expenses' in x and 'profit-loss' in x).find_parent('tr')


        # Extract all <td> elements except the first one (the "Sales" button column)
        sales_numbers = row1.find_all('td')[10:-1]
        expenses_numbers = row2.find_all('td')[10:-1]


        # Extract the text content and convert to integers
        #sales_numbers = [float(td.text) for td in td_elements1]
        #expenses_numbers = [float(td.text) for td in td_elements2]
        other_income_numbers = extractor("Other Income")
        interest = extractor("Interest")
        depreciation = extractor("Depreciation")
        tax = extractor("Tax %")
        div_payout = extractor2("Dividend Payout %")  ## unabel to extract div payout

        # BALANCE SHEET
        equity_capital = extractor2("Equity Capital")
        reserves = extractor2("Reserves")
        borrowings = extractor2("Borrowings")
        other_lia = extractor2("Other Liabilities")
        fixed_ass = extractor2("Fixed Assets")
        cwip = extractor2("CWIP")
        investments = extractor2("Investments")
        other_ass = extractor2("Other Assets")


        # CASH FLOW
        cfo = extractor3("Cash from Operating Activity")
        cfi = extractor3("Cash from Investing Activity")
        cff = extractor3("Cash from Financing Activity")

        # MISC
        mcap = extractor4("Market Cap")
        price = extractor4("Current Price")
        pe = extractor4("Stock P/E")
        promoter = extractor5("Promoters")

        about_div = soup.find('div', class_='sub commentary always-show-more-box')
        about_text = about_div.get_text(separator=" ", strip=True)

        numbers = (sales_numbers + expenses_numbers  + other_income_numbers + interest + depreciation + tax + div_payout +
                   equity_capital + reserves + borrowings + other_lia + fixed_ass + cwip + investments + other_ass +
                   cfo + cfi + cff + mcap + price + pe + promoter + [about_text])

    #[row["Stock"]] + [row["Ticker"]] + [row["Sub"]] + [row["Industry"]]+
        data = [row["Stock"]] + [row["Ticker"]] + [row["Sub"]] + [row["Industry"]]+ numbers
        #print(data)
        df = pd.concat([df, pd.DataFrame([data], columns=columns)], ignore_index=True)
        print(data)
        #print(df)

    except Exception as e:
        print(f"An error occurred for row {row["Ticker"]}: {e}")

print(df)
df.to_csv("output13.csv", index=False)
