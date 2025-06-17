from flask import Flask, jsonify, request
import pymysql
import logging
from flask_cors import CORS
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
import time
import re
import smtplib
from email.message import EmailMessage

from werkzeug.security import generate_password_hash, check_password_hash
from pymysql.err import IntegrityError


# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize Flask app
app = Flask(__name__)

# Enable CORS for the entire app
CORS(app, resources={r"/*": {"origins": "*"}}, supports_credentials=True)

#email format for verification
EMAIL_REGEX = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\\.[a-zA-Z0-9-.]+$"

# Database connection
def get_db_connection():
    try:
        connection = pymysql.connect(
            host='mysql',
            user='root',
            password='stockpulse',
            database='my_database',
            cursorclass=pymysql.cursors.DictCursor
        )
        return connection
    except Exception as e:
        logger.error(f"Database connection failed: {str(e)}")
        return None

@app.before_request
def check_json():
    if request.method in ['POST', 'PUT'] and not request.is_json:
        return jsonify({"error": "Content-Type must be application/json"}), 400



@app.route('/stocks', methods=['GET'])
def get_stocks():
    connection = get_db_connection()
    if connection is None:
        return jsonify({"error": "Database connection failed"}), 500

    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT DISTINCT Name FROM FinancialData")
            stocks = [row['Name'] for row in cursor.fetchall()]

        connection.close()
        return jsonify({"stocks": stocks})

    except Exception as e:
        logger.error(f"Error fetching stock list: {str(e)}")
        return jsonify({"error": "Failed to fetch stocks"}), 500



@app.route('/stock/<string:stock_name>', methods=['GET'])
def get_stock_details(stock_name):
    connection = get_db_connection()
    if connection is None:
        return jsonify({"error": "Database connection failed"}), 500

    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM FinancialData WHERE Name = %s", (stock_name,))
            stock_data = cursor.fetchall()

        connection.close()

        if not stock_data:
            return jsonify({"error": "Stock not found"}), 404

        return jsonify({"stock_details": stock_data})

    except Exception as e:
        logger.error(f"Error fetching stock details: {str(e)}")
        return jsonify({"error": "Failed to fetch stock details"}), 500



@app.route('/sentiment/<string:stock_name>', methods=['GET'])
def get_stock_sentiment(stock_name):
    connection = get_db_connection()
    if connection is None:
        return jsonify({"error": "Database connection failed"}), 500

    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM SentimentData WHERE stock = %s", (stock_name,))
            stock_sentiment = cursor.fetchall()

        connection.close()

        if not stock_sentiment:
            return jsonify({"error": "Stock not found"}), 404
        logger.error(stock_sentiment)
        return jsonify({"stock_details": stock_sentiment})

    except Exception as e:
        logger.error(f"Error fetching stock details: {str(e)}")
        return jsonify({"error": "Failed to fetch stock details"}), 500

@app.route('/stocks/subindustry/<string:stock_name>', methods=['GET'])
def get_stocks_by_subindustry(stock_name):
    connection = get_db_connection()
    if connection is None:
        return jsonify({"error": "Database connection failed"}), 500

    try:
        with connection.cursor() as cursor:
            # Get the Sub_Industry of the selected stock
            cursor.execute("SELECT Sub_Industry FROM FinancialData WHERE Name = %s", (stock_name,))
            result = cursor.fetchone()

            if not result:
                return jsonify({"error": "Stock not found"}), 404

            sub_industry = result['Sub_Industry']

            # Fetch all stocks in the same Sub_Industry excluding the selected stock
            cursor.execute("SELECT DISTINCT Name FROM FinancialData WHERE Sub_Industry = %s",
                           (sub_industry))
            stocks = [row['Name'] for row in cursor.fetchall()]

        connection.close()
        return jsonify({"stocks_in_subindustry": stocks})

    except Exception as e:
        logger.error(f"Error fetching stocks in sub-industry: {str(e)}")
        return jsonify({"error": "Failed to fetch stocks"}), 500


# Initialize model
model = RandomForestRegressor()

#Endpoint for training and prediction
# @app.route('/predict', methods=['POST'])
# def predict():
#     # Get the data from the request
#     data = request.json.get('data')
#
#     if not data:
#         return jsonify({'error': 'No data provided'}), 400
#
#     # Convert the data to a DataFrame
#     df = pd.DataFrame(data)
#
#     # Ensure 'Price' column is present for training
#     if 'Price' not in df.columns:
#         return jsonify({'error': "'Price' column is missing"}), 400
#
#     # Split the DataFrame into predictors (X) and target (y)
#     X = df.drop(columns=['Price', 'Name'])  # Exclude 'Price' and 'Name'
#     y = df['Price']
#
#     # Train the model (simple approach here)
#     X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
#     model.fit(X_train, y_train)
#
#     # For prediction, let's assume you send one row of data for prediction
#     prediction_data = X.tail(1)  # Get the last row (could be adjusted based on your logic)
#
#     # Predict the price
#     predicted_price = model.predict(prediction_data)
#
#     # Return the prediction to the frontend
#     return jsonify({'predicted_price': predicted_price[0]})
#
#
# # Handling CORS pre-flight requests (OPTIONS)
# @app.route('/predict', methods=['OPTIONS'])
# def options_predict():
#     return '', 200


@app.route('/predict', methods=['POST'])
def predict():
    try:
        logger.error(request)
        req_json = request.get_json()
        logger.error(req_json)
        if not req_json:
            return jsonify({'error': 'No JSON received'}), 400

        # Extract parts of the payload
        stock_data = req_json.get('data')
        selected_stock_name = req_json.get('selectedStock')

        # Validate presence of required fields
        if not stock_data or not selected_stock_name:
            return jsonify({'error': 'Missing "data" or "selectedStock" in request'}), 400

        # Create DataFrame from received data
        df = pd.DataFrame(stock_data)
        #logger.error(df)

        # Convert numeric columns, leave 'Name' untouched
        for col in df.columns:
            if col != 'Name':
                df[col] = pd.to_numeric(df[col], errors='coerce')

        logger.error(df)
        # Prepare features and target
        X = df.drop(columns=['Price', 'Name'], errors='ignore')
        y = df['Price']

        logger.error(f"X shape: {X.shape}, y shape: {y.shape}")

        # Train model
        #X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        model.fit(X, y)

        # Find the row matching the selected stock
        selected_row = df[df['Name'] == selected_stock_name]
        logger.error(selected_row)
        if selected_row.empty:
            return jsonify({'error': f'Stock "{selected_stock_name}" not found in data'}), 404

        prediction_data = selected_row.drop(columns=['Price', 'Name'], errors='ignore')
        predicted_price = model.predict(prediction_data)
        logger.error(predicted_price)

        return str(predicted_price)

    except Exception as e:
        logger.error(f"Error processing prediction request: {str(e)}", exc_info=True)
        return jsonify({'error': 'Internal server error'}), 500

@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    first_name = data.get('first_name')
    last_name = data.get('last_name')
    username = data.get('username')
    password = data.get('password')
    plan = data.get('plan', 'Free')  # default to Free if not provided

    password_hash = generate_password_hash(password)

    connection = get_db_connection()
    if connection is None:
        return jsonify({"error": "Database connection failed"}), 500

    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM Users WHERE username = %s", (username,))
            if cursor.fetchone():
                return jsonify({"success": False, "message": "Username already exists"}), 400

            cursor.execute("""
                INSERT INTO Users (first_name, last_name, username, password_hash, plan)
                VALUES (%s, %s, %s, %s, %s)
            """, (first_name, last_name, username, password_hash, plan))

        connection.commit()
        return jsonify({"success": True, "message": "User registered successfully", "username": username})

    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500

    finally:
        connection.close()

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    connection = get_db_connection()
    if connection is None:
        return jsonify({"error": "Database connection failed"}), 500

    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM Users WHERE username = %s", (username,))
            user = cursor.fetchone()

            if user and check_password_hash(user['password_hash'], password):
                return jsonify({"success": True, "message": "Login successful", "username": username})
            else:
                return jsonify({"success": False, "message": "Invalid credentials"}), 401

    finally:
        connection.close()

@app.route('/user/<username>', methods=['GET'])
def get_user(username):
    connection = get_db_connection()
    if connection is None:
        return jsonify({"error": "DB connection failed"}), 500

    try:
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT first_name, last_name, username, plan
                FROM Users
                WHERE username = %s
            """, (username,))
            user = cursor.fetchone()
            if user:
                return jsonify(user)
            else:
                return jsonify({"error": "User not found"}), 404
    finally:
        connection.close()


@app.route('/favorite-stock', methods=['POST'])
def favorite_stock():
    data = request.get_json()
    username = data.get('username')
    stock = data.get('stock_symbol')

    conn = get_db_connection()
    with conn.cursor() as cursor:
        try:
            cursor.execute(
                "INSERT INTO UserFavorites (username, stock_symbol) VALUES (%s, %s)",
                (username, stock)
            )
            conn.commit()
            return jsonify({"success": True, "message": f"{stock} added to favorites"})
        except IntegrityError:
            return jsonify({"success": False, "message": f"{stock} already favorited"}), 409

@app.route('/unfavorite-stock', methods=['POST'])
def unfavorite_stock():
    data = request.get_json()
    username = data.get('username')
    stock = data.get('stock_symbol')

    conn = get_db_connection()
    with conn.cursor() as cursor:
        cursor.execute("DELETE FROM UserFavorites WHERE username = %s AND stock_symbol = %s", (username, stock))
    conn.commit()
    return jsonify({"success": True, "message": f"{stock} removed from favorites"})

@app.route('/user-favorites/<username>', methods=['GET'])
def get_user_favorites(username):
    conn = get_db_connection()
    with conn.cursor() as cursor:
        cursor.execute("SELECT stock_symbol FROM UserFavorites WHERE username = %s", (username,))
        favorites = cursor.fetchall()
    return jsonify([row['stock_symbol'] for row in favorites])

@app.route('/stock/<symbol>', methods=['GET'])
def get_stock_by_name(symbol):
    connection = get_db_connection()
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM FinancialData WHERE Name = %s", (symbol,))
            stock = cursor.fetchone()
            if stock:
                return jsonify(stock)
            else:
                return jsonify({"error": "Stock not found"}), 404
    finally:
        connection.close()

#reddit crypto info
@app.route('/reddit/fetch-crypto', methods=['POST'])
def fetch_crypto_reddit_posts():
    import requests
    import time
    from datetime import datetime
    from flask import request, jsonify

    REDDIT_CLIENT_ID = 'XD8cQQrFUr7w8D5jZ3dd5g'
    REDDIT_CLIENT_SECRET = 'X2zAw9NslTlJjVkhX-5hwGtnFfjbjw'
    REDDIT_USER_AGENT = 'StockMood/0.1 by Outrageous-Pie-122'

    try:
        # Get CoinGecko Top 100 Crypto Names
        coingecko_url = "https://api.coingecko.com/api/v3/coins/markets"
        params = {"vs_currency": "usd", "order": "market_cap_desc", "per_page": 100, "page": 1}
        response = requests.get(coingecko_url, params=params)
        if response.status_code != 200:
            return jsonify({"error": "Failed to fetch from CoinGecko"}), 500

        crypto_names = [coin["name"] for coin in response.json()]

        # Get Reddit Token
        auth = requests.auth.HTTPBasicAuth(REDDIT_CLIENT_ID, REDDIT_CLIENT_SECRET)
        headers = {'User-Agent': REDDIT_USER_AGENT}
        data = {'grant_type': 'client_credentials'}
        token_response = requests.post('https://www.reddit.com/api/v1/access_token', auth=auth, data=data, headers=headers)

        if token_response.status_code != 200:
            return jsonify({"error": "Failed to get Reddit token"}), 500

        access_token = token_response.json().get("access_token")
        if not access_token:
            return jsonify({"error": "Token not received"}), 500

        input_data = request.get_json() or {}
        sort = input_data.get("sort", "relevance")
        limit = int(input_data.get("limit", 100))
        time_filter = input_data.get("time", "month")
        if limit < 1 or limit > 100:
            limit = 100

        headers = {
            "Authorization": f"bearer {access_token}",
            "User-Agent": REDDIT_USER_AGENT
        }

        reddit_url = "https://oauth.reddit.com/search"
        connection = get_db_connection()
        if connection is None:
            return jsonify({"error": "Database connection failed"}), 500

        inserted_total = 0
        for name in crypto_names:
            query = f'"{name}"'
            params = {
                "q": query,
                "sort": sort,
                "limit": limit,
                "t": time_filter
            }

            reddit_res = requests.get(reddit_url, headers=headers, params=params)
            if reddit_res.status_code != 200:
                time.sleep(1)
                continue

            posts = reddit_res.json().get("data", {}).get("children", [])
            inserted_count = 0

            with connection.cursor() as cursor:
                for post in posts:
                    data = post["data"]
                    title = data.get("title", "")
                    url = f"https://www.reddit.com{data.get('permalink', '')}"
                    subreddit = data.get("subreddit", "")
                    author = data.get("author", "")
                    body = data.get("selftext", "")
                    created_at = datetime.utcfromtimestamp(data.get("created_utc", datetime.utcnow().timestamp()))
                    score = data.get("score", 0)
                    num_comments = data.get("num_comments", 0)
                    flair = data.get("link_flair_text")
                    is_oc = data.get("is_original_content", False)
                    awards = data.get("total_awards_received", 0)

                    cursor.execute("""
                        INSERT INTO RedditPosts (
                            topic, title, url, subreddit, author, created_at, body, score,
                            num_comments, link_flair_text, is_original_content, total_awards_received
                        )
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                    """, (
                        name, title, url, subreddit, author, created_at, body, score,
                        num_comments, flair, is_oc, awards
                    ))
                    inserted_count += 1

            inserted_total += inserted_count
            time.sleep(1)  # ✅ Delay to respect Reddit rate limits

        connection.commit()
        connection.close()

        return jsonify({"message": f"✅ {inserted_total} Reddit posts inserted for top 100 cryptocurrencies."})

    except Exception as e:
        app.logger.error("❌ Error in /reddit/fetch-crypto: %s", str(e), exc_info=True)
        return jsonify({"error": "Internal server error"}), 500


#twitter posts
@app.route('/twitter/fetch-crypto', methods=['POST'])
def fetch_crypto_tweets():
    import requests
    import time
    from datetime import datetime
    from flask import request, jsonify

    TWITTER_BEARER_TOKEN = "AAAAAAAAAAAAAAAAAAAAAEi%2FyQEAAAAA0I7I23wLGfRD8WIWnrkncsWA3aA%3DsK7xr4vCy0xmlcvXxmoiiIHmylqakqptqAN5GlsGW4qgix2OmL"
    TWITTER_API_URL = "https://api.twitter.com/2/tweets/search/recent"

    headers = {
        "Authorization": f"Bearer {TWITTER_BEARER_TOKEN}"
    }

    try:
        # Get top 100 cryptos
        cg_res = requests.get("https://api.coingecko.com/api/v3/coins/markets", params={
            "vs_currency": "usd",
            "order": "market_cap_desc",
            "per_page": 100,
            "page": 1
        })

        if cg_res.status_code != 200:
            return jsonify({"error": "Failed to fetch from CoinGecko"}), 500

        crypto_names = [coin["name"] for coin in cg_res.json()][:90]  # limit to 90 cryptos


        connection = get_db_connection()
        if connection is None:
            return jsonify({"error": "Database connection failed"}), 500

        inserted_total = 0

        for name in crypto_names:
            query = f'"{name}" lang:en -is:retweet'
            params = {
                "query": query,
                "max_results": "10",
                "tweet.fields": "created_at,public_metrics,lang,source",
                "expansions": "author_id"
            }

            twitter_res = requests.get(TWITTER_API_URL, headers=headers, params=params)
            if twitter_res.status_code != 200:
                time.sleep(1)
                continue

            res_json = twitter_res.json()
            tweets = res_json.get("data", [])

            with connection.cursor() as cursor:
                for tweet in tweets:
                    tweet_id = tweet["id"]
                    author_id = tweet["author_id"]
                    created_at = tweet["created_at"]
                    content = tweet["text"]
                    metrics = tweet["public_metrics"]
                    lang = tweet.get("lang", "en")
                    source = tweet.get("source", "")

                    cursor.execute("""
                                   INSERT IGNORE INTO TwitterPosts (
                            topic, tweet_id, author, created_at, content, retweet_count,
                            like_count, reply_count, quote_count, lang, source
                        )
                        VALUES (%s,%s, %s,%s,%s,%s,%s,%s,%s,%s,%s)
                    """, (
                        name,
                        tweet_id,
                        author_id,
                        created_at,
                        content,
                        metrics.get("retweet_count", 0),
                        metrics.get("like_count", 0),
                        metrics.get("reply_count", 0),
                        metrics.get("quote_count", 0),
                        lang,
                        source
                    ))
                    inserted_total += 1

            time.sleep(1)

        connection.commit()
        connection.close()

        return jsonify({"message": f"✅ Inserted {inserted_total} tweets for top 100 cryptos."})

    except Exception as e:
        app.logger.error("❌ Error in /twitter/fetch-crypto: %s", str(e), exc_info=True)
        return jsonify({"error": "Internal server error"}), 500


@app.route('/forumscout/fetch-crypto', methods=['POST'])
def fetch_crypto_from_forumscout():
    import requests
    import time
    from datetime import datetime
    from flask import request, jsonify

    TOKENS = [
        "9515370cde0677fed9ad412b0dcc015fc90f0d1627964d8d9346419fa73cf683",
        "09a6d290cbf3d7994868a2edff4891da8b87ca466fadf6f669ad0255f0e00f93"
    ]
    API_URL = "https://forumscout.app/api/x_search"
    token_index = 0
    request_count = 0

    try:
        # Fetch top 100 cryptos
        cg_res = requests.get("https://api.coingecko.com/api/v3/coins/markets", params={
            "vs_currency": "usd",
            "order": "market_cap_desc",
            "per_page": 100,
            "page": 1
        })

        if cg_res.status_code != 200:
            return jsonify({"error": "Failed to fetch from CoinGecko"}), 500

        crypto_names = [coin["name"] for coin in cg_res.json()]
        connection = get_db_connection()
        if connection is None:
            return jsonify({"error": "Database connection failed"}), 500

        inserted_total = 0
        for name in crypto_names:
            # Handle token rotation
            if request_count == 50:
                token_index = 1
            elif request_count >= 100:
                break

            headers = {
                "X-API-Key": TOKENS[token_index]
            }

            params = {
                "keyword": name,
                "sort_by": "Latest",
                "page": 1
            }

            response = requests.get(API_URL, headers=headers, params=params)
            request_count += 1

            if response.status_code != 200:
                print(f"❌ Error for {name}: {response.status_code}")
                time.sleep(1)
                continue

            tweets = response.json()
            inserted_count = 0

            with connection.cursor() as cursor:
                for tweet in tweets:
                    tweet_url = tweet["url"]
                    tweet_date = datetime.strptime(tweet["date"], "%Y-%m-%d %H:%M:%S")
                    author = tweet["author"]
                    title = tweet["title"]
                    snippet = tweet["snippet"]
                    source = tweet["source"]

                    cursor.execute("""
                        INSERT IGNORE INTO TwitterPosts (
                            topic, tweet_url, tweet_date, author, title, snippet, source
                        )
                        VALUES (%s, %s, %s, %s, %s, %s, %s)
                    """, (
                        name, tweet_url, tweet_date, author, title, snippet, source
                    ))
                    inserted_count += 1

            inserted_total += inserted_count
            time.sleep(1)

        connection.commit()
        connection.close()

        return jsonify({"message": f"✅ {inserted_total} tweets inserted from ForumScout for top 100 cryptos."})

    except Exception as e:
        app.logger.error("❌ Error in /forumscout/fetch-crypto: %s", str(e), exc_info=True)
        return jsonify({"error": "Internal server error"}), 500

# code for contact us and email notification for admin and user

def send_admin_notification(name, email, company, message_text):
    try:
        msg = EmailMessage()
        msg['Subject'] = 'New Contact Form Submission'
        msg['From'] = 'contactstockmood@gmail.com'
        msg['To'] = 'msvirdi@my.yorku.ca'

        msg.set_content(f"""
        You have a new contact submission:

        Name: {name}
        Email: {email}
        Company: {company}
        Message:
        {message_text}
        """)

        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login('contactstockmood@gmail.com', 'wgoz uavk fpgt kqjj')
            smtp.send_message(msg)
    except Exception as e:
        print(f"Admin email failed: {e}")

def send_user_confirmation(email, name):
    try:
        msg = EmailMessage()
        msg['Subject'] = 'We Received Your Message'
        msg['From'] = 'contactstockmood@gmail.com'
        msg['To'] = email

        msg.set_content(f"""
        Hi {name},

        Thanks for contacting us! We've received your message and will get back to you shortly.

        - The StockMood Team
        """)

        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login('contactstockmood@gmail.com', 'wgoz uavk fpgt kqjj')
            smtp.send_message(msg)
    except Exception as e:
        print(f"User confirmation email failed: {e}")

@app.route('/contact', methods=['POST'])
def contact():
    try:
        print("Raw request body:", request.data)
        data = request.get_json(force=True)
        print("Parsed JSON:", data)
    except Exception as e:
        print("Error parsing JSON:", str(e))
        return jsonify({"success": False, "message": "Invalid JSON"}), 400

    name = data.get('name')
    email = data.get('email')
    company = data.get('company', '')
    message = data.get('message')

    if not name or not email or not message:
        print("Missing required field(s). Name:", name, "| Email:", email, "| Message:", message)
        return jsonify({"success": False, "message": "Name, email, and message are required"}), 400

    connection = get_db_connection()
    if connection is None:
        return jsonify({"error": "Database connection failed"}), 500

    try:
        with connection.cursor() as cursor:
            cursor.execute("""
                INSERT INTO ContactMessages (name, email, company, message)
                VALUES (%s, %s, %s, %s)
            """, (name, email, company, message))
        connection.commit()

        # Optionally: send email notifications here
        send_admin_notification(name, email, company, message)
        send_user_confirmation(email, name)

        return jsonify({"success": True, "message": "Message submitted successfully"}), 200

    except Exception as e:
        print("Database error:", str(e))
        return jsonify({"success": False, "message": str(e)}), 500

    finally:
        connection.close()



# Run the Flask app
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
