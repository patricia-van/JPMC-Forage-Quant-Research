import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from dateutil.relativedelta import relativedelta

df = pd.read_csv('Nat_Gas.csv')
df['Dates'] = pd.to_datetime(df['Dates'], format='%m/%d/%y')
df.head()

# Plot prices again date
# Observed upwards trend & yearly seasonality
# plt.plot(df['Dates'], df['Prices'])
# plt.xlabel('Date')
# plt.ylabel('Price')
# plt.title('Natural Gas Prices')
# plt.tick_params(axis='x', rotation=45)
# plt.show()

# Express the x-axis as the number of days from the start_date
start_date = min(df['Dates'])
duration = df['Dates'] - start_date
duration = duration.apply(lambda x: x.days)

# Fit trend using linear regression
mean_price, mean_duration = df['Prices'].mean(), duration.mean()
slope = np.sum((duration - mean_duration) * (df['Prices'] - mean_price)) / np.sum((duration - mean_duration)**2)
intercept = mean_price - (slope * mean_duration)

fitted_trend = [(slope * t) + intercept for t in duration]

# Plot fitted trend against actual trend and prices 
# plt.plot(df['Dates'], df['Prices'])
# plt.plot(df['Dates'], df['Prices'].rolling(12).mean())
# plt.plot(df['Dates'], fitted_trend)
# plt.xlabel('Date')
# plt.ylabel('Price')
# plt.title('Natural Gas Prices (Trend)')
# plt.tick_params(axis='x', rotation=45)

# Plot seasonality
# plt.plot(df['Dates'], df['Prices'] - df['Prices'].rolling(12).mean())
# plt.xlabel('Date')
# plt.ylabel('Price')
# plt.title('Natural Gas Prices (Seasonality)')
# plt.tick_params(axis='x', rotation=45)

# Compute seasonality index for each month
seasonality = df['Prices'] - df['Prices'].rolling(12).mean()
seasonality_df = pd.DataFrame({'Dates': df['Dates'], 'Seasonality': seasonality})
seasonality_df['Month'] = [x.month for x in seasonality_df['Dates']]
seasonality_df.dropna(inplace=True)

seasonality_idx = seasonality_df.groupby('Month')['Seasonality'].mean()

# Forecast price for the next on year
end_date = max(df['Dates'])
forecast_dates = []
for i in range(1, 13):
    forecast_dates.append(end_date + relativedelta(months=i))

forecast_duration = [(d - start_date).days for d in forecast_dates]
forecast_trend = [(slope * t) + intercept for t in forecast_duration]
forecast_seasonality = [seasonality_idx[d.month] for d in forecast_dates]
forecast_price = [forecast_trend[i] + forecast_seasonality[i] for i in range(len(forecast_dates))]

# Insert latest historical date & price for plotting purposes 
forecast_dates.insert(0, end_date)
forecast_price.insert(0, df[df['Dates'] == end_date]['Prices'].values[0])

# Plot historical and forecasted price
# plt.plot(df['Dates'], df['Prices'])
# plt.plot(forecast_dates, forecast_price)
# plt.show()

# Define function to get price
def get_price(date):
    date = pd.to_datetime(date, format='%m/%d/%y')
    if date in df['Dates'].values:
        return df[df['Dates'] == date]['Prices'].values[0]
    else:
        t = (date - start_date).days
        price = (slope * t) + intercept + seasonality_idx[date.month]
        return round(price, 2)

if __name__ == "__main__":
    date_input = input("Enter a date (MM/DD/YY): ")
    price = get_price(date_input)
    print(f"The price on {date_input} is: {price}")


