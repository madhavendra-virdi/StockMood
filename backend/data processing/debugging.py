import pandas as pd
from sklearn.linear_model import LinearRegression
import numpy as np

# Sample data
json_data = [
    {
        "Name": "ACC Limited (NSEI:ACC)",
        "Price": "1888",
        "MCap_category": "Large",
        "Kd": "9.21",
        "Ke": "14.76",
        "DE": "0.03",
        "debt_ratio": "0.02",
        "debt_percent_2024": "0.0212765957446808",
        "PE": "15.6",
        "EV2EBITDA": "7.36",
        "ROE": "0.13",
        "ROC_2024": "0.24",
        "sales_CAGR": "13.0",
        "EV2invested_capital": "2.13",
        "price2sales": "1.82",
        "EV2sales": "1.72"
    },
    {
        "Name": "JK Lakshmi Cement Limited (BSE:500380)",
        "Price": "776",
        "MCap_category": "Mid",
        "Kd": "9.53",
        "Ke": "16.212",
        "DE": "0.99",
        "debt_ratio": "0.27",
        "debt_percent_2024": "0.3953708973629292",
        "PE": "27.5",
        "EV2EBITDA": "7.46",
        "ROE": "0.23",
        "ROC_2024": "0.24",
        "sales_CAGR": "12.0",
        "EV2invested_capital": "2.16",
        "price2sales": "1.4",
        "EV2sales": "1.66"
    },
    {
        "Name": "Shree Cement Limited (NSEI:SHREECEM)",
        "Price": "29730",
        "MCap_category": "Large",
        "Kd": "9.21",
        "Ke": "14.76",
        "DE": "0.15",
        "debt_ratio": "0.06",
        "debt_percent_2024": "0.0740641352475513",
        "PE": "54.2",
        "EV2EBITDA": "12.94",
        "ROE": "0.12",
        "ROC_2024": "0.24",
        "sales_CAGR": "17.0",
        "EV2invested_capital": "4.21",
        "price2sales": "4.45",
        "EV2sales": "4.45"
    },
    {
        "Name": "The India Cements Limited (NSEI:INDIACEM)",
        "Price": "307",
        "MCap_category": "Mid",
        "Kd": "13.18",
        "Ke": "16.212",
        "DE": "0.72",
        "debt_ratio": "0.24",
        "debt_percent_2024": "0.3195410716465275",
        "PE": "",
        "EV2EBITDA": "14.87",
        "ROE": "0.03",
        "ROC_2024": "0.05",
        "sales_CAGR": "3.0",
        "EV2invested_capital": "1.23",
        "price2sales": "1.57",
        "EV2sales": "1.93"
    },
    {
        "Name": "J.K. Cement Limited (BSE:532644)",
        "Price": "5112",
        "MCap_category": "Large",
        "Kd": "9.53",
        "Ke": "14.76",
        "DE": "1.6",
        "debt_ratio": "0.37",
        "debt_percent_2024": "0.5083363869549286",
        "PE": "59.2",
        "EV2EBITDA": "13.04",
        "ROE": "0.27",
        "ROC_2024": "0.24",
        "sales_CAGR": "20.0",
        "EV2invested_capital": "3.85",
        "price2sales": "3.2",
        "EV2sales": "3.6"
    },
    {
        "Name": "The KCP Limited (NSEI:KCP)",
        "Price": "200",
        "MCap_category": "Small",
        "Kd": "9.36",
        "Ke": "17.664",
        "DE": "0.57",
        "debt_ratio": "0.17",
        "debt_percent_2024": "0.2539682539682539",
        "PE": "11.3",
        "EV2EBITDA": "4.89",
        "ROE": "0.19",
        "ROC_2024": "0.25",
        "sales_CAGR": "17.0",
        "EV2invested_capital": "1.44",
        "price2sales": "0.88",
        "EV2sales": "0.93"
    }
]

def predict_price(data_json):
    df = pd.DataFrame(data_json)

    # Convert numeric columns
    for col in df.columns:
        if col not in ['Name', 'MCap_category']:
            df[col] = pd.to_numeric(df[col], errors='coerce')

    # Fill missing PE with 0
    df['PE'] = df['PE'].fillna(0)


    # Drop rows with other missing values (if any remain)
    df.dropna(inplace=True)

    # Encode MCap_category
    df['MCap_category'] = df['MCap_category'].map({'Small': 0, 'Mid': 1, 'Large': 2})

    # Separate last row for prediction
    predict_row = df.head(1)
    train_df = df.iloc[1:]

    # Features and target
    X_train = train_df.drop(columns=['Name', 'Price'])
    y_train = train_df['Price']
    X_predict = predict_row.drop(columns=['Name', 'Price'])

    # Train model
    model = LinearRegression()
    model.fit(X_train, y_train)

    # Predict
    predicted_price = model.predict(X_predict)

    return float(predicted_price[0])

# Run prediction
if __name__ == "__main__":
    result = predict_price(json_data)
    print("Predicted Price of last stock:", result)
