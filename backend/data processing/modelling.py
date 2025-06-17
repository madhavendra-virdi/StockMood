import pandas as pd
import numpy as np


pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)
pd.set_option('display.colheader_justify', 'center')
pd.set_option("display.max_colwidth", None)


bse1200 = pd.read_csv('final_bse4.csv')

#bse1200 = bse1200[bse1200["Sub-Industry"] == 'Broadcasting']
bse1200 = bse1200.drop_duplicates(subset = 'Name')
print(bse1200.columns.tolist())

industry_rates_df = pd.read_excel("industry_rates.xlsx")  # Adjust file path as needed

# print(industry_rates_df)

growth_rate_dict = industry_rates_df.set_index("Industry Name")["Expected Growth in EBIT"].to_dict()
roic_dict = industry_rates_df.set_index("Industry Name")["ROC"].to_dict()

print(growth_rate_dict)
print(roic_dict)


def generate_growth_series(start_rate, years=11, final_rate=5):
    """
    Generates a list of growth rates decreasing linearly from start_rate to final_rate over the given years.
    """
    return [round(rate) for rate in np.linspace(start_rate * 100, final_rate, years)]  # Convert to percentage format and round off

bse1200 = bse1200[bse1200["Sub-Industry"].isin(growth_rate_dict.keys())]


bse1200["Revenue Growth Rates"] = bse1200["Sub-Industry"].map(lambda sub: generate_growth_series(growth_rate_dict.get(sub, 5)))

def forecast_revenue(sales_2024, growth_rates):
    """
    Generates a list of forecasted revenues based on sales_2024 and growth rates.
    """
    revenues = [sales_2024 * (1 + growth_rates[0] / 100)]
    for rate in growth_rates[1:]:
        revenues.append(revenues[-1] * (1 + rate / 100))
    return [round(rate) for rate in revenues ]

bse1200["Forecasted Revenues"] = bse1200.apply(lambda row: forecast_revenue(row["sales_2024"], row["Revenue Growth Rates"]), axis=1)


# Find the biggest player in each Sub-Industry
biggest_players = bse1200.groupby("Sub-Industry")["sales_2024"].max().to_dict()

# Compare the last forecasted revenue with the biggest player
bse1200["Comparison with Biggest Player"] = bse1200.apply(lambda row: row["Forecasted Revenues"][-1] >= biggest_players[row["Sub-Industry"]], axis=1)

# Generate operating margin forecast
def generate_operating_margin_series(current_margin, industry_avg, years=11):
    """
    Generates a list of operating margins transitioning from the current margin to the industry average.
    - If negative, it recovers to 0 in 3 years before increasing towards the industry average.
    - If positive, it directly transitions to the industry average.
    """
    if current_margin < 0:
        # Gradual recovery: First 3 years to turn positive
        recovery_path = [
            current_margin,
            current_margin / 3,  # Year 2: Less negative
            current_margin / 8  # Year 3: Near zero but still negative
        ]
        # Ensuring last value is slightly positive
        recovery_path[-1] = max(recovery_path[-1], 0.02)
        remaining_years = years - len(recovery_path)
        final_transition = np.linspace(recovery_path[-1], industry_avg, remaining_years).tolist()
        return [round(margin, 2) for margin in (recovery_path + final_transition)]
    else:
        return [round(margin, 2) for margin in np.linspace(current_margin, industry_avg, years)]

op_margin_dict = industry_rates_df.set_index("Industry Name")["avg operating margin ( bse_1200)"].to_dict()

bse1200["operating_margin_24"] = pd.to_numeric(bse1200["operating_margin_24"], errors='coerce').fillna(0)

bse1200["Operating Margin Forecast"] = bse1200.apply(
    lambda row: generate_operating_margin_series(row["operating_margin_24"], op_margin_dict[row["Sub-Industry"]]), axis=1
)

# Generate forecasting edit (Revenue * Operating Margin)
def calculate_forecasting_edit(revenue_forecast, margin_forecast):
    """
    Multiplies each year's forecasted revenue with the corresponding year's operating margin.
    """
    return [round(rev * margin, 2) for rev, margin in zip(revenue_forecast, margin_forecast)]

bse1200["Forecasted EBIT"] = bse1200.apply(
    # 0.7 for 30% corporate tax, post tax EBIT
    lambda row: [round(ebit * 0.7, 2) for ebit in calculate_forecasting_edit(row["Forecasted Revenues"], row["Operating Margin Forecast"])],
    axis=1
)


bse1200["growth in operating income"] = bse1200["Forecasted EBIT"].apply(lambda x: round((x[-1] / 0.7) - x[0]/0.7, 2))


# Define scenario lists
scenario_1 = [1.2, 1.5, 1.9, 2.3, 2.7, 2.7, 2.7, 2.7, 2.7, 2.7] # growth phase
scenario_2 = [1.35, 1.2, 1.05, 0.9, 0.75, 0.65, 0.55, 0.45, 0.35, 0.3] # mature phase
scenario_3 = [1.3, 1.6, 2.0, 2.4, 2.5, 2.5, 2.5, 2.1, 1.7, 1.3] # uncertain s curve
scenario_4 = [1.0, 1.0, 1.1, 1.2, 1.6, 2.1, 2.5, 2.8, 3.0, 3.2] ## Scenario 4: Delayed Growth (CapEx First, Sales Later)
scenario_5 = [1.4, 1.6, 1.7, 1.5, 1.3, 1.6, 2.0, 2.4, 2.7, 2.9] # Scenario 5: Reinvestment Dip Then Growth
scenario_6 = [1.1, 1.3, 1.6, 2.0, 2.5, 3.1, 3.8, 4.6, 5.5, 6.5] # Scenario 6: Exponential Growth
scenario_7 = [1.1, 1.2, 1.3, 1.3, 2.0, 2.0, 2.1, 2.2, 2.3, 2.3] # Scenario 7: Step-Change (e.g., New Plant Launch)
scenario_8 = [1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0] # Scenario 8: Low and Flat (Efficiency Ceiling)
scenario_9 = [1.1, 1.4, 1.8, 2.2, 2.5, 2.7, 2.7, 2.7, 2.7, 2.7] # Scenario 9: Mid-Growth, Then Maturity
scenario_10 = [1.2, 1.1, 1.0, 1.3, 1.8, 2.2, 2.0, 2.3, 2.5, 2.7] # Scenario 10: W-Shaped Recovery

# Assign lists to every row in new columns
bse1200['sales/capital scenario 1'] = [scenario_1] * len(bse1200)
bse1200['sales/capital scenario 2'] = [scenario_2] * len(bse1200)
bse1200['sales/capital scenario 3'] = [scenario_3] * len(bse1200)
bse1200['sales/capital scenario 4'] = [scenario_4] * len(bse1200)
bse1200['sales/capital scenario 5'] = [scenario_5] * len(bse1200)
bse1200['sales/capital scenario 6'] = [scenario_6] * len(bse1200)
bse1200['sales/capital scenario 7'] = [scenario_7] * len(bse1200)
bse1200['sales/capital scenario 8'] = [scenario_8] * len(bse1200)
bse1200['sales/capital scenario 9'] = [scenario_9] * len(bse1200)
bse1200['sales/capital scenario 10'] = [scenario_10] * len(bse1200)



roic_dict = industry_rates_df.set_index("Industry Name")["ROC"].to_dict()

def calculate_reinvestment(industry_name, revenue_forecast, sales_2024, sales_capital_scenario, ebit_forecast):
    """
    Calculates forecasted reinvestment for each year based on sales/capital ratio.
    """
    reinvestment = [(revenue_forecast[0] - sales_2024) / sales_capital_scenario[0]]

    for i in range(1, len(sales_capital_scenario)):
        reinvestment.append((revenue_forecast[i] - revenue_forecast[i - 1]) / sales_capital_scenario[i])

    # append 11th terminal reinvestment value
    roic = roic_dict.get(industry_name,1)  # Default to 1 if industry not found to avoid division by zero
    terminal_reinvestment = (0.05 / roic) * ebit_forecast[-1]
    reinvestment.append(round(terminal_reinvestment, 2))

    return [round(x, 2) for x in reinvestment]

def industry_roic(industry_name):
    """
    Calculates forecasted reinvestment for each year based on sales/capital ratio.
    """
    # append 11th terminal reinvestment value
    roic = roic_dict.get(industry_name,1)  # Default to 1 if industry not found to avoid division by zero

    return roic

bse1200["Industry ROIC"] = bse1200.apply(
    lambda row: industry_roic(row['Sub-Industry']),
    axis=1
)

# bse1200["Forecasted Reinvestment Scenario 1"] = bse1200.apply(
#     lambda row: print(row.name, calculate_reinvestment(row['Sub-Industry'], row["Forecasted Revenues"], row["sales_2024"], row["sales/capital scenario 1"])),
#     axis=1
# )

# Compute reinvestment for all three scenarios
for i in range(1, 11):
    scenario_col = f"sales/capital scenario {i}"
    output_col = f"Forecasted Reinvestment Scenario {i}"

    bse1200[output_col] = bse1200.apply(
        lambda row: calculate_reinvestment(
            row['Sub-Industry'],
            row["Forecasted Revenues"],
            row["sales_2024"],
            row[scenario_col],
            row['Forecasted EBIT']
        ),
        axis=1)

import pandas as pd

def calculate_year_10_roic(row, scenario):
    try:
        # Year 10 ROIC = EBIT[10] / Invested Capital[10]
        year_10_ebit = row["Forecasted EBIT"][9]  # 10th value (index 9)

        # Invested Capital Year 10 = Sum of all reinvestments except the last one (terminal value)
        reinvestment_column = f"Forecasted Reinvestment Scenario {scenario}"
        invested_capital_10 = sum(row[reinvestment_column][:-1]) + row['invested_capital_2024']

        # Avoid division by zero
        year_10_roic = year_10_ebit / invested_capital_10

        return round(year_10_roic, 4)

    except Exception as e:
        print(f"Error at row {row.name}: {e}")
        return None

# Apply the function for each scenario
for i in range(1, 11):
    bse1200[f"Year 10 ROIC({i})"] = bse1200.apply(lambda row: calculate_year_10_roic(row, i), axis=1)


def calculate_total_reinvestment(row, scenario):
    try:
        reinvestment_column = f"Forecasted Reinvestment Scenario {scenario}"
        total_reinvestment = sum(row[reinvestment_column])

        return total_reinvestment

    except Exception as e:
        print(f"Error at row {row.name}: {e}")
        return None

# Apply the function for each scenario
for i in range(1, 11):
    bse1200[f"total_reinvestment({i})"] = bse1200.apply(lambda row: calculate_total_reinvestment(row, i), axis=1)



# Display updated DataFrame

#print(bse1200[:-200].iloc[:, [0] + list(range(-14, 0))])
# columns_to_keep = [
#     'Name', 'Ticker', 'Sub-Industry', 'Industry', 'MCap_category', 'WACC', 'Beta','borrowings_2024','cash','other_assets_2024','shares_outstanding',
#     'Revenue Growth Rates', 'Forecasted Revenues', 'Operating Margin Forecast',
#     'Comparison with Biggest Player', 'Forecasted EBIT', 'growth in operating income',
#     'sales/capital scenario 1', 'sales/capital scenario 2', 'sales/capital scenario 3',
#     'Industry ROIC',
#     'Forecasted Reinvestment Scenario 1', 'Forecasted Reinvestment Scenario 2', 'Forecasted Reinvestment Scenario 3',
#     'Year 10 ROIC(1)', 'Year 10 ROIC(2)', 'Year 10 ROIC(3)',
#     'total_reinvestment(1)', 'total_reinvestment(2)', 'total_reinvestment(3)'
# ]


# Create the new filtered DataFrame
new_df = bse1200


def select_best_scenario_and_calculate_fcff(row):
    industry_roic = row['Industry ROIC']
    ebit_list = row['Forecasted EBIT']
    op_income_growth = row['growth in operating income']

    best_score = float('inf')
    best_scenario = None
    best_fcff = None

    for i in range(1, 11):
        # Extract values for scenario i
        year10_roic = row[f'Year 10 ROIC({i})']
        total_reinv = row[f'total_reinvestment({i})']
        reinv_list = row[f'Forecasted Reinvestment Scenario {i}']

        # Avoid division by zero
        roic_score = abs(year10_roic - industry_roic) / industry_roic if industry_roic != 0 else float('inf')
        growth_score = abs(total_reinv - op_income_growth) / op_income_growth if op_income_growth != 0 else float('inf')

        score = (roic_score + growth_score) / 2  # simple average

        if score < best_score:
            best_score = score
            best_scenario = i
            best_fcff = [ebit - reinv for ebit, reinv in zip(ebit_list, reinv_list)]

    # Check if fcff is None or contains all NaNs or very small/invalid numbers
    if best_fcff is None or all(pd.isna(x) for x in best_fcff) or all(x is None or x != x for x in best_fcff):
        # Default to scenario 6
        best_scenario = 9
        reinv_list = row[f'Forecasted Reinvestment Scenario 6']
        best_fcff = [ebit - reinv for ebit, reinv in zip(ebit_list, reinv_list)]

    return pd.Series([best_scenario, best_fcff], index=['best_scenario', 'fcff'])



# Apply the function to the DataFrame
new_df[['best_scenario', 'fcff']] = new_df.apply(select_best_scenario_and_calculate_fcff, axis=1)


def discount_fcff_with_terminal(row):
    wacc = row['WACC']/100
    fcff = row['fcff']

    if not isinstance(fcff, list) or len(fcff) != 11:
        return None

    try:
        # Discount years 1–10
        pv_fcff = [fcff[i] / ((1 + wacc) ** (i + 1)) for i in range(10)]

        # Terminal value based on 11th year FCFF
        g = 0.05
        terminal_value = fcff[10] / (wacc - g)
        pv_terminal = terminal_value / ((1 + wacc) ** 10)

        # Append the PV of terminal value as the final element
        pv_fcff.append(pv_terminal)

        return pv_fcff
    except Exception as e:
        print(f"Error in row {row.name}: {e}")
        return None

# Check which values can't be converted to numeric
# invalid_wacc_rows = new_df[pd.to_numeric(new_df['WACC'], errors='coerce').isna()]
#
# # Display the problematic rows and values
# print("🚨 Rows with invalid WACC values:")
# print(invalid_wacc_rows[['WACC']])  # You can add more columns if needed for context
#


new_df['WACC'] = pd.to_numeric(new_df['WACC'], errors='coerce')  # convert invalid strings to NaN
new_df['WACC'].replace([np.inf, -np.inf], np.nan, inplace=True)  # replace inf/-inf with NaN
new_df['WACC'] = new_df['WACC'].fillna(9)  # fill NaNs (including former infs) with 10%




new_df['PV_FCFF'] = new_df.apply(discount_fcff_with_terminal, axis=1)


def calculate_share_price(row):
    pv_fcff = row['PV_FCFF']
    debt = row['borrowings_2024']
    cash = row['cash']
    non_assets = row['other_assets_2024']
    shares_outstanding = row['shares_outstanding']  # prevent division by zero

    if not isinstance(pv_fcff, list):
        return None

    try:
        total_value = sum(pv_fcff) - debt + cash + non_assets
        share_price = total_value / shares_outstanding
        return share_price
    except Exception as e:
        print(f"Error in row {row.name}: {e}")
        return None

new_df['share_price'] = new_df.apply(calculate_share_price, axis=1)

scenario_behavior_map = {
    1: "Steady growth + plateau / Blue chips / stable industries",
    2: "Decline/ Risky/mature declining sectors",
    3: "Boom → bust/Cyclical / hype sectors",
    4: "Delayed take-off/Infra / pharma /high upfront CapEx",
    5: "Reinvestment dip → rise/Manufacturing /CapEx-heavy",
    6: "Exponential/High-growth tech/startups",
    7: "Step change/Event-driven /capacity-based",
    8: "Flat low/Utilities /commodity suppliers",
    9: "Moderate growth → maturity/Consumer goods /mid-cap firms",
    10: "W-recovery/Macro-shock or turnaround bets"
}

new_df["Scenario Behavior Description"] = new_df["best_scenario"].map(scenario_behavior_map)


def convert_numpy_floats(df):
    return df.applymap(lambda x: [float(i) if isinstance(i, np.float64) else i for i in x] if isinstance(x, list) else x)

new_df = convert_numpy_floats(new_df)

#print(new_df.dtypes)
print(new_df)

missing_best_scenario = new_df[new_df['best_scenario'].isna()]
print(missing_best_scenario)



# Assuming your DataFrame is named `df` and the column is called 'sub_industry'
# filtered_df = new_df[new_df['Sub-Industry'] == 'Steel']
#
# # Print selected columns
# print(filtered_df[['Name', 'MCap','Price','share_price','best_scenario','Scenario Behavior Description']])


# import seaborn as sns
# import matplotlib.pyplot as plt
#
# # Plot count of best_scenario by MCap_category
# sns.countplot(x='MCap_category', hue='best_scenario', data=new_df, palette='pastel', edgecolor='black')
# plt.title('Best Scenario Distribution by Market Cap Category')
# plt.xlabel('Market Cap Category')
# plt.ylabel('Count')
# plt.legend(title='Best Scenario')
# plt.grid(axis='y', linestyle='--', alpha=0.7)
# plt.show()


new_df.to_csv("bse1200_modelling10.csv", index=False)
print(len(new_df.columns))

