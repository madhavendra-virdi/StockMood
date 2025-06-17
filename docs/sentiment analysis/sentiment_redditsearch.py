import pandas as pd


pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)
pd.set_option('display.colheader_justify', 'center')
pd.set_option("display.max_colwidth", None)


stock_talks = pd.read_csv('stocktalks_reddit.csv', encoding='ISO-8859-1')
# print(len(stock_talks))
# authors : must_hustle : 10%, time alternative 964 : 5%
# subreddit : IndiaMarketNews : 10%, StockMarketIndia : 8%, InvestmentsTrading : 5%

# shortcomings : Vedanta limited to be used as vedanta / spirtuality
# belfort and lupin is a frnch cartoon, lupin limited to be used
# crusedar kings, britannia empire building
# dark souls villain : havells
# football manager DLF position : DLF
# TVS motors, tvs beng fetched tripl quotes not okringw


# print(stock_talks['subreddit'].value_counts())

stock_talks['text'] = stock_talks['title'] + ' + ' + stock_talks['snippet'].fillna('')
print(stock_talks[stock_talks['text'].isna()])

meme_talks = stock_talks[stock_talks['subreddit'].str.contains('meme', case=False, na=False)]
print("memes")
print(len(meme_talks))
stock_talks = stock_talks.merge(meme_talks, how='outer', indicator=True).query('_merge == "left_only"').drop(columns=['_merge'])


# Define keywords for various corporate actions
keywords1= [
    'revenue','earnings','yoy','fy25','highlight','audit','q4','reports','reported'
]

# Create a regex pattern that covers the list
pattern1 ='|'.join(keywords1)

# Filter rows based on the pattern (case-insensitive)
reporting_talks = stock_talks[
    stock_talks['text'].str.contains(pattern1,case=False, na=False)
]

stock_talks = stock_talks.merge(reporting_talks, how='outer', indicator=True).query('_merge == "left_only"').drop(columns=['_merge'])


# reporting_talks/ annoucements = 39
print("reporting")
print(len(reporting_talks))

stock_talks = stock_talks.merge(reporting_talks, how='outer', indicator=True).query('_merge == "left_only"').drop(columns=['_merge'])

# Define keywords for various corporate actions
keywords2 = [
    'job','exam','interview','hire','walk','internship','placement','looking','salar','package','fresher','cgpa','IIT','IIM','LinkedIN','data engineer role','CV','GATE','BITS','resume','mock test','college'
]

# Create a regex pattern that covers the list
pattern2 = '|'.join(keywords2)

# Filter rows based on the pattern (case-insensitive)
job_talks = stock_talks[
    stock_talks['text'].str.contains(pattern2, case=False, na=False)
]


print("jobs")
print(len(job_talks))

stock_talks = stock_talks.merge(job_talks, how='outer', indicator=True).query('_merge == "left_only"').drop(columns=['_merge'])


keywords3 = [
    'portfolio','advice','help','opinions','Opinion','suggest','help','target','stop loss','recommend','recommends','advise','advises','volume','trading','need','help','GTT','entry point','sell or hold','sell or keep','rallies','sell?','stocks to watch','watchlist','breakout','resistance','technical analysis', 'fundamental analysis',
    'support level', 'oversold', 'overbought', 'RSI', 'MACD', 'chart pattern',
    'indicator', 'investment tip', 'price target', 'short-term',
    'long-term', 'bullish', 'bearish', 'financial advice', 'price action',
    'day trading', 'swing trading', 'intraday', 'multibagger', 'holding period',
    'market outlook', 'sell recommendation', 'buy recommendation',
    'stock tips', 'which stock', 'where to invest', 'entry price', 'exit price',
    'target hit', 'book profit', 'holding stock', 'trailing stop', 'buy zone',
    'risk reward', 'market view', 'stock pick', 'any suggestions',
    'share your views', 'please advise', 'investment idea', 'stock advice',
    'good time to buy', 'should I sell', 'market correction', 'invest now','swing trade'
]

# Create a regex pattern that covers the list
pattern3 = '|'.join(keywords3)

advice_talks = stock_talks[
    stock_talks['text'].str.contains(pattern3, case=False, na=False)
]
print("advice")
print(len(advice_talks))
# print((news_talks))


stock_talks = stock_talks.merge(advice_talks, how='outer', indicator=True).query('_merge == "left_only"').drop(columns=['_merge'])

keywords4 = [
    'news','subsidiary','sale','value','partner','collab','sign','launch','secure','introduce','FII','pakistan','tariff','Times of India','closing bell','wiseinvest.in'
]

# Create a regex pattern that covers the list
pattern4 = '|'.join(keywords4)

news_talks = stock_talks[
    stock_talks['text'].str.contains(pattern4, case=False, na=False)
]
print("news")
print(len(news_talks))
stock_talks = stock_talks.merge(news_talks, how='outer', indicator=True).query('_merge == "left_only"').drop(columns=['_merge'])

# Define keywords for various corporate actions
keywords5 = [
    'dividend', 'stock split', 'merger', 'acquisition','acquire',
    'spin[- ]?off', 'rights issue', 'buyback', 'bonus issue','announced','agreement','received','update','restructuring','headquarter','director','appoint','chairman','board meeting'
]

# Create a regex pattern that covers the list
pattern5 = '|'.join(keywords5)

# Filter rows based on the pattern (case-insensitive)
action_talks = stock_talks[
    stock_talks['text'].str.contains(pattern5, case=False, na=False)
]

# corporate actions : 71
print("corporate actions")
print(len(action_talks))

stock_talks = stock_talks.merge(action_talks, how='outer', indicator=True).query('_merge == "left_only"').drop(columns=['_merge'])

print("total")
print(len(stock_talks))
# stock_talks.to_csv("testing.csv", index=False)

# keywordsx = [
#     'stock','stocks','market','share'
# ]
#
# # Create a regex pattern that covers the list
# patternx = '|'.join(keywordsx)
#
# x_talks = stock_talks[
#     stock_talks['text'].str.contains(patternx, case=False, na=False)
# ]
# print("x")
# print(len(x_talks))
# print("total left")
# print(len(stock_talks))
# print((x_talks))
# stock_talks = stock_talks.merge(advice_talks, how='outer', indicator=True).query('_merge == "left_only"').drop(columns=['_merge'])


# # Combine all snippets into one big string
# all_text = ' '.join(stock_talks['text'].dropna().astype(str))
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

reporting_talks['type'] = 'reporting'
job_talks['type'] = 'jobs'
advice_talks['type'] = 'advice/ due dilligence'
news_talks['type'] = 'news'
action_talks['type'] = 'corporate actions'
stock_talks['type'] = 'discussion'
meme_talks['type'] = 'meme'

final_stocktalks = pd.concat([reporting_talks, action_talks, news_talks, advice_talks, job_talks, stock_talks, meme_talks], ignore_index=True)

final_stocktalks['created_at'] = pd.to_datetime(final_stocktalks['created_at'], unit='d', origin='1899-12-30')
final_stocktalks['created_at'] = final_stocktalks['created_at'].dt.strftime('%Y-%m-%d %H:%M:%S')  # No fractional seconds
print(final_stocktalks[:100])

final_stocktalks.to_csv("sentiment_analysis_reddit.csv", index=False)



