import pandas as pd
import re
bse1200 = pd.read_csv('bse1200_modelling10.csv')

stocks = list(bse1200['Name'])

stocks = [re.sub(r'\s*\([^)]*\)', '', item) for item in stocks]

n = 86
chunk_size = len(stocks) // n  # This will be 17 since 820 / 47 = 17

# Now split into chunks
split_lists = [stocks[i * chunk_size:(i + 1) * chunk_size] for i in range(n)]

print(len(split_lists))        # should print 47
for i, sublist in enumerate(split_lists, start=1):
    print(f"List {i}: {sublist}")
