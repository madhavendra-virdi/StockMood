import requests
import pymysql
import logging
from datetime import datetime

# === CONFIG ===
REDDIT_CLIENT_ID = 'XD8cQQrFUr7w8D5jZ3dd5g'
REDDIT_CLIENT_SECRET = 'X2zAw9NslTlJjVkhX-5hwGtnFfjbjw'
REDDIT_USER_AGENT = 'StockMood/0.1 by Outrageous-Pie-122'
KEYWORD = "Infosys"
SORT = "top"
LIMIT = 100
TIME_FILTER = "month"

# === LOGGING ===
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# === DB CONNECTION ===
def get_db_connection():
    try:
        connection = pymysql.connect(
            host='localhost',
            port=3306,
            user='root',
            password='stockpulse',
            database='my_database',
            cursorclass=pymysql.cursors.DictCursor
        )
        return connection
    except Exception as e:
        logger.error(f"❌ Database connection failed: {str(e)}")
        return None


# === REDDIT AUTH ===
def get_reddit_token():
    try:
        auth = requests.auth.HTTPBasicAuth(REDDIT_CLIENT_ID, REDDIT_CLIENT_SECRET)
        headers = {'User-Agent': REDDIT_USER_AGENT}
        data = {'grant_type': 'client_credentials'}

        token_response = requests.post(
            'https://www.reddit.com/api/v1/access_token',
            auth=auth,
            data=data,
            headers=headers
        )

        token_response.raise_for_status()
        access_token = token_response.json().get("access_token")
        if not access_token:
            raise Exception("Access token not found.")
        return access_token
    except Exception as e:
        logger.error(f"❌ Reddit token fetch failed: {str(e)}")
        return None
import pandas as pd

# === FETCH POSTS ===
def fetch_reddit_posts(keyword, sort, limit, time_filter):
    token = get_reddit_token()
    if not token:
        return []

    headers = {
        "Authorization": f"bearer {token}",
        "User-Agent": REDDIT_USER_AGENT
    }

    params = {
        "q": f'"{keyword}"',
        "sort": sort,
        "limit": 100,
        "t": 'month'
    }

    try:
        response = requests.get("https://oauth.reddit.com/search", headers=headers, params=params)
        response.raise_for_status()
        posts = response.json().get("data", {}).get("children", [])
        logger.info(f"📥 Fetched {len(posts)} Reddit posts.")
        df = pd.DataFrame(posts)
        df = pd.DataFrame(df['data'])
        print(df)
        return posts
    except Exception as e:
        logger.error(f"❌ Failed to fetch Reddit posts: {str(e)}")
        return []


# === INSERT INTO DB ===
def insert_posts(posts, keyword):
    conn = get_db_connection()
    if not conn:
        return

    inserted = 0

    try:
        with conn.cursor() as cursor:
            for post in posts:
                data = post["data"]
                title = data.get("title", "")
                url = f"https://www.reddit.com{data.get('permalink', '')}"
                subreddit = data.get("subreddit", "")
                author = data.get("author", "")
                snippet = data.get("selftext", "")[:200]
                created_at = datetime.utcfromtimestamp(data.get("created_utc", datetime.utcnow().timestamp()))

                sql = """
                    INSERT INTO RedditPosts (stock_name, title, url, subreddit, author, created_at, snippet)
                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                """
                try:
                    cursor.execute(sql, (keyword, title, url, subreddit, author, created_at, snippet))
                    inserted += 1
                    logger.info(f"✅ Inserted: {title[:30]}...")
                except Exception as e:
                    logger.warning(f"⚠️ Skipped insert: {str(e)}")

        conn.commit()
        logger.info(f"🟢 Inserted {inserted} posts into the database.")
    except Exception as e:
        logger.error(f"❌ DB error: {str(e)}")
    finally:
        conn.close()


# === MAIN ===
if __name__ == '__main__':
    posts = fetch_reddit_posts(KEYWORD, SORT, LIMIT, TIME_FILTER)
    if posts:
        insert_posts(posts, KEYWORD)
    else:
        logger.info("No posts to insert.")
