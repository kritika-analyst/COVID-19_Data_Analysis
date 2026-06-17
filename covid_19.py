# Project - COVID_19 Data Analysis and Visualization
# Author - Kritika
# Tools: Python, Pandas, Matplotlib, Seaborn

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Loading Dataset
df = pd.read_csv("covid_19_clean_complete.csv")
print(df.head(5))  # to check first 5 rows of the dataset
print(df.info())   # to check the datatypes and missing values

# Data Cleaning
print("\nMissing values by column: ")
print(df.isnull().sum())

df.drop_duplicates(inplace=True)   # removes duplicate rows and saves it permanently in dataframe

df["Date"] = pd.to_datetime(df["Date"])  # converts the Date column to datetime format

# Data Analysis
print("\nShape of dataset: ",df.shape)   # gives the no. of rows and columns in the dataset 

print("\nStatistical Summary: ",df.describe())   # gives statistical summary of numerical columns

print("\nColumns names : ",df.columns.tolist())  # gives the names of all the columns in the dataset

# KPI Summary / Data Visualization
total_confirmed = df["Confirmed"].sum()
total_deaths = df["Deaths"].sum()
total_recovered = df["Recovered"].sum()

print("Total Confirmed Cases: ", total_confirmed)
print("Total Deaths: ",total_deaths)
print("Total Recovered Cases: ",total_recovered)


# Top 10 Countries with highest confirmed cases
top_countries  = ( df.groupby("Country/Region")["Confirmed"]   # group by country and sum the confirmed cases
                .sum()
                .sort_values(ascending=False)         # sort the values in descending order
                .head(10)
               )

figure= plt.figure(figsize=(10,6))
sns.set_style("whitegrid")
plt.grid(linestyle='--', alpha=0.7)

sns.barplot(
    x = top_countries.values,     # gives the total confirmed cases 
    y = top_countries.index,      # gives country names
    palette= "viridis"            # sets the color palette for the bars
) 

from matplotlib.ticker import FuncFormatter
plt.gca().xaxis.set_major_formatter(
    FuncFormatter(lambda x, p: f"{x/1e6:.0f}M")    
)

for i, value in enumerate(top_countries.values):
    plt.text(
        value,
        i,
        f" {value/1e6:.0f}M",
        va="center"
    )

plt.title("Top 10 countries with highest confirmed cases",
          fontsize= 16,
          fontweight= "bold",
          pad= 20
          )
plt.xlabel("Total Confirmed Cases")
plt.ylabel("Country")
plt.savefig("covid-19_top_10_countries.png")

plt.show()


# Death vs Recovery Analysis
death_recovery= df[["Deaths", "Recovered"]].sum()

plt.figure(figsize=(12,8))

plt.pie(
    death_recovery,                        # gives total death and recovered cases
    labels= death_recovery.index,          # gives labels for the pie chart
    autopct= "%1.1f%%",                    # gives the percentage of each slice
    startangle= 90,                        # rotates the pie chart to start from 90 degrees
    wedgeprops= {"width": 0.5,             # sets width of the pie slices
                 "edgecolor" : "white",    # sets edge color of the pie slices
                 "linewidth":2             # sets the edge line width of the pie slices
                },
    colors= ["red", "green"],              # sets the colors of the pie slices
    textprops= {"color": "black",          # sets the color of the text in the pie slices
                "fontsize": 16             # sets the font size of the text in the pie slices
                }
)

plt.text(
    0,0,                       # sets the position of the text in the center of the pie chart
    "COVID-19\nOutcomes",      # sets the text to be displayed in the center of the pie chart
    ha= "center",              # sets the horizontal alignment of the text to center
    va= "center",              # sets the vertical alignment of the text to center
    fontsize= 14,              # sets the font size
    fontweight= "bold"         # sets the font weight to bold
)

plt.title("COVID-19 Global Outcomes: Recovery vs Death Distribution", fontsize= 18, fontweight= "bold")
plt.savefig("Covid-19_death_recovery")
plt.show()


# Correlation Heatmap
plt.figure(figsize=(12,8))

sns.heatmap(
        df[["Confirmed", "Deaths" , "Recovered"]].corr(),   # calculates the correlation between the columns
        annot= True,                                        # shows the correlation value inside each box
        fmt= ".2f",                                         # format the numbers
        cmap= "viridis",                                    # choose the color scheme
        linewidth= 1,                                       # border thickness between boxes
        linecolor= "white",                                 # color of the borders
        square= True,                                       # makes each heatmap box a perfect square
        cbar_kws= {"label": "Correlation"}                  # adds a title to the color scale
)

plt.title(
    "Correlation Between COVID-19 Metrics",     # gives title to the heatmap
    fontsize= 16,                               # sets font size of the title
    fontweight= "bold",                         # sets font weight to bold 
    pad =20                                     # leaves 20 units between title and the heatmap
)

plt.tight_layout()
plt.savefig("covid-19_metrics")
plt.show()


# Daily Trend Analysis
import matplotlib.ticker as ticker      # modules used for formatting axis numbers
daily_cases= df.groupby("Date")["Confirmed"].sum()     

plt.figure(figsize=(12,8))

plt.plot(
    daily_cases.index,     # x-axis values
    daily_cases.values,    # y-axis values
    color= "royalblue",     # adds color
    linewidth= 2.5,        # thickness of the line
    marker= "o",           # put a circle on every data point
    markersize= 4          # size of each circle
)

plt.title(
    "Global Confirmed COVID-19 Cases Over Time",   # title name  
    fontsize= 16,                                  # font size of the title is 16
    fontweight= "bold",                            # font weight is bold
    pad= 20                                        # 20 units between graph and title 
)

plt.xlabel("Date", fontsize= 12)               # label of x-axis and sets font size
plt.ylabel("Confirmed Cases", fontsize= 12)    # label of y-axis and sets font size

plt.xticks(rotation= 45)    # rotates the x-axis labels by 45 degrees

plt.grid(alpha=0.3)         # adds light grid lines to the graph

plt.gca().yaxis.set_major_formatter(         # gca= get current axes ,access the y-axis
    ticker.StrMethodFormatter("{x:,.0f}")     # change how numbers appear on the y-axis and show zero decimal places
)

plt.tight_layout()
plt.savefig("covid-19_trend_analysis")
plt.show()


print("COVID-19 Analysis Successfully Completed !")