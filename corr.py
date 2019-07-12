# -*- coding: utf-8 -*-
"""

This module retrieves the correlation analysis of the paper 'Macroeconomic, 
social and environmental impacts of a circular economy to 2050: A meta analysis
of prospective studies'

The functions are:
    - main(): Loads data source and runs corr(data, year, title) function
    - corr(gdp, co2, job, year): Retrieves correlation analysis using Pearson
    Method. Inputs: gdp=dataset for GDP
    indicator as pandas dataframe; job=dataset for job creation
    indicator as pandas dataframe; co2=dataset for CO2 emissions
    indicator as pandas dataframe; year= specific year as 'int'
    
    - group(df, group_name, degree, title): Retrieves mean values and
    statistcal summary for a specific group region.
    Inputs: df=dataset for specific indicator as pandas dataframe;
    group_name= country/region group name as list; title= text as string

    - save(): Saves dataframes from main() in an Excel file

Created on Tue Mar 19 15:52:39 2019

Updated on Wed Jun 26 09:40:00 2019

@author: aguilarga
"""


import pandas as pd
from pandas import ExcelWriter
from datetime import datetime


# FUNCTIONS

def main():
    # SETTINGS
    data = pd.ExcelFile('data_source.xlsx')
    gdp = data.parse('gdp', sep='\t', index_col=[0], header=[0],
                     decimal=',')
    job = data.parse('job', sep='\t', index_col=[0], header=[0],
                     decimal=',')
    co2 = data.parse('co2', sep='\t', index_col=[0], header=[0],
                     decimal=',')
    # ANALYSIS FOR 2030
    year = 2030
    results = corr(gdp, co2, job, year)
    return results


def corr(gdp, co2, job, year):  # CORRELATION WITH STUDYS' MEAN
    # CALCULATING MEAN PER STUDIES
    def group(df, scen_name, year):
        df_ = df.loc[df['degree'] == scen_name]  # selecting scenario dataset
        df_ = df_.drop(['title', 'author', 'country', 'degree', 'scenario',
                        'csc', 'rwm', 'ple', 're', 'proxy', 'proxy_source'],
                       axis=1)   # deleting non-relevant columns
        cod = ['d01', 'd02', 'd03', 'd04', 'd05', 'd06', 'd07', 'd08',
               'd09', 'd10', 'd11', 'd12', 'd13', 'd14', 'd15', 'd16',
               'd17', 'd18', 'd19', 'd20', 'd21', 'd22', 'd23', 'd24',
               'd25', 'd26', 'd27']  # studies' code index
        emp = []
        for i in cod:
            res_ = df_[[i in s for s in df_.index]]
            res_ = res_.mean()
            emp.append(res_)
        res = pd.DataFrame(emp)  # mean of indicator per study, per year
        res.index = cod
        res = res.loc[:, [year]]
        return res
    # CREATING DATAFRAMES FOR CORRELATION ANALYSIS
    ga_ = group(gdp, 'amb', year)  # gdp(ambtious) average per study
    ja_ = group(job, 'amb', year)  # job(ambtious) average per study
    ca_ = group(co2, 'amb', year)  # co2(ambtious) average per study
    ta_ = pd.concat([ga_, ja_, ca_], axis=1)  # all(ambtious) average per study
    ta_.columns = ['gdp', 'job', 'co2']  # setting columns name
    gm_ = group(gdp, 'mod', year)  # gdp(moderate) average per study
    jm_ = group(job, 'mod', year)  # job(moderate) average per study
    cm_ = group(co2, 'mod', year)  # co2(moderate) average per study
    tm_ = pd.concat([gm_, jm_, cm_], axis=1)  # all(moderate) average per study
    tm_.columns = ['gdp', 'job', 'co2']  # setting columns name
    res = pd.concat([ta_, tm_], axis=0)  # merging ambitious and moderate
    # CORRELATION ANALYSIS
    print('Correlation matrix (Pearson method)')
    print(res.corr(method='pearson'))
    return res


def save():
    res = main()
    writer = ExcelWriter('results_corr' + '_' +
                         datetime.now().strftime('%Y%m%d') + ".xlsx")
    res.to_excel(writer, 'val')
    writer.save()
    return
