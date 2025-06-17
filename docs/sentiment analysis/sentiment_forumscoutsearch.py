import pandas as pd


pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)
pd.set_option('display.colheader_justify', 'center')
pd.set_option("display.max_colwidth", None)


stock_talks = pd.read_csv('stocktalks.csv')


# 311 rows, 65 facebook(21%), 39 reddit(13%), 31 quora(13%), 25 ambitionBox, 22 teamBHP, 14 upstox community, 9 tradingQnA by zerodha, 9 shiksha ask n answer, 7 desidime, 6 technofino
# 50% of talks on facebook, reddit, quora

import nltk
nltk.download('vader_lexicon')
from nltk.sentiment import SentimentIntensityAnalyzer

sia = SentimentIntensityAnalyzer()
# sia.lexicon.get("fall")  # Try printing this

stock_talks['scores'] = stock_talks['title'].apply(lambda x: sia.polarity_scores(str(x)))
stock_talks['compound'] = stock_talks['scores'].apply(lambda x: x['compound'])
stock_talks['sentiment'] = stock_talks['compound'].apply(lambda x: 'Positive' if x > 0.05 else 'Negative' if x < -0.05 else 'Neutral')




# 175 of 311 stocks are neutral
# import matplotlib.pyplot as plt
#
# stock_talks['compound'].hist(bins=30, edgecolor='black')
# plt.title('Histogram of Compound Sentiment Scores')
# plt.xlabel('Compound Score')
# plt.ylabel('Frequency')
# plt.grid(True)
# plt.show()



# from transformers import AutoTokenizer, AutoModelForSequenceClassification, pipeline
#
# # Load FinBERT sentiment model
# model_name = "ProsusAI/finbert"
# tokenizer = AutoTokenizer.from_pretrained(model_name)
# model = AutoModelForSequenceClassification.from_pretrained(model_name)
#
# # Create sentiment analysis pipeline
# finbert = pipeline("sentiment-analysis", model=model, tokenizer=tokenizer)
#
# stock_talks['finbert_sentiment'] = stock_talks['title'].apply(lambda x: finbert(str(x))[0]['label'])

# # (2)  attempt to find hindi text failed
# import langid
# stock_talks['language'] = stock_talks['title'].apply(lambda x: langid.classify(str(x))[0])



print(stock_talks)