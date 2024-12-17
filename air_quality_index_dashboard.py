import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import seaborn as sns

aqi_df = pd.read_csv('aqi_dataset.csv')

with st.sidebar:
    st.caption('Built by Maya Sopiah Lubis :rose:')
    st.title('Brief Guideline of AQI :wind_blowing_face:')
    st.subheader('What is AQI?')
    st.markdown("""
            AQI is an abbreviation of Air Quality Index. AQI is a measurement indicator of the outdoor air quality. Air quality is defined by the content of air pollution. The higher AQI score, means the air quality is more concerning and more unhealthy. AQI has six categories, which describe the difference severity of air pollution.
            """)
    st.markdown("""
                - Good (0 to 50): Air quality is satisfactory, and air pollution poses little or no risk.
                - Moderate (51 to 100): Air quality is acceptable. However, there may be a risk for some people.
                - Unhealthy for Sensitive Groups (101 to 150): Members of sensitive groups may experience health effects.
                - Unhealthy (151 to 200): Some members of the general public may experience health effects.
                - Very Unhealthy (201 to 300): Health alert- the risk of health effects is increased for everyone.
                - Hazardous (301 and higher): Health warning of emergency conditions -  everyone is more likely to be affected.
                """)
    st.subheader('What is AQI components?')
    st.markdown("""
            - PM2.5: The particles in the air with a diameter less than 2.5 micrometers, which is the type of particles that can reach the bloodstream, then hurt lungs and heart. Related to gaseous pollutant.
            - PM10: A mixture of particles suspended in the air that do not exceed 10 micrograms in diameter. It is harmful because it contains benzopyrenes, furans, dioxins and in short, carcinogenic heavy metals.
            - SO2: Sulphur dioxide, which irritates the lining of the nose, throat and lungs and may worsen existing respiratory illness especially asthma.
            - NO2: Nitrogen dioxide is a respiratory irritant and has a variety of adverse health effects on the respiratory system.
            - CO: Carbon monoxide is a poisonous gas that you can't see, taste or smell.
            - O3: Ozone on ground level is the main component of smog and is the product of the interaction between sunlight and emissions from sources such as motor vehicles and industry.
            """)
    
    st.title('About this Project :flags:')
    st.markdown("""
                This project is based on the dataset of air pollutant in 12 cities in China from year 2013 to 2017. As one of emerging nation in the world nowadays, China has delevoped as one of most powerful country in industrialization. Unfortunately, as the side effect of it, air pollutant is increasing significantly which can be harmful to the citizen of China, especially in the big cities. This mini project tries to dig in the insight of the fluctuation of AQI of some cities and how harmful it can be in the daily life for its citizen.
                """)

#----------------------------------------------------------
# Dashboard title
st.title('China AQI Dashboard 	:chart_with_upwards_trend:')
#----------------------------------------------------------
# Dasboard Selectbox

# Prepare options for selectbox. The options consist of station names
cities = list(aqi_df['station'].unique())
cities.insert(0, 'All')

# Display selectbox and load the city names in it
city_selected = st.selectbox("Select preferred city/station name",
                             options = cities
)
city_name = city_selected

if city_name != 'All':
    df_city = aqi_df[aqi_df['station'] == city_name].copy()
    # Select 'date' column as the Dataframe index
    df_city['date'] = pd.to_datetime(df_city['date'])

#----------------------------------------------------------

first_col, sec_col, third_col = st.columns(3)

with first_col:
    if city_name != 'All':
        aqi_score_mean = df_city['AQI_value'].mean()
    else:
        aqi_score_mean = aqi_df['AQI_value'].mean()
    aqi_score_mean = round(aqi_score_mean, 0)
    st.metric(label="AQI Score Average", value=aqi_score_mean)

with sec_col:
    if city_name != 'All':
        aqi_score_max = df_city['AQI_value'].max()
    else:
        aqi_score_max = aqi_df['AQI_value'].max()
    st.metric(label="Highest AQI Score", value=aqi_score_max)

with third_col:
    if city_name != 'All':
        aqi_score_min = df_city['AQI_value'].min()
    else:
        aqi_score_min = aqi_df['AQI_value'].min()
    st.metric(label="Lowest AQI Score", value=aqi_score_min)

#----------------------------------------------------------
# 'AQI Score Fluctuation per Year' line plot part

if city_name != 'All':
    st.subheader(f'AQI Score Fluctuation per Year - {city_name} City')
    df_year = df_city.copy()

    # Select 'date' column as the Dataframe index
    df_year.set_index('date', inplace=True)

    # # Calculating average AQI per year for all stations
    df_anual = df_year['AQI_value'].resample('A').mean()
    df_anual = df_anual.reset_index()

    # Create a multi-line chart based on annual data
    fig, ax = plt.subplots(figsize=(40, 15), dpi=150)
    sns.set_style('whitegrid')
    sns.set_context("talk")
    sns.lineplot(x='date', y='AQI_value', data=df_anual, ax=ax)

    # Assigning and adjusting title, x label, y label, and legend
    ax.set_xlabel('Year', fontsize=30, labelpad=25)
    ax.set_ylabel('AQI Value', fontsize=30, labelpad=25)
    ax.tick_params(axis='both', which='major', labelsize=25)
else:
    st.subheader('AQI Score Fluctuation per Year')
    
    # Copy the df_aqi_daily to the new variable
    df_year = aqi_df.copy()

    # Select 'date' column as the Dataframe index
    df_year['date'] = pd.to_datetime(df_year['date'])
    df_year.set_index('date', inplace=True)

    # Calculating average AQI per year for all stations
    df_anual = df_year.groupby('station')['AQI_value'].resample('A').mean()
    df_anual = df_anual.reset_index()

    # Create a multi-line chart based on annual data
    fig, ax = plt.subplots(figsize=(40, 15), dpi=300)
    sns.set_style('whitegrid')
    sns.set_context("talk")
    sns.lineplot(x='date', y='AQI_value', hue='station', data=df_anual, ax=ax)

    # Assigning and adjusting title, x label, y label, and legend
    ax.set_xlabel('Year', fontsize=30, labelpad=25)
    ax.set_ylabel('AQI Value', fontsize=30, labelpad=25)
    ax.tick_params(axis='both', which='major', labelsize=25)
    legend = ax.legend(loc='center left', bbox_to_anchor=(1, 0.5), title='Station', fontsize=25, title_fontsize=30)

# Show the line plot
st.pyplot(fig)

#----------------------------------------------------------
# 'AQI Score Fluctuation per Month' line plot part


if city_name != 'All':
    st.subheader(f'AQI Score Fluctuation per Month - {city_name} City')
    
    df_month = df_city.copy()

    # Select 'date' column as the Dataframe index
    df_month.set_index('date', inplace=True)

    # Calculating average AQI per year for all stations
    df_monthly = df_month['AQI_value'].resample('M').mean()
    df_monthly = df_monthly.reset_index()

    # Create a multi-line chart based on monthly data
    fig, ax = plt.subplots(figsize=(40, 15), dpi=150)
    sns.set_style('whitegrid')
    sns.set_context("talk")
    sns.lineplot(x='date', y='AQI_value', data=df_monthly, ax=ax)

    # Assigning and adjusting title, x label, y label, and legend
    ax.set_xlabel('Month', fontsize=30, labelpad=25)
    ax.set_ylabel('AQI Value', fontsize=30, labelpad=25)
    ax.tick_params(axis='both', which='major', labelsize=25)
else:
    st.subheader('AQI Score Fluctuation per Month')
    
    # Copy the df_aqi_daily to the new variable
    df_month = aqi_df.copy()

    # Select 'date' column as the Dataframe index
    df_month['date'] = pd.to_datetime(df_month['date'])
    df_month.set_index('date', inplace=True)

    # Calculating average AQI per year for all stations
    df_monthly = df_month.groupby('station')['AQI_value'].resample('M').mean()
    df_monthly = df_monthly.reset_index()

    # Create a multi-line chart based on monthly data
    fig, ax = plt.subplots(figsize=(40, 15), dpi=300)
    sns.set_style('whitegrid')
    sns.set_context("talk")
    sns.lineplot(x='date', y='AQI_value', hue='station', data=df_monthly, ax=ax)

    # Assigning and adjusting title, x label, y label, and legend
    ax.set_xlabel('Month', fontsize=30, labelpad=25)
    ax.set_ylabel('AQI Value', fontsize=30, labelpad=25)
    ax.tick_params(axis='both', which='major', labelsize=25)
    legend = ax.legend(loc='center left', bbox_to_anchor=(1, 0.5), title='Station', fontsize=25, title_fontsize=30)

# Show the line plot
st.pyplot(fig)

#----------------------------------------------------------
# 'AQI Score Fluctuation per Day' line plot part

if city_name != 'All':
    st.subheader(f'AQI Score Fluctuation per Day - {city_name} City')
    
    # Create a multi-line chart based on daily data
    fig, ax = plt.subplots(figsize=(100, 30), dpi=150)
    sns.set_style('whitegrid')
    sns.set_context("talk")
    sns.lineplot(x='date', y='AQI_value', data=df_city, ax=ax)

    # Assigning and adjusting title, x label, y label, and legend
    ax.set_xlabel('Date', fontsize=70, labelpad=50)
    ax.set_ylabel('AQI Value', fontsize=70, labelpad=50)
    ax.tick_params(axis='x', which='major', labelsize=50, rotation=45)
    ax.tick_params(axis='y', which='major', labelsize=50)
    ax.xaxis.set_major_locator(mdates.MonthLocator(interval=3))  # Set interval to 3 months
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))  # Format the date as Year-Month
else:
    st.subheader('AQI Score Fluctuation per Day')
    
    # Copy the df_aqi_daily to the new variable
    df_daily = aqi_df.copy()

    # Select 'date' column as the Dataframe index
    df_daily['date'] = pd.to_datetime(df_daily['date'])

    # Create a multi-line chart based on daily data
    fig, ax = plt.subplots(figsize=(100, 30), dpi=300)
    sns.set_style('whitegrid')
    sns.set_context("talk")
    sns.lineplot(x='date', y='AQI_value', hue='station', data=df_daily, ax=ax)

    # Assigning and adjusting title, x label, y label, and legend
    ax.set_xlabel('Date', fontsize=70, labelpad=50)
    ax.set_ylabel('AQI Value', fontsize=70, labelpad=50)
    ax.tick_params(axis='both', which='major', labelsize=50)
    legend = ax.legend(loc='center left', bbox_to_anchor=(1, 0.5), title='Station', fontsize=50, title_fontsize=70)

    ax.xaxis.set_major_locator(mdates.MonthLocator(interval=3))  # Set interval to 6 months
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))  # Format the date to show Year-Month

st.pyplot(fig)

#----------------------------------------------------------
# 'AQI Status Occurences' bar plot part

if city_name != 'All':
    st.subheader(f'AQI Status Occurences - {city_name} City')
    
    # Filter data from dataset
    aqi_label_occurences = pd.DataFrame(df_city['AQI_label'].value_counts()).reset_index()
    aqi_label_occurences.rename(columns={'index': 'AQI_label', 'AQI_label':'amount'}, inplace=True)
    
    # Create bar plot
    plt.figure(figsize=(30, 10), dpi=150)
    sns.set_style('whitegrid')
    ax = sns.barplot(data=aqi_label_occurences, x='AQI_label', y='amount')
    ax.set_xlabel('AQI Label', fontsize=30, labelpad=30)
    ax.set_ylabel('Occurences Amount', fontsize=30, labelpad=30)
    ax.tick_params(axis='both', which='major', labelsize=20)
    ax.bar_label(ax.containers[0], fontsize=20, color='blue')
else:
    st.subheader('AQI Status Occurences')
    
    aqi_status_df = pd.DataFrame(aqi_df.groupby('AQI_label', as_index=False).size())
    aqi_status_df = aqi_status_df.sort_values(by='size', ascending=False).reset_index()
    aqi_status_df = aqi_status_df.drop('index', axis=1)
    aqi_status_df.rename(columns={'size': 'occurences_amount'}, inplace=True)

    plt.figure(figsize=(30, 10), dpi=150)
    sns.set_style('whitegrid')
    ax = sns.barplot(data=aqi_status_df, x=aqi_status_df['AQI_label'], y=aqi_status_df['occurences_amount'], color='C0')
    ax.set_xlabel('AQI Label', fontsize=30, labelpad=30)
    ax.set_ylabel('Occurences Amount', fontsize=30, labelpad=30)
    ax.tick_params(axis='both', which='major', labelsize=20)
    ax.bar_label(ax.containers[0], fontsize=20, color='blue')

st.pyplot(plt)
#----------------------------------------------------------
# 'Bad Air Quality Occurences Each Year' bar plot part

if city_name != 'All':
    st.subheader(f'Bad Air Quality Occurences Each Year - {city_name} City')
    
    # Filter data from dataset
    bad_aqi = df_city.groupby(['year', 'AQI_label'], as_index=False).size()
    bad_aqi = bad_aqi[(bad_aqi['AQI_label'] != 'Good') & (bad_aqi['AQI_label'] != 'Moderate')]
    bad_aqi = pd.DataFrame(bad_aqi.groupby('year', as_index=False)['size'].sum()).reset_index()
    bad_aqi = bad_aqi.drop('index', axis=1)
    bad_aqi.rename(columns={'size': 'occurences_amount'}, inplace=True)
    
    # Create bar plot
    plt.figure(figsize=(30, 10), dpi=150)
    sns.set_style('whitegrid')
    ax = sns.barplot(data=bad_aqi, x='year', y='occurences_amount')
    ax.set_xlabel('Year', fontsize=30, labelpad=30)
    ax.set_ylabel('Occurences Amount', fontsize=30, labelpad=30)
    ax.tick_params(axis='both', which='major', labelsize=20)
    ax.bar_label(ax.containers[0], fontsize=20, color='blue')
else:
    st.subheader('Bad Air Quality Occurences Each Year')
    bad_aqi_df = aqi_df.groupby(['year', 'AQI_label'], as_index=False).size()
    bad_aqi_df = bad_aqi_df[(bad_aqi_df['AQI_label'] != 'Good') & (bad_aqi_df['AQI_label'] != 'Moderate')]
    bad_aqi_df = pd.DataFrame(bad_aqi_df.groupby('year', as_index=False)['size'].sum())
    bad_aqi_df = bad_aqi_df.sort_values(by='size', ascending=False).reset_index()
    bad_aqi_df = bad_aqi_df.drop('index', axis=1)
    bad_aqi_df.rename(columns={'size': 'occurences_amount'}, inplace=True)

    plt.figure(figsize=(30, 10), dpi=150)
    sns.set_style('whitegrid')
    ax = sns.barplot(data=bad_aqi_df, x=bad_aqi_df['year'], y=bad_aqi_df['occurences_amount'], color='C0')
    ax.set_xlabel('Year', fontsize=30, labelpad=30)
    ax.set_ylabel('Occurences Amount', fontsize=30, labelpad=30)
    ax.tick_params(axis='both', which='major', labelsize=20)
    ax.bar_label(ax.containers[0], fontsize=20, color='blue')
    
st.pyplot(plt)

#----------------------------------------------------------
# 'Air Pollutant Percentages of AQI' pie chart part

if city_name != 'All':
    st.subheader(f'Air Pollutant Percentages of AQI - {city_name} City')
    pollutants = pd.DataFrame(df_city['highest_pollutant'].value_counts()).reset_index()
    pollutants.rename(columns={'index': 'pollutant', 'highest_pollutant':'amount'}, inplace=True)
else:
    st.subheader('Air Pollutant Percentages of AQI')
    pollutants = pd.DataFrame(aqi_df['highest_pollutant'].value_counts()).reset_index()
    pollutants.rename(columns={'index': 'pollutant', 'highest_pollutant':'amount'}, inplace=True)

pollutants = pollutants[pollutants['pollutant'] != 'SO2']

fig, ax = plt.subplots(figsize=(10, 10), dpi=100)
pollutant_length = len(list(pollutants['pollutant'].unique()))
if pollutant_length == 6:
    explode = (0.1, 0, 0, 0, 0.1, 0.1)
elif pollutant_length == 5:
    explode = (0.1, 0, 0, 0.1, 0.1)
else:
    explode = (0.1, 0, 0.1, 0.1)

# Create pie chart in 'ax' object
wedges, texts, autotexts = ax.pie(
    pollutants['amount'],
    textprops={'fontsize':15},
    autopct='%1.1f%%',
    startangle = 45,
    explode = explode
)

ax.axis('equal')
# Add legend
ax.legend(
    wedges,  # Pass the wedge objects (slices of the pie chart)
    pollutants['pollutant'],  # Use the pollutant names for labels
    title="Pollutants",  # Add a title for the legend
    loc="center left",  # Position the legend
    bbox_to_anchor=(1, 0, 0.5, 1),  # Place the legend outside the plot
    fontsize=15  # Set font size
)
st.pyplot(plt)