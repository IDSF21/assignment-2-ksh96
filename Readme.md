# US Air Pollution Analysis


## Goal

Taking a deep dive into the US Air Pollution Statistics for CO, SO2, NO2 and Ozone and understanding if pollutants have come down.


## Introduction
This project looks into very harmful pollutants like CO, SO2, NO2 and Ozone in the lower layers of the atmosphere. Generally, we know that the common pollutants like CO2 are increasing in the atmosphere. Due to different environmental movements that have brought attention to the pollutants mentioned above, I want to see if there has been any decrease in the pollutants that may show that we as a society are moving slowly but surely towards protecting the atmosphere.

### Dataset
The data set was downloaded from [Kaggle](https://www.kaggle.com/sogun3/uspollution). For the application to use the dataset, the downloaded file was cleaned is stored on Google Drive.

### Features
* A look at the Raw Data
* View metrics and AQI graphs for a selected state (from a drop down) over the years. The graphs can be scaled
* View graphs for a particular state of interest over time for selected pollutants. Here we can delve deeper into the values that contribute to the calculation of an AQI like the mean and max values of the pollutants
* View graphs for all the pollutants everyday for a year and state of your choice.
* Observe the AQI values of all the states on a Map with the colors as decided by the EPA


## Design Decisions
1. Use of line charts: To visualize the trends over time, the a subset of the data was resampled based on year and month to show different trends over time
2. Use of Choropleth Maps: The dataset contained information on a state level. I used this to visualize the Air Quality Index as calculated by the EPA and plot the colors of the air quality using the ranges and guidelines provided by the EPA
3. Use of scatterplots: To visualize the data on a daily level, the data was filtered based on state and was plotted on a scatter plot. There are multiple scatterplots, one for each parameter.


## Development 
It took about 30 hours for me to develop the application. I initially experimented with different datasets to figure out what I want to showcase. This was 20% of time. After deciding the dataset, I spent 60% of my time on EDA, to clean the data and sample the data for different conditions. I spent 20% of time to develop my application and tell a story. 