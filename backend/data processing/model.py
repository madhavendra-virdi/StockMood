import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error
import numpy as np

# Ensure all rows and columns of the DataFrame are displayed
pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)
pd.set_option('display.colheader_justify', 'center')

bse1200 = pd.read_csv('final_bse_1200.csv')

#bse1200 = bse1200[bse1200["Sub-Industry"] == 'Broadcasting']
bse1200 = bse1200.drop_duplicates(subset = 'Name')


print(bse1200.columns.tolist())

selected_columns = ['Name', 'Price','shares_outstanding', 'MCap','P/E','P/R','sales_2024','cash','fixed_assets_2024','operating_margin_24','sales_to_capital_24-23','Equity_2024','Equity_2023','Equity_2022','invested_capital_2024','invested_capital_2023','invested_capital_2022','debt%_2024','debt%_2023','debt%_2022']  # Replace with your column names
bse_model = bse1200[selected_columns]

#print(bse_model)


# Drop the Name column as it's not useful for modeling
df = bse_model.drop(columns=['Name'])
X = df.drop(columns=['Price'])
y = df['Price']
X = X.fillna(0)
X.replace([np.inf, -np.inf], 0, inplace=True)

# Train-test split (80-20 split)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train a Random Forest Regressor
model = RandomForestRegressor(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Predict on test set and evaluate
y_pred = model.predict(X_test)
mae = mean_absolute_error(y_test, y_pred)
print(f"Mean Absolute Error: {mae}")

# Predict price for all records in the dataset
df['Predicted_Price'] = model.predict(X)

# Display first few predictions
print(df[['Price', 'Predicted_Price']])
