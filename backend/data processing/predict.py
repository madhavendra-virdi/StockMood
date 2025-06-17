from flask import Flask, request, jsonify
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split

app = Flask(__name__)

# Initialize the model
model = RandomForestRegressor()


# Endpoint for training and prediction
@app.route('/predict', methods=['POST'])
def predict():
    # Get the data from the request
    data = request.json.get('data')

    if not data:
        return jsonify({'error': 'No data provided'}), 400

    # Convert the data to a DataFrame
    df = pd.DataFrame(data)

    # Ensure 'Price' column is present for training
    if 'Price' not in df.columns:
        return jsonify({'error': "'Price' column is missing"}), 400

    # Split the DataFrame into predictors (X) and target (y)
    X = df.drop(columns=['Price', 'Name'])  # Exclude 'Price' and 'Name'
    y = df['Price']

    # Train the model (simple approach here)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    model.fit(X_train, y_train)

    # For prediction, let's assume you send one row of data for prediction
    prediction_data = X.tail(1)  # Get the last row (could be adjusted based on your logic)

    # Predict the price
    predicted_price = model.predict(prediction_data)

    # Return the prediction to the frontend
    return jsonify({'predicted_price': predicted_price[0]})


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
