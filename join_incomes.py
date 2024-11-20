import pandas as pd

# Function to clean tract IDs
def clean_tract(tract):
    if isinstance(tract, str) and 'US' in tract:
        return tract.split('US')[-1]
    return tract

# Read the first CSV file (division to tract)
division_df = pd.read_csv('division_to_tract.csv')
division_df['tract'] = division_df['tract'].astype(str)

# Read the second CSV file (Census data)
census_df = pd.read_csv('ACSST5Y2022.S1901-Data.csv')

# Clean the tract IDs in the census data
census_df['GEO_ID'] = census_df['GEO_ID'].apply(clean_tract)

ownership_df = pd.read_csv('ACSDP5Y2022.DP04-Data.csv')

ownership_df['GEO_ID'] = ownership_df['GEO_ID'].apply(clean_tract)


hhi_column = 'S1901_C02_012E'
ownership_column = 'DP04_0046PE'

# Merge the dataframes
merged_df = pd.merge(division_df, census_df[['GEO_ID', hhi_column]], left_on='tract', right_on='GEO_ID', how='left')
merged_df = pd.merge(merged_df, ownership_df[['GEO_ID', ownership_column]], left_on='tract', right_on='GEO_ID', how='left')
# Select and rename the required columns
result_df = merged_df[['division', 'tract', hhi_column, ownership_column]]
result_df = result_df.rename(columns={hhi_column: 'hhi', ownership_column: 'ownership'})

# Write to a new CSV file
result_df.to_csv('division_tract_hhi_ownership.csv', index=False)

print("New CSV file 'division_tract_hhi.csv' has been created.")