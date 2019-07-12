# meta_analysis_supplementary_material

## data_source
It contains the data from the selected publications in 7 spreedsheets as:
* data_source: Selected publications with detailed information about: source, model caracteristic, intervention type, macro-indicators,                  geographical and temporal dimension, and method/data transparency
* gdp: Range of projections for GDP scenarios per study
* job: Range of projections for job creation scenarios per study
* co2: Range of projections for CO2 emissions scenarios per study
* figure_1: A flowchart  of the inclusion of selected publications, and specific queries used in the systematic review
* table_1: Overview of models used by the selected 28 publications


## time_ser.py
Phyton script retrieves the time series of changes in GDP, job creation ,and CO2 emissions respect to BAU scenarios from 2020 to 2050, per scenario category. This module contains:
* ***main()***: Loads data source and runs ***scenario(data, title)*** function
* ***scenario(data, title)***: Retrieves  graphs and dataframes for the time series of scenarios per study. Inputs: data=dataset for specific indicator as pandas dataframe; title= text as string)
* ***mean(df, scen_type)***: Retrieves mean values and statistcal summary for a specific scenario type. Inputs: df=dataset for specific indicator as pandas dataframe; scen_type= 'amb' or 'mod' as string
* save(): Saves dataframes from ***main()*** in an Excel file

## boxplot.py
Phyton script retrieves the boxplot of changes in GDP, job creation ,and CO2 emissions respect to BAU, per year and scenario category. This module contains:
* ****main()***: Loads data source and runs ***boxplot(data, year, title)*** function
* ****boxplot(data, year, title)***: Retrieves boxplot graphs from the statistical analysis. Inputs: data=dataset for specific indicator as pandas dataframe; year= specific year as integer; title= text as string
* ***group(df, group_name, degree, title)***: Retrieves mean values and statistcal summary for a specific group region. Inputs: df=dataset for specific indicator as pandas dataframe; group_name= country/region group name as list; title= text as string

## corr.py
Phyton script retrieves the correlation analysis of changes in GDP, job creation ,and CO2 emissions respect to BAU per year using Pearson Method. This module contains:
* ***main()***: Loads data source and runs ***corr(data, year, title)*** function
* ***corr(gdp, co2, job, year)***: Retrieves correlation analysis using Pearson Method. Inputs: gdp=dataset for GDP indicator as pandas dataframe; job=dataset for job creation indicator as pandas dataframe; co2=dataset for CO2 emissions indicator as pandas dataframe; year= specific year as integer
 * ***group(df, group_name, degree, title)***: Retrieves mean values and statistcal summary for a specific group region. Inputs: df=dataset for specific indicator as pandas dataframe; group_name= country/region group name as list; title= text as string
* ***save()***: Saves dataframes from ***main()*** in an Excel file

## results_time_ser.xlsx
Excel file with the summary of results from ***time_ser.py***

## results_corr.xlsx
Excel file with the summary of results from ***corr.py***
