# -*- coding: utf-8 -*-
"""
Created on Mon May 13 12:13:41 2024

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


#

#%% dose response population dynamics



def drs_summarize(drug,dose_lvl,output_dir=output_main): # measures alive cell count from each simulation
    
    drs_dose = {}
    for rep in range(10):
        print('now running...'+str(drug)+'...'+str(dose_lvl)+'...'+str(rep+1))
        drs_dict0 = drs_dict(output_dir,drug,rep+1,dose_lvl)
        pd,tp,td = drs_dict0.pop_dyn()
        drs_rep = {}
        drs_rep['cellpop'] = pd
        drs_rep['tout'] = tp
        drs_rep['t_death'] = td
        drs_dose['r'+str(rep+1)] = drs_rep
    return drs_dose





#%% generate population dynamics summary datasets



drugs_exp = ['Alpelisib','Neratinib','Trametinib','Palbociclib']

drs_all = {}

#%

for dr_idx in range(len(drugs_exp)):
    
    drug = drugs_exp[dr_idx][:5].lower()
    
    
    drs_drug = {}
    
    for d in range(10):
        
        drs_dose = drs_summarize(drug, d)
        drs_drug['d'+str(d)] = drs_dose
        
    drs_all[drug] = drs_drug

#%

pickle.dump(drs_all, open(os.path.join(wd,'output','in_silico_drs_summary','drs_summary.pkl'),'wb'))




#%% replicate median dose respnose population dynamics


drs_median = {}

drugs = list(drs_all.keys())

for dr in drugs:
    
    drs_median_drug = {}
    
    for dl in range(10):
        
        drs_median_dose = {}
        
        tp_drs = [drs_all[dr]['d'+str(dl)]['r'+str(rep+1)]['tout'] for rep in range(10)]
        popdyn_reps0 = [drs_all[dr]['d'+str(dl)]['r'+str(rep+1)]['cellpop'] for rep in range(10)]
        tp_all = np.array(list(itertools.chain(*tp_drs)))
        tp_all = np.unique(tp_all)
        tp_max = min([tp_drs[x][-1] for x in range(len(tp_drs))])
        tp_max_idx = np.where(tp_all == tp_max)[0][0]
        tp_all = tp_all[:tp_max_idx+1]
        popdyn_reps = []
        for rep in range(10):
            interpolator = interp1d(tp_drs[rep],popdyn_reps0[rep])
            y_new = interpolator(tp_all)
            popdyn_reps.append(y_new)
            
        popdyn_med = np.median(popdyn_reps,axis=0)
        
        drs_median_dose['cellpop'] = popdyn_med
        drs_median_dose['tout'] = tp_all
        
        drs_median_drug['d'+str(dl)] = drs_median_dose
        
    drs_median[dr] = drs_median_drug

#%

pickle.dump(drs_median, open(os.path.join(wd,'output','in_silico_drs_summary','drs_median.pkl'),'wb'))

#%% load datasets if they're already generated

with open(os.path.join(wd,'output','in_silico_drs_summary','drs_summary.pkl'),'rb') as f:
    drs_summary_full = pickle.load(f)

with open(os.path.join(wd,'output','in_silico_drs_summary','drs_median.pkl'),'rb') as f:
    drs_summary_median = pickle.load(f)


#%% drs_plots % median population dynamics (trametinib example)

drugs_exp = ['Alpelisib','Neratinib','Trametinib','Palbociclib']

drug_idx = 2

drug = drugs_exp[drug_idx][:5].lower()

for dl in range(10):
    
    dose = doses_all[dl]
    
    x_dl = drs_median[drug]['d'+str(dl)]['tout']/3600
    y_dl = drs_median[drug]['d'+str(dl)]['cellpop']
    
    plt.plot(x_dl,y_dl,label=f"{doses_all[dl]:.3f}")
    

plt.legend(bbox_to_anchor=(1.05,1.05),title='Doses (\u03BCM)',fontsize=15,title_fontsize=15)
plt.ylim(0,550)
plt.xlim(0,72)
plt.xticks(fontsize=15)
plt.yticks(fontsize=15)
# plt.xlabel('Time (h)')
# plt.ylabel('# of cells')
# plt.title(drugs_exp[2])
plt.show()