import pandas as pd
import re
import io 


# open csv file without pandas
with open('messy_IMDB.csv', 'r') as file:
    raw_text = file.read()

# fix with regex to remove extra spaces and commas in digits
fixed_text = re.sub(r'(?<=\d)\s*,\s*(?=\d)', '', raw_text)  # remove spaces around commas

# fix dates
fixed_text = re.sub(r'\-', '/', fixed_text)

# read csv file with pandas, using "io.StringIO" to read from the fixed text string
# the "comment='#'" argument tells pandas to ignore lines starting with '#'
# using "skipinitialspace=True" to skip spaces after the delimiter
df = pd.read_csv(io.StringIO(fixed_text), comment='#', skipinitialspace=True) 

# delete extra spaces in all string columns
df = df.map(lambda x: " ".join(str(x).split()) if isinstance(x, str) else x)


df = df.replace(r'\;', ',', regex=True)  # replace semicolons with commas

#df["Join Date"] = df["Join Date"].apply(fix_date)

# convert "id" column to integer
df['id'] = df['id'].astype('Int64')

print(df.index)
print(df.columns.tolist())

# save the cleaned dataframe to a new csv file
df.to_csv('cleaned.csv', index=False)