import pandas as pd

# Ensure all rows and columns of the DataFrame are displayed
pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)
pd.set_option('display.colheader_justify', 'center')


bse2000 = pd.read_csv('bse2000.csv', encoding='ISO-8859-1')
print(len(bse2000))
bse2000 = bse2000.drop_duplicates()
print(len(bse2000))


# market cap : blue chip 20k cr plus, mid cap 5k-20k, small cap (5k-500), nano/micro : 500-50
# market cap
bse2000['MCap'] = bse2000['MCap'].str.replace(',', '').astype(float)
bins = [-float('inf'), 500, 5000, 20000, float('inf')]
labels = ['Nano', 'Micro', 'Small', 'Mid', 'Large']
bse2000['MCap_category'] = pd.cut(bse2000['MCap'], bins=[-float('inf'),50, 500, 5000, 20000, float('inf')],
                                  labels=['Nano', 'Micro', 'Small', 'Mid', 'Large'], right=True)


bse2000['Price'] = bse2000['Price'].str.replace(',', '').astype(float)
bse2000['P/E'] = bse2000['P/E'].str.replace(',', '').astype(float)
bse2000['PromoterHold'] = bse2000['PromoterHold'].str.replace('%', '').astype(float)
bse2000['sales_2024'] = pd.to_numeric(bse2000['sales_2024'].str.replace(r'<[^>]+>', '', regex=True).str.replace(',', ''), errors='coerce')
bse2000['sales_2023'] = pd.to_numeric(bse2000['sales_2023'].str.replace(r'<[^>]+>', '', regex=True).str.replace(',', ''), errors='coerce')
bse2000['sales_2022'] = pd.to_numeric(bse2000['sales_2022'].str.replace(r'<[^>]+>', '', regex=True).str.replace(',', ''), errors='coerce')
bse2000['expenses_2024'] = pd.to_numeric(bse2000['expenses_2024'].str.replace(r'<[^>]+>', '', regex=True).str.replace(',', ''), errors='coerce')
bse2000['expenses_2023'] = pd.to_numeric(bse2000['expenses_2023'].str.replace(r'<[^>]+>', '', regex=True).str.replace(',', ''), errors='coerce')
bse2000['expenses_2022'] = pd.to_numeric(bse2000['expenses_2022'].str.replace(r'<[^>]+>', '', regex=True).str.replace(',', ''), errors='coerce')
bse2000['other_income_2024'] = bse2000['other_income_2024'].str.replace(',', '').astype(float)
bse2000['other_income_2023'] = bse2000['other_income_2023'].str.replace(',', '').astype(float)
bse2000['other_income_2022'] = bse2000['other_income_2022'].str.replace(',', '').astype(float)
bse2000['interest_2024'] = pd.to_numeric(bse2000['interest_2024'].str.replace(r'<[^>]+>', '', regex=True).str.replace(',', ''), errors='coerce')
bse2000['interest_2023'] = pd.to_numeric(bse2000['interest_2023'].str.replace(r'<[^>]+>', '', regex=True).str.replace(',', ''), errors='coerce')
bse2000['interest_2022'] = pd.to_numeric(bse2000['interest_2022'].str.replace(r'<[^>]+>', '', regex=True).str.replace(',', ''), errors='coerce')
bse2000['equity_capital_2024'] = bse2000['equity_capital_2024'].str.replace(',', '').astype(float)
bse2000['equity_capital_2023'] = bse2000['equity_capital_2023'].str.replace(',', '').astype(float)
bse2000['equity_capital_2022'] = bse2000['equity_capital_2022'].str.replace(',', '').astype(float)
bse2000['reserves_2024'] = bse2000['reserves_2024'].str.replace(',', '').astype(float)
bse2000['reserves_2023'] = bse2000['reserves_2023'].str.replace(',', '').astype(float)
bse2000['reserves_2022'] = bse2000['reserves_2022'].str.replace(',', '').astype(float)
bse2000['borrowings_2024'] = bse2000['borrowings_2024'].str.replace(',', '').astype(float)
bse2000['borrowings_2023'] = bse2000['borrowings_2023'].str.replace(',', '').astype(float)
bse2000['borrowings_2022'] = bse2000['borrowings_2022'].str.replace(',', '').astype(float)
bse2000['other_liabilities_2022'] = bse2000['other_liabilities_2022'].str.replace(',', '').astype(float)
bse2000['other_liabilities_2023'] = bse2000['other_liabilities_2023'].str.replace(',', '').astype(float)
bse2000['other_liabilities_2024'] = bse2000['other_liabilities_2024'].str.replace(',', '').astype(float)
bse2000['fixed_assets_2022'] = bse2000['fixed_assets_2022'].str.replace(',', '').astype(float)
bse2000['fixed_assets_2023'] = bse2000['fixed_assets_2023'].str.replace(',', '').astype(float)
bse2000['fixed_assets_2024'] = bse2000['fixed_assets_2024'].str.replace(',', '').astype(float)
bse2000['cwip_2024'] = bse2000['cwip_2024'].str.replace(',', '').astype(float)
bse2000['cwip_2023'] = bse2000['cwip_2023'].str.replace(',', '').astype(float)
bse2000['cwip_2022'] = bse2000['cwip_2022'].str.replace(',', '').astype(float)
bse2000['investments_2022'] = bse2000['investments_2022'].str.replace(',', '').astype(float)
bse2000['investments_2023'] = bse2000['investments_2023'].str.replace(',', '').astype(float)
bse2000['investments_2024'] = bse2000['investments_2024'].str.replace(',', '').astype(float)
bse2000['other_assets_2022'] = bse2000['other_assets_2022'].str.replace(',', '').astype(float)
bse2000['other_assets_2023'] = bse2000['other_assets_2023'].str.replace(',', '').astype(float)
bse2000['other_assets_2024'] = bse2000['other_assets_2024'].str.replace(',', '').astype(float)
bse2000['cfo_2024'] = bse2000['cfo_2024'].str.replace(',', '').astype(float)
bse2000['cfo_2023'] = bse2000['cfo_2023'].str.replace(',', '').astype(float)
bse2000['cfo_2022'] = bse2000['cfo_2022'].str.replace(',', '').astype(float)
bse2000['cfi_2024'] = bse2000['cfi_2024'].str.replace(',', '').astype(float)
bse2000['cfi_2023'] = bse2000['cfi_2023'].str.replace(',', '').astype(float)
bse2000['cfi_2022'] = bse2000['cfi_2022'].str.replace(',', '').astype(float)
bse2000['cff_2024'] = bse2000['cff_2024'].str.replace(',', '').astype(float)
bse2000['cff_2023'] = bse2000['cff_2023'].str.replace(',', '').astype(float)
bse2000['cff_2022'] = bse2000['cff_2022'].str.replace(',', '').astype(float)
bse2000['depreciation_2024'] = bse2000['depreciation_2024'].str.replace(',', '').astype(float)

# mitigating for other income hacks
bse2000['sales_2024'] = bse2000['sales_2024'] + bse2000['other_income_2024']
bse2000['sales_2023'] = bse2000['sales_2023'] + bse2000['other_income_2023']
bse2000['sales_2022'] = bse2000['sales_2022'] + bse2000['other_income_2022']



#EBIT
bse2000['EBIT_2024'] = (bse2000['sales_2024'] - bse2000['expenses_2024'] + bse2000['interest_2024'])
bse2000['EBIT_2023'] = (bse2000['sales_2023'] - bse2000['expenses_2023'] + bse2000['interest_2023'])
bse2000['EBIT_2022'] = (bse2000['sales_2022'] - bse2000['expenses_2022'] + bse2000['interest_2022'])




# operating margin
# Calculate operating margin for each year
bse2000['operating_margin_24'] = bse2000['EBIT_2024']/bse2000['sales_2024']
bse2000['operating_margin_23'] = bse2000['EBIT_2023']/bse2000['sales_2023']
bse2000['operating_margin_22'] = bse2000['EBIT_2022']/bse2000['sales_2022']


# Compute the average operating margin
bse2000['avg_operating_margin'] = bse2000[['operating_margin_24', 'operating_margin_23', 'operating_margin_22']].mean(axis=1)

# P/R
bse2000['shares_outstanding'] = bse2000['MCap']/bse2000['Price']
bse2000['P/R'] = bse2000['Price']*bse2000['shares_outstanding']/bse2000['sales_2024']

# cash proxy, other current assests used ( 20% of avg other assests )
bse2000['cash'] = ((bse2000['other_assets_2024'] + bse2000['other_assets_2023'] + bse2000['other_assets_2022'] )/3)*0.2

# fixed assets = non-operating assets


# capex proxy CFI

# CA and CL making
bse2000['CA_2024'] = bse2000['cwip_2024'] + bse2000['investments_2024'] + bse2000['other_assets_2024']
bse2000['CA_2023'] = bse2000['cwip_2023'] + bse2000['investments_2023'] + bse2000['other_assets_2023']
bse2000['CA_2022'] = bse2000['cwip_2022'] + bse2000['investments_2022'] + bse2000['other_assets_2022']

# CL = other_liabilites
bse2000.rename(columns={'other_liabilities_2024': 'CL_2024'}, inplace=True)
bse2000.rename(columns={'other_liabilities_2023': 'CL_2023'}, inplace=True)
bse2000.rename(columns={'other_liabilities_2022': 'CL_2022'}, inplace=True)

# change in working capital
bse2000['Change_WC_24-23'] = (bse2000['CA_2024'] - bse2000['CL_2024']) - (bse2000['CA_2023'] - bse2000['CL_2023'])
bse2000['Change_WC_23-22'] = (bse2000['CA_2023'] - bse2000['CL_2023']) - (bse2000['CA_2022'] - bse2000['CL_2022'])

# reinvestment rate
bse2000['Reinv_rate_24'] = (bse2000['Change_WC_24-23'] + bse2000['cfi_2024'])/ bse2000['EBIT_2024']
bse2000['Reinv_rate_23'] = (bse2000['Change_WC_23-22'] + bse2000['cfi_2023'])/ bse2000['EBIT_2023']

#equity
bse2000['Equity_2024'] = (bse2000['equity_capital_2024'] + bse2000['reserves_2024'])
bse2000['Equity_2023'] = (bse2000['equity_capital_2023'] + bse2000['reserves_2023'])
bse2000['Equity_2022'] = (bse2000['equity_capital_2022'] + bse2000['reserves_2022'])

#invested capital
bse2000['invested_capital_2024'] = (bse2000['Equity_2024'] + bse2000['borrowings_2024'])
bse2000['invested_capital_2023'] = (bse2000['Equity_2023'] + bse2000['borrowings_2023'])
bse2000['invested_capital_2022'] = (bse2000['Equity_2022'] + bse2000['borrowings_2022'])

#ROC
bse2000['ROC_2024'] = (bse2000['EBIT_2024'] / bse2000['invested_capital_2024']).round(2)
bse2000['ROC_2023'] = (bse2000['EBIT_2023'] / bse2000['invested_capital_2023'])
bse2000['ROC_2022'] = (bse2000['EBIT_2022'] / bse2000['invested_capital_2022'])

bse2000['ROE'] = ((bse2000['EBIT_2024'] - (bse2000['depreciation_2024']))*0.7 / bse2000['Equity_2024']).round(2)


# sales/capital
bse2000['sales_to_capital_24-23'] = (bse2000['sales_2024'] - bse2000['sales_2023']) / (bse2000['invested_capital_2024'] - bse2000['invested_capital_2023'] )
bse2000['sales_to_capital_23-22'] = (bse2000['sales_2023'] - bse2000['sales_2022']) / (bse2000['invested_capital_2023'] - bse2000['invested_capital_2022'] )

#debt%
bse2000['debt%_2024'] = (bse2000['borrowings_2024'] / bse2000['invested_capital_2024'])
bse2000['debt%_2023'] = (bse2000['borrowings_2023'] / bse2000['invested_capital_2023'])
bse2000['debt%_2022'] = (bse2000['borrowings_2022'] / bse2000['invested_capital_2022'])

#cost of debt, Kd, insolvency issues ratios
bse2000['avg_interest_coverage_ratio'] = (((bse2000['EBIT_2024']/bse2000['interest_2024']) + (bse2000['EBIT_2024']/bse2000['interest_2024']) + (bse2000['EBIT_2024']/bse2000['interest_2024']))/3)
bse2000['DE'] = ((bse2000['borrowings_2024']/bse2000['Equity_2024']) + (bse2000['borrowings_2023']/bse2000['Equity_2023'])/2).round(2)
bse2000['debt_ratio'] = (bse2000['borrowings_2024']/(bse2000['fixed_assets_2024']+bse2000['CA_2024'])).round(2)

# ratios
bse2000['EV'] = bse2000['MCap'] + bse2000['borrowings_2024'] - bse2000['cash']
bse2000['EV2EBITDA'] = (bse2000['EV'] / ( bse2000['EBIT_2024'] + bse2000['depreciation_2024'] )).round(2)
bse2000['EV2invested_capital'] = (bse2000['EV'] / bse2000['invested_capital_2024']).round(2)
bse2000['price2sales'] = (bse2000['MCap'] / bse2000['sales_2024']).round(2)
bse2000['EV2sales'] = (bse2000['EV'] / bse2000['sales_2024']).round(2)


# Calculate CAGR for each company
bse2000['sales_CAGR'] = ((((bse2000['sales_2024'] / bse2000['sales_2022']) ** (1/2)) - 1)*100).round(0)



# print(bse2000)
##############################################################################################################################################
def assign_kd(row):
    ic = row['avg_interest_coverage_ratio']
    industry = str(row['Industry']).lower()
    mkt_cap = str(row['MCap_category']).lower()

    if 'financials' in industry:
        # Financials spread table
        if ic <= 0.049999:
            return 0.19
        elif ic <= 0.099999:
            return 0.155
        elif ic <= 0.199999:
            return 0.101
        elif ic <= 0.299999:
            return 0.0728
        elif ic <= 0.399999:
            return 0.0442
        elif ic <= 0.499999:
            return 0.03
        elif ic <= 0.599999:
            return 0.0261
        elif ic <= 0.749999:
            return 0.0183
        elif ic <= 0.899999:
            return 0.0155
        elif ic <= 1.199999:
            return 0.012
        elif ic <= 1.49999:
            return 0.0095
        elif ic <= 1.99999:
            return 0.0085
        elif ic <= 2.49999:
            return 0.0077
        elif ic <= 2.99999:
            return 0.006
        else:  # ic > 3
            return 0.0045

    else:
        if mkt_cap == 'large':
            # Large non-financial firms spread table
            if ic <= 0.199999:
                return 0.19
            elif ic <= 0.649999:
                return 0.155
            elif ic <= 0.799999:
                return 0.101
            elif ic <= 1.249999:
                return 0.0728
            elif ic <= 1.499999:
                return 0.0442
            elif ic <= 1.749999:
                return 0.03
            elif ic <= 1.999999:
                return 0.0261
            elif ic <= 2.249999:
                return 0.0183
            elif ic <= 2.49999:
                return 0.0155
            elif ic <= 2.999999:
                return 0.012
            elif ic <= 4.249999:
                return 0.0095
            elif ic <= 5.499999:
                return 0.0085
            elif ic <= 6.499999:
                return 0.0077
            elif ic <= 8.499999:
                return 0.006
            else:  # ic > 8.5
                return 0.0045
        else:
            # Smaller and riskier non-financial service firms
            if ic <= 0.499999:
                return 0.19
            elif ic <= 0.799999:
                return 0.155
            elif ic <= 1.249999:
                return 0.101
            elif ic <= 1.499999:
                return 0.0728
            elif ic <= 1.999999:
                return 0.0442
            elif ic <= 2.499999:
                return 0.03
            elif ic <= 2.999999:
                return 0.0261
            elif ic <= 3.499999:
                return 0.0183
            elif ic <= 3.999999:
                return 0.0155
            elif ic <= 4.499999:
                return 0.012
            elif ic <= 5.999999:
                return 0.0095
            elif ic <= 7.499999:
                return 0.0085
            elif ic <= 9.499999:
                return 0.0077
            elif ic <= 12.499999:
                return 0.006
            elif ic <= 100000:
                return 0.0045
            else:
                return 0.0045  # fallback if any

# Apply the function to the DataFrame
bse2000['Kd'] = bse2000.apply(assign_kd, axis=1)
# risk free rate + country DS
bse2000['Kd'] = (bse2000['Kd'] + 0.075 + 0.0126)*100
#############################################################################################################################################


# cost of equity, Ke
# large cos beta : 1 , mid beta : 1.2 , small : 1.4 , micro : 1.6 , nano : 1.8
beta_values = {'Large': 1.0, 'Mid': 1.2, 'Small': 1.4, 'Micro': 1.6, 'Nano': 1.8}
bse2000['Beta'] = bse2000['MCap_category'].map(beta_values)
bse2000['Beta'] = bse2000['Beta'].astype(float)

# risk free rate = 10 yr india bond( 7.5%) , Equity risk premium ( 13.5% market return - 7.5% Rf = 6%), now 1.26% added for country risk premium = 7.26% final
bse2000['Ke'] = 7.5 + (7.26 * bse2000['Beta'])

# Add 2% to Ke if stock is Nano or Micro (but not more than once for other conditions)
bse2000.loc[bse2000['MCap_category'].isin(['Nano', 'Micro']), 'Ke'] += 2

# Add 2% to Ke only if stock price is less than 10 INR and not already adjusted for Nano/Micro
bse2000.loc[(bse2000['Price'] < 10) & (~bse2000['MCap_category'].isin(['Nano', 'Micro'])), 'Ke'] += 2

# WACC
bse2000['WACC'] = (bse2000['Kd']* bse2000['debt%_2024']) + (bse2000['Ke']* (1-bse2000['debt%_2024']))

# asset tunrover
bse2000['asset_turnover'] = bse2000['sales_2024'] / ((bse2000['fixed_assets_2024']) + bse2000['CA_2024'])

#capex/rev
bse2000['capex/revenue'] = -(bse2000['cfi_2024'] / bse2000['sales_2024'])


# bse2000.to_csv("final_bse4.csv", index=False)


# print(bse2000[:200])
print(bse2000['Industry'].unique())
print(bse2000['Sub-Industry'].unique())
# Filter rows where industry is 'financials', then get unique sub-industry values
unique_sub_industries = bse2000[bse2000['Industry'].str.lower() == 'financials']['Sub-Industry'].unique()

print(unique_sub_industries)

# bse_steel = bse2000[bse2000["Sub-Industry"] == 'Steel']
sub_industry_avg_margin = bse2000.groupby('Sub-Industry')['avg_operating_margin'].mean().reset_index()

# Sort the result alphabetically by sub-industry
sub_industry_avg_margin = sub_industry_avg_margin.sort_values(by='Sub-Industry')

# Display the result
print(sub_industry_avg_margin)


# Assuming your DataFrame is named `df` and the column is called 'sub_industry'
filtered_df = bse2000[bse2000['Sub-Industry'] == 'Financial Svcs. (Non-bank & Insurance)']

# Print selected columns
print(filtered_df[['MCap', 'operating_margin_24', 'operating_margin_23', 'operating_margin_22', 'ROC_2024','ROC_2023','ROC_2022']].median())


#### major finding : negative shareholder equity leads to weird DE, which inturn spoils WACC. remedy ?
filtered_bse = bse2000[(bse2000['WACC'] > 25) | (bse2000['WACC'] < 10)]

# Select and print required columns
print(filtered_bse[['Name', 'MCap', 'Kd', 'Ke','DE','debt%_2024', 'WACC']])

# print(bse_steel)

import matplotlib.pyplot as plt

plt.figure(figsize=(10, 6))
plt.scatter(range(len(bse2000)), bse2000['WACC'], alpha=0.7, color='teal')

plt.title('Scatter Plot of WACC - bse2000')
plt.xlabel('Index')
plt.ylabel('WACC')
plt.grid(True)
plt.show()


