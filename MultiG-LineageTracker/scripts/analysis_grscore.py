# -*- coding: utf-8 -*-
"""
Created on Mon May 13 12:29:35 2024

@author: Arnab
"""


# import required libraries

import pickle
import re

import itertools
import math

import os
import sys

import libsbml
import numpy as np
import pandas as pd
from scipy.stats import percentileofscore
import copy

from Bio import Phylo

from io import StringIO

from scipy.interpolate import interp1d
from scipy.stats import percentileofscore
from scipy.stats import gaussian_kde
import math
import seaborn as sns
import itertools
import plotly.figure_factory as ff
import plotly.io as pio


import matplotlib.pyplot as plt
import matplotlib as mpl

mpl.rcParams['figure.dpi'] = 300
mpl.rcParams['font.sans-serif'] = ['Arial']


#%%
cd = os.getcwd()
wd = os.path.dirname(cd)
sys.path.append(os.path.join(wd,'bin'))

sbml_file = "SPARCED.xml"


sbml_reader = libsbml.SBMLReader()
sbml_doc = sbml_reader.readSBML(os.path.join(wd,sbml_file))
sbml_model = sbml_doc.getModel()

species_all = [str(x.getId()) for x in list(sbml_model.getListOfSpecies())]





#%%
output_dir_main = os.path.join(wd,'output')

exp_title = 'in_silico_drs'
# output_main = os.path.join(wd,'output',exp_title)
output_main = os.path.join("E:\\",exp_title)


dir_doses_all = os.listdir(os.path.join(output_main,'drs_alpel','drs_alpel_rep1'))

doses_all = [float(x.split('_')[-1]) for x in dir_doses_all]

doses_all.sort()


#%%

# import class for reading dose response outputs

from modules.drsPlotting import drs_dict


#%% load datasets if they're already generated (run analysis_popdyn if drs_summary.pkl is missing)

with open(os.path.join(wd,'output','in_silico_drs_summary','drs_summary.pkl'),'rb') as f:
    drs_summary_full = pickle.load(f)


#%% prepare dataframes for calculating gr score



def gr_calc_row (drug,time_h,dl,rep,drs_summary_dict,cell_line='mcf10a_sim'):
    
    dose = doses_all[dl]
    
    dose_dict = drs_summary_dict[str(drug)]['d'+str(dl)]['r'+str(rep+1)]
    cellpop = dose_dict['cellpop']
    tout = dose_dict['tout']
 
    interpolator = interp1d(tout,cellpop)
    cell_count = interpolator(time_h*3600)
    cell_count_time0 = dose_dict['cellpop'][0]
    
    drugs_all = list(drs_summary_dict.keys())
 
    
    ctrl_pool = []
    
    for dr in drugs_all:
        for rp in range(1,len(drs_summary_dict[dr]['d0'].keys())+1):
            rp_dict = drs_summary_dict[dr]['d0']['r'+str(rp)]
            rp_cellpop = np.array(rp_dict['cellpop'])
            rp_tout = np.array(rp_dict['tout'])
            
            rp_interp = interp1d(rp_tout,rp_cellpop)
            rp_cellcount = float(rp_interp(time_h*3600))
            ctrl_pool.append(rp_cellcount)
            
    dose_pool = []
    
    for rp in range(1,len(drs_summary_dict[drug]['d'+str(dl)].keys())+1):
        rp_dose_dict = drs_summary_dict[drug]['d'+str(dl)]['r'+str(rp)]
        rp_dose_cellpop = np.array(rp_dose_dict['cellpop'])
        rp_dose_tout = np.array(rp_dose_dict['tout'])
        
        rp_dose_interp = interp1d(rp_dose_tout,rp_dose_cellpop)
        rp_dose_cellcount = float(rp_dose_interp(time_h*3600))
        dose_pool.append(rp_dose_cellcount)    
 
    cell_count_percentile = percentileofscore(dose_pool, cell_count)
    cell_count_ctrl = np.percentile(ctrl_pool,cell_count_percentile)


    new_row = {}
    new_row['cell_line'] = cell_line
    new_row['agent'] = str(drug)
    new_row['timepoint'] = time_h
    new_row['concentration'] = dose
    new_row['cell_count'] = cell_count
    new_row['cell_count__ctrl'] = cell_count_ctrl
    new_row['cell_count__time0'] = cell_count_time0 
    
    
    return new_row

#%%



time_h = [48,72]

drs_grcalc3 = pd.DataFrame(data=None,columns=['cell_line','agent','timepoint','concentration','cell_count','cell_count__ctrl','cell_count__time0'])



for drug in drs_summary_full.keys():
    for dl in range(1,len(drs_summary_full[str(drug)].keys())):
        for rep in range(len(drs_summary_full[str(drug)]['d'+str(dl)].keys())):
            for t in time_h:
                new_row = gr_calc_row(drug,t,dl,rep,drs_summary_full)
                drs_grcalc3 = drs_grcalc3.append(new_row, ignore_index=True)


drs_grcalc3.to_csv(os.path.join(wd,'output','in_silico_drs_summary','drs_grcalc3.tsv'),sep='\t',index=False)

