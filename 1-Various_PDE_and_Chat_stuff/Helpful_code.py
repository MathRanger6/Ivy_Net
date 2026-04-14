df.replace(to_replace=None, value=None, inplace=False, regex=False) ## Replace every instance iof an object in a dataframe
string_exists = df.astype(str).applymap(lambda x: string_to_find in x).any().any() ## Any match
df.isin([string_to_find]).any().any() ## Exact Match