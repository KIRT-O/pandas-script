import pandas as pd


# Load the CSV file into a DataFrame
# "sep" to make delimiter ';' instead of ',', and to remove duplicate semicolons
# engine='python' to avoid error with regex separator
df = pd.read_csv('data/messy_IMDB.csv', na_values=['NULL', 'null', 'None', 'none','Nan', 'NaN', 'nan', ''], on_bad_lines='warn', skipinitialspace=True, sep=r'\;+', engine='python', ) 

######### Handle blanks and spaces #########

# clean extra spaces of headers names 
df.columns = df.columns.str.strip()

# Clean all text columns by removing all extra spaces
text_columns = df.select_dtypes(include=["object", "string"]).columns
for col in text_columns: df[col] = (df[col].str.replace(r"\s+", " ", regex=True).str.strip())

# Delete all blank lines
df = df.dropna(how="all")

########### Handle 'Release year' column ###########

# make the 'Release year' column to datetime format, and if there is an error, it will be set to NaT, and then format it to 'yy/mm/dd' format
df['Release year'] = pd.to_datetime(df['Release year'], errors='coerce').dt.strftime(r'%Y/%m/%d')

# using (ffill) to automatically fill the missing values in the 'Release year' column with the previous valid value
df['Release year'] = df['Release year'].ffill()

############ Handle 'Genre' column ###########

# make first letter of each word in the 'Genre' column to uppercase (title case)
df['Genre'] = df['Genre'].str.title()

# make every "," in the 'Genre' column to ", " (comma and space) and remove extra spaces at the beginning and end of the string
df['Genre'] = df['Genre'].str.replace(r'\s*,\s*', ', ', regex=True).str.strip()

df['Genre'] = df['Genre'].str.replace('Drma', 'Drama')

############ Handle 'Duration' column ###########

# extract only the valid numbers from the text
df['Duration'] = df['Duration'].astype(str).str.extract(r'(\d+)')[0]

# turn every value to number and every invalid or none int turns into "NaN"
df['Duration'] = pd.to_numeric(df['Duration'], errors='coerce')

# make the column to int type
df['Duration'] = df['Duration'].astype('Int64')

############ Handle 'Country' column ###########

# Create a mapping dictionary to correct common misspellings and variations of country names
mapping = {
    'US': 'USA',
    'US.': 'USA',
    'New Zeland': 'New Zealand',
    'New Zesland': 'New Zealand',
    'Italy1': 'Italy',
}

# replace the misspelled country names in the 'Country' column using our mapping dictionary
df['Country'] = df['Country'].replace(mapping)

############# Handle 'Content Rating' column ###########

# setting rating map
rating_map = {
    'Not Rated': 'Unrated',
    'Approved': 'Unrated',
}

# Replace the values in the 'Content Rating' column using the rating_map dictionary
df['Content Rating'] = df['Content Rating'].replace(rating_map)

########### Handle 'Director' column ###########

# Delete all extra spaces at the beginning and end of the string in the 'Director' column
df['Director'] = df['Director'].str.strip()

# delete all extra spaces between words in the 'Director' column
df['Director'] = df['Director'].str.replace(r'\s+', ' ', regex=True)

########### Handle 'Income' column ###########

# turn the 'income' column to string type to be able to apply string operations
df['Income'] = df['Income'].astype(str)

# make every "o" to "0" (zero) to avoid confusion between letter "o" and number "0"
df['Income'] = df['Income'].str.replace('o', '0', case=False)

# delete everything not a digit like "$" or "," or " " or any other character, and keep only the numbers and the decimal point
# the regex pattern r'[^\d.]' means: delete anything except digits and the decimal point
df['Income'] = df['Income'].str.replace(r'[^\d.]', '', regex=True)

# 4. convert the column to a numeric type (float or int)
df['Income'] = pd.to_numeric(df['Income'], errors='coerce')

############# Handle 'Votes' column ###########

# make the column string type to be able to apply string operations
df['Votes'] = df['Votes'].astype(str).str.replace('.', '', regex=False).str.strip()

# Delete everything not a digit like "," or " " or any other character, and keep only the numbers
df['Votes'] = df['Votes'].str.replace(r'[^\d]', '', regex=True)

# make the data type into int type, and if there is an error, it will be set to NaN
df['Votes'] = pd.to_numeric(df['Votes'], errors='coerce').astype('Int64')

############# Handle 'Score' column ###########

# Turn the column into string type to be able to apply string operations, and remove extra spaces at the beginning and end of the string
df['Score'] = df['Score'].astype(str).str.strip()

# make a series of string replacements to clean the 'Score' column
df['Score'] = (
    df['Score']
    .str.replace(r',', '.', regex=False)         # convert "," to "." (8,8 -> 8.8)
    .str.replace(':', '.', regex=False)          # convert ":" to "." (8:8 -> 8.8)
    .str.replace(r'\.+', '.', regex=True)        # merge repeated dots (8..8 -> 8.8)
    .str.replace(r'^\.', '0.',  regex=True)      # add 0 before dot at the beginning (.0 -> 0.0 or .4 -> 0.4)
    .str.replace(r'\.$', '.0', regex=True)       # add 0 after dot at the end (9. -> 9.0)
    .str.replace(r'e-?0$', '.0', regex=True)     # fix formats like (7e-0 -> 7.0)
)

# take first number from the string, and ignore other like (++, f, e-0)
df['Score'] = df['Score'].str.extract(r'(\d+\.?\d*)')[0]

# Final conversion of the Score column to floating-point numbers
df['Score'] = pd.to_numeric(df['Score'], errors='coerce')

#####################################################################
##################### Finish the cleaning process ###################
####################################################################

# move everything to new csv file
df.to_csv('data/cleaned.csv', index=False)