# Environment Setup
# Required libraries
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px  # For interactive visualizations

# 3. Data Loading & Initial Exploration

# Load the dataset
df = pd.read_csv('owid-covid-data.csv')

# Initial exploration
print(df.info())
print(df.describe())
print(df.isnull().sum())

# Display key columns
key_columns = ['date', 'location', 'total_cases', 'new_cases', 'total_deaths', 
               'new_deaths', 'total_vaccinations', 'people_vaccinated', 
               'people_fully_vaccinated', 'population']
print(df[key_columns].head())

# 4. Data Cleaning

# Convert date to datetime
df['date'] = pd.to_datetime(df['date'])

# Select countries of interest
countries = ['United States', 'India', 'Brazil', 'United Kingdom', 'Kenya', 'South Africa']
df = df[df['location'].isin(countries)]

# Handle missing values
numeric_cols = ['total_cases', 'new_cases', 'total_deaths', 'new_deaths', 
                'total_vaccinations', 'people_vaccinated', 'people_fully_vaccinated']
df[numeric_cols] = df[numeric_cols].fillna(0)

# Calculate derived metrics
df['death_rate'] = df['total_deaths'] / df['total_cases']
df['vaccination_rate'] = df['people_vaccinated'] / df['population']

# 5. Time Series Analysis
# Plot total cases over time
plt.figure(figsize=(12, 6))
for country in countries:
    country_data = df[df['location'] == country]
    plt.plot(country_data['date'], country_data['total_cases'], label=country)
plt.title('Total COVID-19 Cases Over Time')
plt.xlabel('Date')
plt.ylabel('Total Cases')
plt.legend()
plt.grid()
plt.show()

# Plot new cases (7-day rolling average)
plt.figure(figsize=(12, 6))
for country in countries:
    country_data = df[df['location'] == country]
    plt.plot(country_data['date'], 
             country_data['new_cases'].rolling(7).mean(), 
             label=country)
plt.title('Daily New COVID-19 Cases (7-day Average)')
plt.xlabel('Date')
plt.ylabel('New Cases')
plt.legend()
plt.grid()
plt.show()

# 6. Vaccination Analysis
# Plot vaccination progress
plt.figure(figsize=(12, 6))
for country in countries:
    country_data = df[df['location'] == country]
    plt.plot(country_data['date'], 
             country_data['people_fully_vaccinated']/country_data['population']*100, 
             label=country)
plt.title('Percentage of Population Fully Vaccinated')
plt.xlabel('Date')
plt.ylabel('% Population Fully Vaccinated')
plt.legend()
plt.grid()
plt.show()
# Comparative Analysis

# Latest data for each country
latest = df.sort_values('date').groupby('location').tail(1)

# Bar plot of total cases
plt.figure(figsize=(10, 6))
sns.barplot(x='location', y='total_cases', data=latest)
plt.title('Total COVID-19 Cases by Country')
plt.xticks(rotation=45)
plt.show()

# Bar plot of death rates
plt.figure(figsize=(10, 6))
sns.barplot(x='location', y='death_rate', data=latest)
plt.title('COVID-19 Death Rates by Country')
plt.xticks(rotation=45)
plt.show()

# 8. Advanced Visualization (Choropleth Map)

# Get worldwide latest data
world_df = pd.read_csv('owid-covid-data.csv')
world_df['date'] = pd.to_datetime(world_df['date'])
latest_world = world_df.sort_values('date').groupby('location').tail(1)

# Create choropleth map
fig = px.choropleth(latest_world, 
                    locations="iso_code",
                    color="total_cases_per_million",
                    hover_name="location",
                    color_continuous_scale=px.colors.sequential.Plasma,
                    title="Total COVID-19 Cases per Million People")
fig.show()
