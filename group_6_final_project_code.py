# -*- coding: utf-8 -*-

import pandas as pd
import os
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.dates as mdates

# Get the current working directory and print it
current_directory = os.getcwd()
print("Current Working Directory:", current_directory)

#Temp and Precip Data
##Travis County

###Precipitation
travis_precip = 'travis_precipitation_monthly.csv'

df_travis_precip = pd.read_csv(travis_precip)

print(df_travis_precip)

###Temperature

travis_temp = 'travis_mean_temperature_monthly.csv'

df_travis_temp = pd.read_csv(travis_temp)

print(df_travis_temp)

##Harris County

###Precipitation
harris_precip = 'harris_precipitation_monthly.csv'

df_harris_precip = pd.read_csv(harris_precip)

print(df_harris_precip)

###Temperature

harris_temp = 'harris_mean_temperature_monthly.csv'

df_harris_temp = pd.read_csv(harris_temp)

print(df_harris_temp)

##Hidalgo County

###Precipitation
hidalgo_precip = 'hidalgo_precipitation_monthly.csv'

df_hidalgo_precip = pd.read_csv(hidalgo_precip)

print(df_hidalgo_precip)

###Temperature
hidalgo_temp = 'hidalgo_mean_temperature_monthly.csv'

df_hidalgo_temp = pd.read_csv(hidalgo_temp)

print(df_hidalgo_temp)

##El Paso County

###Precipitation
el_paso_precip = 'el paso_precipitation_monthly.csv'

df_el_paso_precip = pd.read_csv(el_paso_precip)

print(df_el_paso_precip)

###Temperature
el_paso_temp = 'el paso_mean_temperature_monthly.csv'

df_el_paso_temp = pd.read_csv(el_paso_temp)

print(df_el_paso_temp)

##Dallas County

###Precipitation
dallas_precip = 'dallas_precipitation_monthly.csv'

df_dallas_precip = pd.read_csv(dallas_precip)

print(df_dallas_precip)
###Temperature

dallas_temp = 'dallas_mean_temperature_monthly.csv'

df_dallas_temp = pd.read_csv(dallas_temp)

print(df_dallas_temp)

#Join into one large dataframe
precip_df=pd.concat([df_travis_precip,df_harris_precip,df_hidalgo_precip,df_el_paso_precip,df_dallas_precip])
print(precip_df)

##Temp
temp_df=pd.concat([df_travis_temp,df_harris_temp,df_hidalgo_temp,df_el_paso_temp,df_dallas_temp])
print(temp_df)

##Add temp column to precip df
precip_df['mean_temperature_monthly_degf'] = temp_df['mean_temperature_monthly_degf']

#Rename precip df
all_df=precip_df

##testing all df
print(all_df)

#Defined function to allow for multiple county data
def plot_temp_precip(county):

    county_df=all_df[all_df['county']==county].copy()
    temp_df = county_df['mean_temperature_monthly_degf']
    precip_df = county_df['precipitation_monthly_inches']
    #Turning date into datetime format for use

    county_df['period'] = pd.to_datetime(county_df['period'])
    #Separating the Period into months and years

    county_df['year_month'] = county_df['period'].dt.to_period('M')
    # Convert 'year_month' Period columns to datetime (using the first day of each month)
    county_df['year_month_dt'] = county_df['year_month'].dt.to_timestamp()
    #Create subplot
    fig, axes = plt.subplots(1, 2, figsize=(15, 6))

    #Storing Slopes and creating graph based on data
    slopes = {'precipitation': None, 'temperature': None}

    #Precipitation plot
    x_precip = county_df['year_month_dt']  # Use datetime object for x-axis
    y_precip = precip_df
    axes[0].scatter(x_precip, y_precip, color='blue', label=f'{county} Precipitation Data')
    trendline_pre = np.polyfit(range(len(x_precip)), y_precip, 1)
    p_precip = np.poly1d(trendline_pre)
    axes[0].plot(x_precip, p_precip(range(len(x_precip))), color='red', linestyle='--', label='Precipitation Trendline')
    axes[0].plot(county_df['year_month_dt'],y_precip,color='blue',linestyle='-',linewidth=1)

    #Slopes stored for precipitation multiplied by 12 to result in by year differences
    slopes['precipitation'] = trendline_pre[0]*12

    #Set x-axis ticks every 5 years for precipitation plot
    years_range_precip = pd.date_range(start=x_precip.min(), end=x_precip.max(), freq='5Y')
    axes[0].set_xticks(years_range_precip)
    # Format the x-axis ticks as YYYY-MM
    axes[0].xaxis.set_major_formatter(mdates.DateFormatter('%Y'))

    axes[0].set_title(f'{county} Precipitation (Monthly)', fontsize=12)
    axes[0].set_xlabel('Period (Year-Month)', fontsize=10)
    axes[0].set_ylabel('Precipitation (Inches)', fontsize=10)
    axes[0].legend()

    #Temperature plot
    x_temp = county_df['year_month_dt']
    y_temp = temp_df

    axes[1].scatter(x_temp, y_temp, color='orange', label=f'{county} Temperature Data')
    trendline_temp = np.polyfit(range(len(x_temp)), y_temp, 1)
    p_temp = np.poly1d(trendline_temp)
    axes[1].plot(x_temp, p_temp(range(len(x_temp))), color='green', linestyle='--', label='Temperature Trendline')
    axes[1].plot(county_df['year_month_dt'],y_temp,color='orange',linestyle='-',linewidth=1)
    #Slopes stored for temperature multiplied by 12 to result in by year differences
    slopes['temperature'] = trendline_temp[0]*12

    #Set x-ticks every 5 years for temp plot
    years_range_temp = pd.date_range(start=x_temp.min(), end=x_temp.max(), freq='5Y')
    axes[1].set_xticks(years_range_temp)

    #Format the x-axis ticks as YYYY-MM
    axes[1].xaxis.set_major_formatter(mdates.DateFormatter('%Y'))

    axes[1].set_title(f'{county} Temperature (Monthly)', fontsize=12)
    axes[1].set_xlabel('Period (Year-Month)', fontsize=10)
    axes[1].set_ylabel('Temperature (F)', fontsize=10)
    axes[1].legend()

    #Make the layout tight
    plt.tight_layout(pad=2)

    #Add an overall title to the figure
    plt.suptitle(f'{county} - Precipitation and Temperature Trends', fontsize=14)

    #Show final plot
    plt.show()

    #Show average rate of change per month and year
    print('Precipitation - Temperature average changes for a one year period')
    print(slopes)
    totaltemp = (slopes['temperature']*24)
    totalprecip = (slopes['precipitation']*24)
    print(f'Average temperature change for the 24 year period: {totaltemp} degrees')
    print(f'Average precipitation change for the 24 year period: {totalprecip} inches')



plot_temp_precip('Travis')
plot_temp_precip('Harris')
plot_temp_precip('Hidalgo')
plot_temp_precip('El_Paso')
plot_temp_precip('Dallas')

####### PART 2: DROUGHT MONITOR CODE ########

#CSV's and Dataframes

##Travis County
travis_drought = 'travis_drought_monitor.csv'
travis_drought_df = pd.read_csv(travis_drought)
print(travis_drought_df)

##Harris County
harris_drought = 'harris_drought_monitor.csv'
harris_drought_df = pd.read_csv(harris_drought)
print(harris_drought_df)

##Hidalgo County
hidalgo_drought = 'hidalgo_drought_monitor.csv'
hidalgo_drought_df = pd.read_csv(hidalgo_drought)
print(hidalgo_drought_df)

##El Paso County
el_paso_drought = 'el paso_drought_monitor.csv'
el_paso_drought_df = pd.read_csv(el_paso_drought)
print(el_paso_drought_df)

##Dallas County
dallas_drought = 'dallas_drought_monitor.csv'
dallas_drought_df = pd.read_csv(dallas_drought)
print(dallas_drought_df)

#Make One Inclusive Dataframe
drought_df=pd.concat([travis_drought_df, harris_drought_df, hidalgo_drought_df,
                      el_paso_drought_df, dallas_drought_df])
print(drought_df)

#Function to plot each county with category frequencies and calculate slope of trendline
def plot_drought_categories(drought_df, county_name):
    drought_columns = ['None', 'D0', 'D1', 'D2', 'D3', 'D4']

    #Change period to datetime and add year column
    drought_df['period'] = pd.to_datetime(drought_df['period'])
    drought_df['year'] = drought_df['period'].dt.year

    #Create figure with subplots for each drought category
    fig, axes = plt.subplots(2, 3, figsize=(10, 6))
    axes = axes.flatten()

    #Store slopes
    slopes = {}

    # For loop over each drought category and create a separate subplot for it
    for idx, drought_category in enumerate(drought_columns):

        #Frequency of drought condition each year
        drought_frequencies_by_year = drought_df.groupby('year')[drought_category].apply(lambda x: (x > 0).sum())
        #x and y values
        x_values = list(drought_frequencies_by_year.index)
        y_values = drought_frequencies_by_year.values

        #Plot the histogram for drought category
        axes[idx].bar(x_values, y_values, label=drought_category, color='blue', width=0.6)

        #Add trendline
        trendline = np.polyfit(x_values, y_values, 1)
        p = np.poly1d(trendline)
        axes[idx].plot(x_values, p(x_values), color='red', linestyle='--', alpha=0.6, label=f'{drought_category} Trendline')

        #Calculate the slope of trendline
        slope = trendline[0]
        slopes[drought_category] = slope

        #Customize subplots
        axes[idx].set_xlabel('Year', fontsize=8)
        axes[idx].set_ylabel('Frequency', fontsize=8)
        axes[idx].set_title(f'{drought_category}', fontsize=9)

        axes[idx].legend(fontsize=8)

        #Rotate x-axis labels
        axes[idx].tick_params(axis='x', rotation=45)

    #Adjust plot layout/readability
    plt.tight_layout(pad=1.5)
    plt.subplots_adjust(top=0.85, bottom=0.12)
    plt.suptitle(f'{county_name} - Drought Conditions (2000-2024)', fontsize=12, y=0.95)
    plt.show()

    #Print the slopes
    print(f"Slope of Trendline (Rate of Change per Year) for {county_name} (2000-2024):")
    for category, slope in slopes.items():
        print(f"{category}: {slope:.2f} units per year")


#Plot each county
plot_drought_categories(travis_drought_df, 'Travis County')
plot_drought_categories(harris_drought_df, 'Harris County')
plot_drought_categories(hidalgo_drought_df, 'Hidalgo County')
plot_drought_categories(el_paso_drought_df, 'El Paso County')
plot_drought_categories(dallas_drought_df, 'Dallas County')