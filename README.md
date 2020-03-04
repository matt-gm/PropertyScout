# Property Scout  

###1-stop real estate record resource.
![PropertyScout_Screenshot.png](frontend/assets/PS_logo.png)

## Pipeline

![Matthew_Maatubang_Insight_Demo.png](frontend/assets/Matthew_Maatubang_Insight_Demo.png)   

- ETL real estate records from 6 different datasets (see Datasets below).  
- Storage of raw and aggregated data in AWS S3.   
- Aggregation and data access via AWS Athena.   
- Visualization via Dash.   

## Dashboard Features

- View LA County Real Estate Assessor data from 2006-2019.    
- Filter data by geography: City, Neighborhood (ZIP Code), and Street.     
![Geo Filter](frontend/assets/PropertyScout_Geographic_Filter.png)   
- Filter data by use type.   
![Use Filter](frontend/assets/PropertyScout_Use_Filter.png)  
- Filter data by record year.     
![Year Filter](frontend/assets/PropertyScout_Year_Filter.png)  
- Interactive time series, property count, and average improvement value charts.   
![Time Series](frontend/assets/PropertyScout_Time_Series.png)   
![Pie Chart](frontend/assets/PropertyScout_Pie_Chart.png)   
![Bar Chart](frontend/assets/PropertyScout_Bar_Chart.png)   

## Datasets
  
City | CSV API Endpoint |
--------------------|------------------|
Los Angeles | https://data.lacounty.gov/resource/9trm-uz8i.csv |
San Francisco | https://data.sfgov.org/resource/wv5m-vpq2.csv |
New York City | https://data.cityofnewyork.us/resource/yjxr-fw8i.csv |
Denver | https://data.colorado.gov/resource/msap-49q7.csv |
Austin | https://data.austintexas.gov/resource/8hvr-vyie.csv |
Las Vegas | https://opendata.arcgis.com/datasets/1a89b7b4de56414088c854c4f785e3e7_0.csv |

## Created by Matthew Maatubang
#### Insight Data Engineering Fellowship - Los Angeles 2020A
Platform | Username |
--------------------|------------------|
Github | @matt-gm |  
Personal | mmaatubang.com | 
LinkedIn | linkedin.com/in/mmaatubang/ |