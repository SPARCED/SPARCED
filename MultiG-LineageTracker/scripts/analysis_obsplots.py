# -*- coding: utf-8 -*-
"""
Created on Mon May 13 13:06:25 2024

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



#%% define formula for plotting obs


ObsMat = pd.read_csv(os.path.join(wd,'input_files','Observables.txt'),sep='\t',header=0,index_col=0)
Species_doc = pd.read_csv(os.path.join(wd,'input_files','Species.txt'),sep='\t',header=0,index_col=0)
Compartment_vol = pd.read_csv(os.path.join(wd,'input_files','Compartments.txt'),sep='\t',header=0,index_col=0)

# ppERK/total ERK

sp_erk = list(np.array(species_all)[np.where(ObsMat.loc[:,'ERK'].values)[0]])

sp_pperk = list(np.array(sp_erk)[np.where(['ppERK' in sp_erk[k] for k in range(len(sp_erk))])[0]])

formula_num = ''

for sp in sp_pperk:
    sp_comp = Species_doc.loc[sp,'compartment']
    multiplier = float(ObsMat.loc[sp,'ERK'])*float(Compartment_vol.loc[sp_comp,'volume'])
    num_item = str(sp)+'*'+str(multiplier)
    formula_num = formula_num+'+'+num_item

formula_num = formula_num[1:]

formula_den = ''

for sp in sp_erk:
    sp_comp = Species_doc.loc[sp,'compartment']
    multiplier = float(ObsMat.loc[sp,'ERK'])*float(Compartment_vol.loc[sp_comp,'volume'])
    den_item = str(sp)+'*'+str(multiplier)
    formula_den = formula_den+'+'+den_item

formula_den = formula_den[1:]

formula_ppERK = '(' + formula_num + ')/(' + formula_den + ')'


## ppAKT/total AKT

sp_akt = list(np.array(species_all)[np.where(ObsMat.loc[:,'AKT'].values)[0]])

sp_ppakt = list(np.array(sp_akt)[np.where(['ppAKT' in sp_akt[k] for k in range(len(sp_akt))])[0]])

formula_num = ''

for sp in sp_ppakt:
    sp_comp = Species_doc.loc[sp,'compartment']
    multiplier = float(ObsMat.loc[sp,'AKT'])*float(Compartment_vol.loc[sp_comp,'volume'])
    num_item = str(sp)+'*'+str(multiplier)
    formula_num = formula_num+'+'+num_item

formula_num = formula_num[1:]

formula_den = ''

for sp in sp_akt:
    sp_comp = Species_doc.loc[sp,'compartment']
    multiplier = float(ObsMat.loc[sp,'AKT'])*float(Compartment_vol.loc[sp_comp,'volume'])
    den_item = str(sp)+'*'+str(multiplier)
    formula_den = formula_den+'+'+den_item

formula_den = formula_den[1:]

formula_ppAKT = '(' + formula_num + ')/(' + formula_den + ')'

#% fractional EGFR inhibition

sp_EGFR = list(np.array(species_all)[np.where(ObsMat.loc[:,'E1'].values)[0]])

sp_EGFR_nerat = list(np.array(sp_EGFR)[np.where(['nerat' in sp_EGFR[k] for k in range(len(sp_EGFR))])[0]])


formula_num_egfr = ''

for sp in sp_EGFR_nerat:
    sp_comp = Species_doc.loc[sp,'compartment']
    multiplier = float(ObsMat.loc[sp,'E1'])*float(Compartment_vol.loc[sp_comp,'volume'])
    num_item = str(sp)+'*'+str(multiplier)
    formula_num_egfr = formula_num_egfr +'+'+num_item

formula_num_egfr = formula_num_egfr[1:]

formula_den_egfr = ''

for sp in sp_EGFR:
    sp_comp = Species_doc.loc[sp,'compartment']
    multiplier = float(ObsMat.loc[sp,'E1'])*float(Compartment_vol.loc[sp_comp,'volume'])
    den_item = str(sp)+'*'+str(multiplier)
    formula_den_egfr = formula_den_egfr+'+'+den_item

formula_den_egfr = formula_den_egfr[1:]

formula_egfr = '(' + formula_num_egfr + ')/(' + formula_den_egfr + ')'

#% palbociclib target engagement

sp_Md = list(np.array(species_all)[np.where(ObsMat.loc[:,'Cd'].values)[0]])

sp_Md.remove('Cd')

sp_Md_drug = list(np.array(sp_Md)[np.where(['palbo' in sp_Md[k] for k in range(len(sp_Md))])])

formula_num_palbo_target = ''

for sp in sp_Md_drug:
    sp_comp = Species_doc.loc[sp,'compartment']
    multiplier = float(ObsMat.loc[sp,'Cd'])*float(Compartment_vol.loc[sp_comp,'volume'])
    num_item = str(sp)+'*'+str(multiplier)
    formula_num_palbo_target = formula_num_palbo_target +'+'+num_item
    
formula_num_palbo_target = formula_num_palbo_target[1:]
    
formula_den_palbo_target = ''

for sp in sp_Md:
    sp_comp = Species_doc.loc[sp,'compartment']
    multiplier = float(ObsMat.loc[sp,'Cd'])*float(Compartment_vol.loc[sp_comp,'volume'])
    den_item = str(sp)+'*'+str(multiplier)
    formula_den_palbo_target = formula_den_palbo_target +'+'+den_item

formula_den_palbo_target = formula_den_palbo_target[1:]

formula_palbo_target = '(' + formula_num_palbo_target + ')/(' + formula_den_palbo_target + ')'





#%%

def pop_obs_plot(obs_array,timepoints):
    obs_mean = np.array([np.nanmean(obs_array[:,tp]) for tp in range(len(timepoints))])
    obs_sd = np.array([np.nanstd(obs_array[:,tp]) for tp in range(len(timepoints))])


    for cell in range(np.shape(obs_array)[0]):
        plt.plot(timepoints/3600,obs_array[cell,:],linewidth=0.5,color='grey')
    
    plt.plot(timepoints/3600,obs_mean,linewidth=2.0,color='red',label='Mean')
    plt.plot(timepoints/3600,obs_mean+obs_sd,linewidth=2.0,color='blue',label='+SD')
    plt.plot(timepoints/3600,obs_mean-obs_sd,linewidth=2.0,color='blue',label='-SD')
    
    
    ymax = np.nanmax(obs_array)*1.25
    
    plt.ylim(0,ymax)
    plt.xlim(0,74)
    plt.xticks(fontsize=15)
    plt.yticks(fontsize=15)
    plt.legend(bbox_to_anchor=(1.2,1.2),fontsize=20)
    
    plt.show()
    
#%% dose specific neratinib target engagement - Figure 4B

for dl in range(len(doses_all)):
    dose_dict = drs_dict(output_main,'nerat',1,dl)
    cells,tps,tout_deaths,obs_array = dose_dict.pop_dyn_obs(formula_egfr)
    obs_median = np.array([np.nanmedian(obs_array[:,tp]) for tp in range(len(tps))])
    plt.plot(tps/3600,obs_median,label=f"{doses_all[dl]:.3f}")
    
plt.ylim(0,1.2)
plt.xlim(0,74)
plt.xticks(fontsize=15)
plt.yticks(fontsize=15)
plt.legend(bbox_to_anchor=(1.05,1.1),title='Doses (\u03BCM)',fontsize=15,title_fontsize=15)
plt.show()        

#%% dose specific erk activity (old figure 5 C-E)

for dl in range(len(doses_all)):
    dose_dict = drs_dict(output_main,'nerat',1,dl)
    cells,tps,tout_deaths,obs_array = dose_dict.pop_dyn_obs(formula_ppERK)
    pop_obs_plot(obs_array,tps)

#%% dose specific palbociclib target engagement - Figure 3A

for dl in range(len(doses_all)):
    dose_dict = drs_dict(output_main,'palbo',1,dl)
    cells,tps,tout_deaths,obs_array = dose_dict.pop_dyn_obs(formula_palbo_target)
    obs_median = np.array([np.nanmedian(obs_array[:,tp]) for tp in range(len(tps))])
    plt.plot(tps/3600,obs_median,label=f"{doses_all[dl]:.3f}")
    
# plt.ylim(0,1.2)
plt.xlim(0,74)
plt.xticks(fontsize=15)
plt.yticks(fontsize=15)
plt.legend(bbox_to_anchor=(1.05,1.1),title='Doses (\u03BCM)',fontsize=15,title_fontsize=15)
plt.show()   

