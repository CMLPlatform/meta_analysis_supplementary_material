# -*- coding: utf-8 -*-
"""

This module retrieves the time series from the paper 'Macroeconomic, social and
environmental impacts of a circular economy to 2050: A meta analysis
of prospective studies'

The functions are:
    - main(): Loads data source and runs scenario(data, title) function

    - scenario(data, title): Retrieves  graphs and dataframes for the
    time series of scenarios per study. Inputs: data=dataset for specific
    indicator as pandas dataframe; title= text as string)

    - mean(df, scen_type): retrieves mean values and statistcal summary for
    a specific scenario type. Inputs: df=dataset for specific
    indicator as pandas dataframe; scen_type= 'amb' or 'mod' as string

    - save(): Saves dataframes from main() in an Excel file


Created on Mon Mar 18 09:16:12 2019

Updated on Wed Jun 26 09:40:00 2019

@author: aguilarga
"""


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.lines as mlines
import matplotlib.patches as mpatches
from pandas import ExcelWriter
from datetime import datetime


# FUNCTIONS

def main():
    # LOAD DATA
    data = pd.ExcelFile('data_source.xlsx')
    gdp = data.parse('gdp', sep='\t', index_col=[0], header=[0],
                     decimal=',')
    job = data.parse('job', sep='\t', index_col=[0], header=[0],
                     decimal=',')
    co2 = data.parse('co2', sep='\t', index_col=[0], header=[0],
                     decimal=',')
    # ANALYSIS OF TIME SERIES PER INDICATOR TYPE
    ga, gas, gm, gms = scenario(gdp, 'GDP')
    ja, jas, jm, jms = scenario(job, 'job creation')
    ca, cas, cm, cms = scenario(co2, 'CO2 emissions')
    return ga, gas, gm, gms, ja, jas, jm, jms, ca, cas, cm, cms


def scenario(data, title):
    def mean(df, scen_type):
        df_ = df.loc[df['degree'] == scen_type]  # selecting scenario dataset
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
        res_sum = res.describe(include=[np.number])  # stats analysis summary
        return res, res_sum

    # DATA ANALYSIS
    amb, amb_sum = mean(data, 'amb')  # ambitious scenarios dataframes
    mod, mod_sum = mean(data, 'mod')  # moderate scenarios dataframes
    # TIME SERIES PLOT
    plt.figure()
    plt.style.use('seaborn-whitegrid')
    year = np.arange(2020, 2051)
    year = year.tolist()
    # AMBITIOUS SCENARIOS PLOT
    acol = 'green'
    amb.loc['year'] = np.arange(2020, 2051)  # adding year column
    amb_ = amb.T
    amb_ = amb_.loc[year, :]
    for column in amb_.drop('year', axis=1):
        plt.plot(amb_['year'], amb_[column], marker='o', color=acol,
                 linestyle='None', label=column)  # plotting each study
    asum_ = amb_sum.loc[['min', '50%', 'max']]  # selecting median and IQR
    asum_.loc['year'] = np.arange(2020, 2051)  # adding year column
    asum_ = asum_.T
    asum_ = asum_.loc[year, :]
    plt.plot(asum_['year'], asum_['min'], color=acol,
             alpha=0.1, label=['min'])  # plotting Q1 or 25%
    plt.plot(asum_['year'], asum_['max'], color=acol,
             alpha=0.1, label=['max'])  # plotting Q3 or 75%
    plt.fill_between(x='year', y1='min', y2='max', data=asum_,
                     color=acol, alpha=0.25)  # filling IQR
    plt.plot(asum_['year'], asum_['50%'], color='dark'+acol, linestyle='--',
             linewidth=2, label=['median'])  # plotting median
    # MODERATE SCENARIOS PLOT
    mcol = 'blue'
    mod.loc['year'] = np.arange(2020, 2051)  # adding year column
    mod_ = mod.T
    mod_ = mod_.loc[year, :]
    for column in mod_.drop('year', axis=1):
        plt.plot(mod_['year'], mod_[column], marker='X', color=mcol,
                 linestyle='None', label=column)  # plotting each study
    msum_ = mod_sum.loc[['min', '50%', 'max']]  # selecting median and IQR
    msum_.loc['year'] = np.arange(2020, 2051)  # adding year column
    msum_ = msum_.T
    msum_ = msum_.loc[year, :]
    plt.plot(msum_['year'], msum_['min'], color=mcol,
             alpha=0.1, label=['min'])  # plotting Q1 or 25%
    plt.plot(msum_['year'], msum_['max'], color=mcol,
             alpha=0.1, label=['max'])  # plotting Q3 or 75%
    plt.fill_between(x='year', y1='min', y2='max', data=msum_,
                     color=mcol, alpha=0.25)  # filling IQR
    plt.plot(msum_['year'], msum_['50%'], color='dark'+mcol, linestyle='--',
             linewidth=2, label=['median'])  # plotting median
    # SETTING LEGEND
    mdot = mlines.Line2D([], [], color=mcol, marker='X', linestyle='None',
                         label='Moderate scenario')
    adot = mlines.Line2D([], [], color=acol, marker='o', linestyle='None',
                         label='Ambitious scenario')
    mline = mlines.Line2D([], [], color='dark'+mcol, linestyle='--',
                          label='Median (moderate)')
    aline = mlines.Line2D([], [], color='dark'+acol, linestyle='--',
                          label='Median (ambitious)')
    mpatch = mpatches.Patch(color=mcol, alpha=0.25,
                            label='Range (moderate)')
    apatch = mpatches.Patch(color=acol, alpha=0.25,
                            label='Range (ambitious)')
    plt.legend(handles=[mdot, adot, mline, aline, mpatch, apatch],
               loc='center left', bbox_to_anchor=(1, 0.5),
               frameon=True, fontsize=14)
    # SETTING TITLE
    plt.ticklabel_format(useOffset=False)
    plt.xticks(year)
    plt.xlabel('Year', fontsize=16)
    plt.ylabel('Change in % ', fontsize=16)
    plt.title('Range of projections for ' + title + ' scenarios')
    plt.show()
    return amb, amb_sum, mod, mod_sum


def save():
    ga, gas, gm, gms, ja, jas, jm, jms, ca, cas, cm, cms = main()
    writer = ExcelWriter('results_time_ser' + '_' +
                         datetime.now().strftime('%Y%m%d') + ".xlsx")
    ga.to_excel(writer, 'gdp_a')
    gas.to_excel(writer, 'gdp_a_sum')
    gm.to_excel(writer, 'gdp_m')
    gms.to_excel(writer, 'gdp_m_sum')
    ja.to_excel(writer, 'job_a')
    jas.to_excel(writer, 'job_a_sum')
    jm.to_excel(writer, 'job_m')
    jms.to_excel(writer, 'job_m_sum')
    ca.to_excel(writer, 'co2_a')
    cas.to_excel(writer, 'co2_a_sum')
    cm.to_excel(writer, 'co2_m')
    cms.to_excel(writer, 'co2_m_sum')
    writer.save()
    return
