# -*- coding: utf-8 -*-

"""


This module retrieves the boxplots from the paper 'Macroeconomic, social and
environmental impacts of a circular economy to 2050: A meta analysis
of prospective studies'

The functions are:
    - main(): Loads data source and runs boxplot(data, year, title) function

    - boxplot(data, year, title): Retrieves boxplot graphs from the statistical
    analysis. Inputs: data=dataset for specific
    indicator as pandas dataframe; year= specific year as 'int';
    title= text as string

    - group(df, group_name, degree, title): Retrieves mean values and
    statistcal summary for a specific group region.
    Inputs: df=dataset for specific indicator as pandas dataframe;
    group_name= country/region group name as list; title= text as string


Created on Mon Mar 18 15:24:47 2019

Updated on Wed Jun 26 09:40:00 2019

@author: aguilarga
"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.lines as mlines
import matplotlib.patches as mpatches
import seaborn as sns


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

    # ANALYSIS PER INDICATOR FOR 2030
    year = 2030
    ga, gas, gm, gms = res(gdp, year, 'gdp')
    ja, jas, jm, jms = res(job, year, 'job')
    ca, cas, cm, cms = res(co2, year, 'co2')
    boxplot(ga, gm, ja, jm, ca, cm, year)
    return


def res(data, year, title):  # BOXPLOT FROM MEANS VALUES
    # SETTINGS
    df_ = data.loc[:, ['country', 'degree', year]]
    def group(df, degree):
        df_ = df.loc[df['degree'] == degree]
        cod = ['d01', 'd02', 'd03', 'd04', 'd05', 'd06', 'd07', 'd08',
               'd09', 'd10', 'd11', 'd12', 'd13', 'd14', 'd15', 'd16',
               'd17', 'd18', 'd19', 'd20', 'd21', 'd22', 'd23', 'd24',
               'd25', 'd26', 'd27']  # studies' code index
        df_ = df_.drop(['country', 'degree'],
                       axis=1)   # deleting non-relevant columns
        emp = []
        for i in cod:
            res_ = df_[[i in s for s in df_.index]]
            res_ = res_.mean()
            emp.append(res_)
        res = pd.DataFrame(emp)  # mean of indicator per study, per year
        res.index = cod
        res_sum = res.describe(include=[np.number])
        res_sum.columns = [title + '_' + degree + ' (n=' +
                           str(res_sum.loc['count', :].sum().round(0)) +
                           ')']
        res.columns = ['val']
        res['label'] = [title + '_' + degree + ' (n=' +
                        str(res_sum.loc['count', :].sum().round(0)) +
                        ')']*len(res)
        return res, res_sum

    # ANALYSIS
    ta, tas = group(df_, 'amb')
    tm, tms = group(df_, 'mod')
    return ta, tas, tm, tms


def boxplot(ga, gm, ja, jm, ca, cm, year):
    # BOXPLOT
    bp = pd.concat([ga, gm, ja, jm, ca, cm])
    plt.figure()
    fig = sns.set_style("whitegrid")
    fig = sns.boxplot(x='val', y='label', data=bp,
                      medianprops=dict(linestyle='-', linewidth=2,
                                       color='black'),
                      width=0.25) 
    # CUSTUMIZING BOXPLOT
    # CUSTUMIZING BOXPLOT
    acol = 'green'
    mcol = 'blue'
    alpha = 0.3
    fs= 12
    gab = fig.artists[0]
    gmb = fig.artists[1]
    jab = fig.artists[2]
    jmb = fig.artists[3]
    cab = fig.artists[4]
    cmb = fig.artists[5]
    gab.set_facecolor(acol)  # changing color scenario
    gmb.set_facecolor(mcol)  # changing color scenario
    jab.set_facecolor(acol)  # changing color scenario
    jmb.set_facecolor(mcol)  # changing color scenario
    cab.set_facecolor(acol)  # changing color scenario
    cmb.set_facecolor(mcol)  # changing color scenario
    fig.axes.set_title('Boxplot of scenarios per indicator for ' +
              str(year))
    fig.set_xlabel('Change in %', fontsize=fs)
    fig.set_ylabel('', fontsize=fs)
    mpatch = mpatches.Patch(color=mcol, label='moderate scenarios', alpha=alpha)
    apatch = mpatches.Patch(color=acol, label='ambitious scenarios', alpha=alpha)
    mdn = mlines.Line2D([], [], linestyle='-', linewidth=2, color='black',
                        label='median')
    out = mlines.Line2D([], [], linestyle='None', marker='d', color='black',
                        label='outliers')
    plt.legend(handles=[mpatch, apatch, mdn, out], loc='center left',
               fontsize=fs-2, bbox_to_anchor=(1, 0.5), frameon=True)
    for patch in fig.artists:
        r, g, b, a = patch.get_facecolor()
        patch.set_facecolor((r, g, b, alpha))
    return
