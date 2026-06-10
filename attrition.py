import pandas as pd
import sqlite3

# Load the CSV file
df = pd.read_csv('WA_Fn-UseC_-HR-Employee-Attrition.csv')

# Create SQLite database
conn = sqlite3.connect('attrition.db')

# Load data into SQLite
df.to_sql('employees', conn, if_exists='replace', index=False)

print("Done! Total rows loaded:", len(df))
print(df.head())