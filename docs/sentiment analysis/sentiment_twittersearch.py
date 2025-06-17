import pandas as pd
import time

# Start timer
start_time = time.time()


pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)
pd.set_option('display.colheader_justify', 'center')
pd.set_option("display.max_colwidth", None)


stock_talks = pd.read_csv('stocktalks_twitter.csv', encoding='ISO-8859-1')
#print(stock_talks)

# sherlock 7.2%, updates_trade 5%, cqnow_ 5%, scanx_trade 4.5%
#print(stock_talks['author'].value_counts())


# Define keywords for various corporate actions
keywords1= [
    'revenue','sales','profit','reported','consolidated','call','earnings','report','reported','yoy','results','fy25','highlight','audit','result'
]

# Create a regex pattern that covers the list
pattern1 ='|'.join(keywords1)

# Filter rows based on the pattern (case-insensitive)
reporting_talks = stock_talks[
    stock_talks['snippet'].str.contains(pattern1,case=False, na=False)
]


# reporting_talks/ annoucements = 39
print("reporting")
print(len(reporting_talks))

stock_talks = stock_talks.merge(reporting_talks, how='outer', indicator=True).query('_merge == "left_only"').drop(columns=['_merge'])

# Define keywords for various corporate actions
keywords2 = [
    'dividend', 'stock split', 'merger', 'acquisition','acquire',
    'spin[- ]?off', 'rights issue', 'buyback', 'bonus issue','announced','agreement','received','update','restructuring'
]

# Create a regex pattern that covers the list
pattern2 = '|'.join(keywords2)

# Filter rows based on the pattern (case-insensitive)
action_talks = stock_talks[
    stock_talks['snippet'].str.contains(pattern2, case=False, na=False)
]

# corporate actions : 71
print("corporate")
print(len(action_talks))

stock_talks = stock_talks.merge(action_talks, how='outer', indicator=True).query('_merge == "left_only"').drop(columns=['_merge'])

#print(stock_talks)


keywords3 = [
    'subsidiary','sale','new','value','partner','collab','sign','launch','secure','introduce'
]

# Create a regex pattern that covers the list
pattern3 = '|'.join(keywords3)

news_talks = stock_talks[
    stock_talks['snippet'].str.contains(pattern3, case=False, na=False)
]
print("news")
print(len(news_talks))


stock_talks = stock_talks.merge(news_talks, how='outer', indicator=True).query('_merge == "left_only"').drop(columns=['_merge'])



keywords4 = [
    'target','stop loss','recommend','recommends','advise','advises','volume','trading'
]

# Create a regex pattern that covers the list
pattern4 = '|'.join(keywords4)

advice_talks = stock_talks[
    stock_talks['snippet'].str.contains(pattern4, case=False, na=False)
]
print("advice")
print(len(advice_talks))
stock_talks = stock_talks.merge(advice_talks, how='outer', indicator=True).query('_merge == "left_only"').drop(columns=['_merge'])


keywords5 = [
    'hire','job','walk','internship'
]

# Create a regex pattern that covers the list
pattern5 = '|'.join(keywords5)

job_talks = stock_talks[
    stock_talks['snippet'].str.contains(pattern5, case=False, na=False)
]
print("jobs")
print(len(job_talks))
# print((job_talks))
stock_talks = stock_talks.merge(job_talks, how='outer', indicator=True).query('_merge == "left_only"').drop(columns=['_merge'])

print("total")
print(len(stock_talks))


# # Combine all snippets into one big string
# all_text = ' '.join(stock_talks['snippet'].dropna().astype(str))
# import re
# from collections import Counter
# from nltk.corpus import stopwords
# import nltk
#
# # Download stopwords (only needed the first time)
# nltk.download('stopwords')
#
# # Define English stopwords
# stop_words = set(stopwords.words('english'))
#
#
# # Clean and tokenize text (remove punctuation, lowercase, split words)
# words = re.findall(r'\b\w+\b', all_text.lower())
#
# # Remove stopwords and short tokens (like "a", "is", "3", etc.)
# filtered_words = [word for word in words if word not in stop_words and len(word) > 2 and not word.isdigit()]
#
# # Count frequency of each remaining word
# word_counts = Counter(filtered_words)
#
# # Get top 100 most common meaningful words
# top_100 = word_counts.most_common(100)
#
# # Display results
# for word, count in top_100:
#     print(f"{word}: {count}")

# print(stock_talks['snippet'])

# Example DataFrames: df1, df2, df3, df4, df5
# Add a distinguishing column before concatenation
reporting_talks['type'] = 'reporting'
action_talks['type'] = 'corporate actions'
news_talks['type'] = 'news'
advice_talks['type'] = 'advice/ due dilligence'
job_talks['type'] = 'jobs'
stock_talks['type'] = 'discussion'

# Combine all into one
final_stocktalks = pd.concat([reporting_talks, action_talks, news_talks, advice_talks, job_talks, stock_talks], ignore_index=True)
final_stocktalks.drop(final_stocktalks.columns[7], axis=1, inplace=True)
final_stocktalks.drop(final_stocktalks.columns[8], axis=1, inplace=True)
final_stocktalks.drop(final_stocktalks.columns[7], axis=1, inplace=True)

final_stocktalks['date'] = pd.to_datetime(final_stocktalks['date'], unit='d', origin='1899-12-30')
final_stocktalks['date'] = final_stocktalks['date'].dt.strftime('%Y-%m-%d %H:%M:%S')  # No fractional seconds
# print(final_stocktalks)

from transformers import pipeline

classifier = pipeline('sentiment-analysis', model='ProsusAI/finbert')

# print(classifier("The company's revenue decreased significantly."))

def get_sentiment_info(text):
    result = classifier(str(text))[0]  # Get the first (and only) result
    return pd.Series([result['label'], result['score']])

# final_stocktalks[['label', 'score']] = final_stocktalks['snippet'].apply(get_sentiment_info)

print(final_stocktalks)
final_stocktalks.to_csv("sentiment_analysis_twitter.csv", index=False)
end_time = time.time()
print(f"\n✅ Sentiment analysis completed in {end_time - start_time:.2f} seconds.")




