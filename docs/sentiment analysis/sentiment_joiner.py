from transformers import pipeline
import time
import pandas as pd

dfr = pd.read_csv('sentiment_analysis_reddit.csv')
dft = pd.read_csv('sentiment_analysis_twitter.csv')


pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)
pd.set_option('display.colheader_justify', 'center')
pd.set_option("display.max_colwidth", None)


print(len(dfr))
print(len(dft))
print(dfr.columns)
print(dft.columns)
print(dfr[:2])
print(dft[:2])

# Standardize column names to match the unified structure
dfr = pd.DataFrame({
    'stock': dfr['stock_name'],
    'title': dfr['title'],
    'url': dfr['url'],
    'subreddit': dfr['subreddit'],
    'author': dfr['author'],
    'created_at': dfr['created_at'],
    'snippet': dfr['snippet'],
    'text': dfr['text'],
    'type': dfr['type'],
    'platform' : 'reddit'
})

dft = pd.DataFrame({
    'stock': dft['stock'],         # Rename 'stock' to 'stock_name'
    'title': '',                        # No title in Twitter
    'url': dft['url'],
    'subreddit': '',                    # No subreddit in Twitter
    'author': dft['author'],
    'created_at': dft['date'],          # Rename 'date' to 'created_at'
    'snippet': dft['snippet'],
    'text': dft['snippet'],                         # snippet text same thing, title not there in twitter
    'type': dft['type'],
    'platform': 'twitter'

})

# Combine both cleaned DataFrames
df_combined = pd.concat([dfr, dft], ignore_index=True)

# Sort by stock_name
df_combined = df_combined.sort_values(by='stock', ascending=True).reset_index(drop=True)

# Add serial number
df_combined.insert(0, 'serial_number', range(1, len(df_combined) + 1))

# Preview the result
# print(df_combined.tail(130))



# Start timer
print("START")
start_time = time.time()
classifier = pipeline('sentiment-analysis', model='ProsusAI/finbert')

# print(classifier("The company's revenue decreased significantly."))

def get_sentiment_info(text):
    result = classifier(str(text))[0]  # Get the first (and only) result
    return pd.Series([result['label'], result['score']])


df_combined[['label', 'score']] = df_combined['text'].apply(get_sentiment_info)
print(df_combined)
df_combined.to_csv("finalsm_sentiment.csv", index=False)
end_time = time.time()
print(f"\n✅ Sentiment analysis completed in {(end_time - start_time)/60:.2f} minutes.")
