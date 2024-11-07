#!/usr/bin/env python
# coding: utf-8

# # Summary of Analysis
# 
# 
# ## Data Preparation
# - Extracted `transaction_date`, `transaction_time`, `transaction_year`, and `transaction_month` from the `transaction_date_and_time` column.
# - Masked the Aadhaar number to only show the last four digits.
# 
# ## Yearly Analysis
# - Number of transactions each year.
# - Number of unique ration card IDs each year.
# - Yearly usage of each ration card.
# - Number of times portability is marked as 'Yes' each year.
# - Visualizations for yearly analysis.
# 
# ## Monthly Analysis
# - Number of transactions each month.
# - Number of unique ration card IDs each month.
# - Monthly usage of each ration card.
# - Number of times portability is marked as 'Yes' each month.
# - Visualizations for monthly analysis.
# 
# ## Daily Analysis
# - Number of transactions each day.
# - Number of unique ration card IDs each day.
# - Daily usage of each ration card.
# - Number of times portability is marked as 'Yes' each day.
# 
# 
# ## Time Slot Analysis
# - Transactions per day, month, and year in 2-hour time slots.
# - Identification of the time slot with the highest transactions.
# - Detection of abnormalities where transactions are unusually high in certain time periods.
# - Calculation of the average time between transactions.
# - Identification of fast transactions (less than 1 minute apart) and whether they occur during abnormal high transaction periods.
# 
# ## Member Name Analysis
# - Number of different names appearing in the Member Name column for each ration card.
# - Sorting ration cards by the number of unique member names and listing those names.
# - Identification of members collecting ration for more than one ration card.
# 
# ## Commodity Analysis
# - Total amount of wheat, rice, sugar, K.Oil, and other commodities purchased each month.
# - Visualization of monthly totals for each commodity.
# 
# ## Card Type Analysis
# - Types of cards used and the number of transactions done using them each month.

# In[2]:


# get_ipython().system('pip install pandas pandasgui plotly')


# In[3]:


import warnings
warnings.filterwarnings('ignore')


# ## Data Preparation
# - Extracted `transaction_date`, `transaction_time`, `transaction_year`, and `transaction_month` from the `transaction_date_and_time` column.
# - Masked the Aadhaar number to only show the last four digits.

# In[5]:


import pandas as pd
from pandasgui import show
# Load the CSV file
file_path = r'2824-shop.csv'
df = pd.read_csv(file_path)

# Convert 'transaction_date_and_time' to datetime
df['transaction_date_and_time'] = pd.to_datetime(df['Trans Date time'])

# Extract transaction_date, transaction_time, transaction_year, transaction_month
df['transaction_date'] = df['transaction_date_and_time'].dt.date
df['transaction_time'] = df['transaction_date_and_time'].dt.time
df['transaction_year'] = df['transaction_date_and_time'].dt.year
df['transaction_month'] = df['transaction_date_and_time'].dt.to_period('M').astype(str)
# Ensure the 'transaction_day' column is created


# Mask Aadhaar number
df['Aadhaar No'] = df['Aadhaar No'].apply(lambda x: str(x)[-4:] if pd.notnull(x) else x)

# Save processed data
df.to_csv('Processed-Data.csv', index=False)


# ## Yearly Analysis
# - Number of transactions each year.
# - Number of unique ration card IDs each year.
# - Yearly usage of each ration card.
# - Number of times portability is marked as 'Yes' each year.
# - Visualizations for yearly analysis.

# In[6]:


import plotly.express as px
from pandasgui import show
# Number of transactions each year
transactions_per_year = df['transaction_year'].value_counts().sort_index()
transactions_per_year.index = transactions_per_year.index.astype(str)  # Convert index to string
fig1 = px.bar(transactions_per_year, labels={'index': 'Year', 'value': 'Number of Transactions'})
# fig1.show()

# Number of unique ration card IDs each year
unique_rationcards_per_year = df.groupby('transaction_year')['Ration Card No.'].nunique()
unique_rationcards_per_year = unique_rationcards_per_year.index.astype(str)
fig2 = px.bar(unique_rationcards_per_year, labels={'index': 'Year', 'value': 'Number of Unique Ration Cards'})
# fig2.show()

# Yearly usage of each ration card
rationcard_usage_per_year = df.groupby(['transaction_year', 'Ration Card No.']).size().unstack(fill_value=0).transpose()
# show(rationcard_usage_per_year)

# Number of times portability is marked as 'Yes' each year
portability_yes_per_year = df[df['Portability Transaction'] == 'Yes'].groupby('transaction_year').size()
portability_yes_per_year.index = portability_yes_per_year.index.astype(str)  # Convert index to string
fig4 = px.bar(
    portability_yes_per_year,
    labels={'index': 'Year', 'value': 'Count of Portability "Yes"'},    
)
# fig4.show()


# ## Monthly Analysis
# - Number of transactions each month.
# - Number of unique ration card IDs each month.
# - Monthly usage of each ration card.
# - Number of times portability is marked as 'Yes' each month.
# - Visualizations for monthly analysis.
# 

# In[7]:


# Number of transactions each month
transactions_per_month = df['transaction_month'].value_counts().sort_index()
fig6 = px.bar(transactions_per_month, title='Number of Transactions Each Month', labels={'index': 'Month', 'value': 'Number of Transactions'})
# fig6.show()

# Number of unique ration card IDs each month
unique_rationcards_per_month = df.groupby('transaction_month')['Ration Card No.'].nunique()
fig7 = px.bar(unique_rationcards_per_month, title='Number of Unique Ration Cards Each Month', labels={'index': 'Month', 'value': 'Number of Unique Ration Cards'})
# fig7.show()


# Monthly usage of each ration card
rationcard_usage_per_month = df.groupby(['transaction_month', 'Ration Card No.']).size().unstack(fill_value=0).transpose()
fig8 = px.imshow(rationcard_usage_per_month, title='Monthly Ration Card Usage')
# fig8.show()
# show(rationcard_usage_per_month)

# Number of times portability is marked as 'Yes' each month
portability_yes_per_month = df[df['Portability Transaction'] == 'Yes'].groupby('transaction_month').size()
fig9 = px.bar(portability_yes_per_month, title='Number of Times Portability is Yes Each Month', labels={'index': 'Month', 'value': 'Count'})
# fig9.show()
# show(portability_yes_per_month)



# ## Monthly analysis of unused ration card

# In[8]:


import pandas as pd

def analyze_ration_card_usage_with_details(df):
    # Ensure transaction_date is in datetime format
    df['transaction_date'] = pd.to_datetime(df['transaction_date'])

    # Extract year and month from transaction_date
    df['year_month'] = df['transaction_date'].dt.to_period('M')

    # Group by ration card number and month, and count the transactions
    usage_counts = df.groupby(['Ration Card No.', 'year_month']).size().reset_index(name='transaction_count')

    # Pivot to have ration cards as rows and months as columns, filling missing values with 0
    usage_pivot = usage_counts.pivot(index='Ration Card No.', columns='year_month', values='transaction_count').fillna(0)

    # Get the list of all ration card numbers and names
    ration_card_info = df[['Ration Card No.', 'Card Holder Name']].drop_duplicates()

    # Find ration cards and names not used in particular months
    unused_info = []
    for card in usage_pivot.index:
        zero_months = usage_pivot.loc[card][usage_pivot.loc[card] == 0].index.tolist()
        card_holder_name = ration_card_info[ration_card_info['Ration Card No.'] == card]['Card Holder Name'].values[0]
        if zero_months:
            unused_info.append({
                'Ration Card No.': card,
                'Card Holder Name': card_holder_name,
                'Unused Months': zero_months
            })

    return usage_pivot, unused_info



# Analyze the ration card usage with details
usage_pivot, unused_info = analyze_ration_card_usage_with_details(df)


# show(unused_info)


# ## Daily Analysis
# - Number of transactions each day.
# - Number of unique ration card IDs each day.
# - Daily usage of each ration card.
# - Number of times portability is marked as 'Yes' each day.
# 
# 

# In[9]:


# Number of transactions each day
transactions_per_day = df['transaction_date'].value_counts().sort_index()
fig11 = px.bar(transactions_per_day, title='Number of Transactions Each Day', labels={'index': 'Day', 'value': 'Number of Transactions'})
# fig11.show()

# Number of unique ration card IDs each day
unique_rationcards_per_day = df.groupby('transaction_date')['Ration Card No.'].nunique()
fig12 = px.bar(unique_rationcards_per_day, title='Number of Unique Ration Cards Each Day', labels={'index': 'Day', 'value': 'Number of Unique Ration Cards'})
# fig12.show()

# Daily usage of each ration card
rationcard_usage_per_day = df.groupby(['transaction_date', 'Ration Card No.']).size().unstack(fill_value=0).transpose()
fig13 = px.imshow(rationcard_usage_per_day, title='Daily Ration Card Usage')
# fig13.show()

# Number of times portability is marked as 'Yes' each day
portability_yes_per_day = df[df['Portability Transaction'] == 'Yes'].groupby('transaction_date').size()
fig14 = px.bar(portability_yes_per_day, title='Number of Times Portability is Yes Each Day', labels={'index': 'Day', 'value': 'Count'})
# fig14.show()



# ## Analysis of Transactions on Specific Dates
# The following analysis identifies and summarizes transactions that occur on specific dates across multiple months.
# 

# In[10]:


import pandas as pd
import plotly.express as px

# Ensure the 'transaction_day' column is created
df['transaction_day'] = pd.to_datetime(df['transaction_date']).dt.day

# Identify all unique days of the month present in the dataset
unique_days = df['transaction_day'].unique()

# Create a dictionary to store analysis results for each day
analysis_results = {}

# Function to analyze trends for a specific day
def analyze_trends_for_day(day):
    # Filter transactions for the specific day
    transactions_on_day = df[df['transaction_day'] == day]
    
    # Count the number of ration card numbers that appear more than once on this day
    ration_card_counts = transactions_on_day['Ration Card No.'].value_counts()
    repeated_ration_cards = ration_card_counts[ration_card_counts > 1]
    
    if len(repeated_ration_cards) == 0:
        return None  # No repeated transactions for this day
    
    # Get detailed information for these ration card numbers
    repeated_transactions_details = transactions_on_day[transactions_on_day['Ration Card No.'].isin(repeated_ration_cards.index)]
    
    # Group by Ration Card No and aggregate the months, years, and portability transactions
    detailed_repeated_transactions = repeated_transactions_details.groupby('Ration Card No.').agg({
        'Card Holder Name': 'first',
        'transaction_month': lambda x: ', '.join(sorted(x.unique())),
        'transaction_year': lambda x: ', '.join(sorted(x.astype(str).unique())),
        'transaction_date': 'count',
        'Portability Transaction': lambda x: ', '.join(x.unique())
    }).reset_index()
    
    # Rename columns for clarity
    detailed_repeated_transactions.columns = ['Ration Card No.', 'Card Holder Name', 'Months', 'Years', 'Total Transactions', 'Portability Transactions']
    
    return detailed_repeated_transactions
    # show(detailed_repeated_transactions)
# Analyze trends for each unique day
for day in unique_days:
    result = analyze_trends_for_day(day)
    if result is not None:
        analysis_results[day] = result

# Combine results into a single DataFrame
combined_results = pd.concat(analysis_results.values(), keys=analysis_results.keys()).reset_index(level=0).rename(columns={'level_0': 'Day'})

# Aggregate total repeated transactions per day
total_repeated_transactions_per_day = combined_results.groupby('Day')['Total Transactions'].sum().reset_index()

# Sort by total transactions and get the top 5 days
top_5_days = total_repeated_transactions_per_day.sort_values(by='Total Transactions', ascending=False).head(5)

# Plot the top 5 days using Plotly
fig = px.bar(top_5_days, x='Day', y='Total Transactions', title='Top 5 Dates with Highest Repeated Transactions',
             labels={'Day': 'Day of the Month', 'Total Transactions': 'Total Repeated Transactions'})

# fig.show()


# ## Highest Transaction Day Trend
# The following analysis identifies the day with the highest number of total transactions across all months and analyzes the transaction trends for that day.
# 

# In[11]:


# Filter transactions that are done on the 20th of each month
transactions_on_20th = df[df['transaction_day'] == 20]

# Count the number of ration card numbers that appear more than once on the 20th of each month
ration_card_counts = transactions_on_20th['Ration Card No.'].value_counts()
repeated_ration_cards = ration_card_counts[ration_card_counts > 1]

# Filter the detailed transactions for these repeated ration cards
repeated_transactions_details = transactions_on_20th[transactions_on_20th['Ration Card No.'].isin(repeated_ration_cards.index)]

# Group by Ration Card No and aggregate the months, years, and portability transactions
detailed_repeated_transactions = repeated_transactions_details.groupby('Ration Card No.').agg({
    'Card Holder Name': 'first',
    'transaction_month': lambda x: ', '.join(sorted(x.unique())),
    'transaction_year': lambda x: ', '.join(sorted(x.astype(str).unique())),
    'transaction_date': 'count',
    'Portability Transaction': lambda x: ', '.join(x.unique())
}).reset_index()

# Rename columns for clarity
detailed_repeated_transactions.columns = ['Ration Card No.', 'Card Holder Name', 'Months', 'Years', 'Total Transactions', 'Portability Transactions']

# Display the detailed repeated transactions
# show(detailed_repeated_transactions)




# ## Time Slot Analysis
# - Transactions per day, month, and year in 2-hour time slots.
# - Identification of the time slot with the highest transactions.
# - Detection of abnormalities where transactions are unusually high in certain time periods.
# - Calculation of the average time between transactions.
# - Identification of fast transactions (less than 1 minute apart) and whether they occur during abnormal high transaction periods.

# In[12]:


# Define 2-hour time slots
time_slots_2hr = [
    ('00:00:00', '02:00:00'),
    ('02:00:01', '04:00:00'),
    ('04:00:01', '06:00:00'),
    ('06:00:01', '08:00:00'),
    ('08:00:01', '10:00:00'),
    ('10:00:01', '12:00:00'),
    ('12:00:01', '14:00:00'),
    ('14:00:01', '16:00:00'),
    ('16:00:01', '18:00:00'),
    ('18:00:01', '20:00:00'),
    ('20:00:01', '22:00:00'),
    ('22:00:01', '23:59:59')
]

# Function to determine the 2-hour time slot for a given time
def get_time_slot_2hr(time):
    for start, end in time_slots_2hr:
        if start <= time <= end:
            return f"{start} - {end}"
    return 'Unknown'

# Apply the function to create a new column 'time_slot_2hr'
df['time_slot_2hr'] = df['transaction_time'].apply(lambda x: get_time_slot_2hr(str(x)))

# Daily time slot analysis
transactions_per_day_slot_2hr = df.groupby(['transaction_date', 'time_slot_2hr']).size().unstack(fill_value=0)
fig16 = px.imshow(transactions_per_day_slot_2hr.T, title='Transactions Per Day Slot (2hr)')
# fig16.show()

# Monthly time slot analysis
transactions_per_month_slot_2hr = df.groupby(['transaction_month', 'time_slot_2hr']).size().unstack(fill_value=0)
fig17 = px.imshow(transactions_per_month_slot_2hr.T, title='Transactions Per Month Slot (2hr)')
# fig17.show()

# Yearly time slot analysis
transactions_per_year_slot_2hr = df.groupby(['transaction_year', 'time_slot_2hr']).size().unstack(fill_value=0)
fig18 = px.imshow(transactions_per_year_slot_2hr.T, title='Transactions Per Year Slot (2hr)')
# fig18.show()

# Identify time slot with highest transactions
highest_transactions_time_slot = transactions_per_day_slot_2hr.sum().idxmax()
print(f"The time slot with the highest transactions is: {highest_transactions_time_slot}")

# Calculate average time between transactions
df['transaction_datetime'] = pd.to_datetime(df['transaction_date'].astype(str) + ' ' + df['transaction_time'].astype(str))
df = df.sort_values(by='transaction_datetime')
df['time_diff'] = df['transaction_datetime'].diff()
average_time_diff = df['time_diff'].mean()
print(f"The average time between transactions is: {average_time_diff}")

# Identify fast transactions (less than 1 minute apart)
fast_transactions = df[df['time_diff'] < pd.Timedelta(minutes=1)]

# Detecting abnormal high transaction periods
time_slot_stats = transactions_per_day_slot_2hr.describe().transpose()
abnormal_thresholds = time_slot_stats['mean'] + 2 * time_slot_stats['std']
abnormal_days = transactions_per_day_slot_2hr > abnormal_thresholds
abnormal_days_filtered = transactions_per_day_slot_2hr[abnormal_days]
abnormal_days_filtered = abnormal_days_filtered.dropna(how='all')

# Identify fast transactions within abnormal high transaction periods
fast_transactions_abnormal = fast_transactions[fast_transactions['transaction_date'].isin(abnormal_days_filtered.index)]

# Display fast transactions within abnormal high transaction periods
import pandasgui
from pandasgui import show

# show(fast_transactions_abnormal)

# Additional graphs for abnormal days
# Total transactions on each abnormal day
abnormal_day_transactions = df[df['transaction_date'].isin(abnormal_days_filtered.index)]
total_transactions_abnormal_days = abnormal_day_transactions['transaction_date'].value_counts().sort_index()
fig19 = px.bar(total_transactions_abnormal_days, title='Total Transactions on Each Abnormal Day', labels={'index': 'Date', 'value': 'Number of Transactions'})
# fig19.show()

# Unique transactions on each abnormal day
unique_transactions_abnormal_days = abnormal_day_transactions.groupby('transaction_date')['Ration Card No.'].nunique()
fig20 = px.bar(unique_transactions_abnormal_days, title='Unique Transactions on Each Abnormal Day', labels={'index': 'Date', 'value': 'Number of Unique Transactions'})
# fig20.show()

# Time slot distribution on abnormal days
abnormal_day_time_slot_distribution = abnormal_day_transactions.groupby(['transaction_date', 'time_slot_2hr']).size().unstack(fill_value=0).transpose()
fig21 = px.imshow(abnormal_day_time_slot_distribution, title='Time Slot Distribution on Abnormal Days')
# fig21.show()



# ## Member Name Analysis
# - Number of different names appearing in the Member Name column for each ration card.
# - Sorting ration cards by the number of unique member names and listing those names.
# - Identification of members collecting ration for more than one ration card.

# In[13]:


# Number of different names appearing in the Member Name column for each ration card
unique_member_names_per_card = df.groupby('Ration Card No.')['Member Name'].nunique().sort_values(ascending=False)
unique_member_names_details = df.groupby('Ration Card No.')['Member Name'].apply(lambda x: list(set(x))).loc[unique_member_names_per_card.index]

# Create dataframe for display
unique_member_names_df = pd.DataFrame({
    'Number of Unique Member Names': unique_member_names_per_card,
    'Member Names': unique_member_names_details
})

# show(unique_member_names_df)

# Identify members collecting ration for more than one ration card
members_multiple_ration_cards = df.groupby('Member Name')['Ration Card No.'].nunique()
members_multiple_ration_cards = members_multiple_ration_cards[members_multiple_ration_cards > 1]

# Extract relevant details: ration card number, card holder name, and all member names in the next column
members_multiple_ration_cards_details = df[df['Member Name'].isin(members_multiple_ration_cards.index)]
details_grouped = members_multiple_ration_cards_details.groupby('Ration Card No.').agg({
    'Card Holder Name': 'first',
    'Member Name': lambda x: ', '.join(set(x))
}).reset_index()

# show(details_grouped)


# ## Commodity Analysis
# - Total amount of wheat, rice, sugar, K.Oil, and other commodities purchased each month.
# - Visualization of monthly totals for each commodity.

# In[14]:


# Calculate the total amount of wheat, rice, sugar, K.Oil, and other commodities purchased each month
monthly_totals = df.groupby('transaction_month').agg({
    'Wheat (kg)': 'sum',
    'Rice (kg)': 'sum',
    'Sugar (kg)': 'sum',
    'K.Oil (ltr)': 'sum',
    'Other Comm. (kg)': 'sum'
})

# Plotting the total amount of each commodity purchased each month
fig19 = px.bar(monthly_totals, title='Total Commodities Purchased Each Month')
# fig19.show()


# 
# 
# ## Card Type Analysis
# - Types of cards used and the number of transactions done using them each month.

# In[15]:


# Calculate the number of transactions for each card type per month
transactions_per_card_type_per_month = df.groupby(['Card Type', 'transaction_month']).size().unstack(fill_value=0)

# Plotting the number of transactions for each card type per month
fig20 = px.imshow(transactions_per_card_type_per_month.T, title='Transactions Per Card Type Per Month')
# fig20.show()

# Export the DataFrame and figures
__all__ = ['df', 'fig1', 'fig2', 'rationcard_usage_per_year', 'fig4']