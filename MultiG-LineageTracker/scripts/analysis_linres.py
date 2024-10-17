# -*- coding: utf-8 -*-
"""
Created on Mon May 13 13:22:09 2024

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
output_main = os.path.join(wd,'output',exp_title)
# output_main = os.path.join("E:\\",exp_title)


dir_doses_all = os.listdir(os.path.join(output_main,'drs_alpel','drs_alpel_rep1'))

doses_all = [float(x.split('_')[-1]) for x in dir_doses_all]

doses_all.sort()


#%%

# import class for reading dose response outputs

from modules.drsPlotting import drs_dict



#%% test - load data

trame1_7 = drs_dict(output_main,'trame',1,7)

trame1_7.get_desc(4)

trame1_7.get_g1desc()



#%% count g1 descendents for all control conditions

drugs_all = ['alpel','lapat','nerat','palbo','trame']

g1desc_all = []

for drug in drugs_all:
    for rep in range(10):
        print(drug+'.....'+str(rep+1))
        control_dict = drs_dict(output_main,drug,rep+1,0)
        g1desc_all.append(control_dict.get_g1desc())

np.savetxt(os.path.join(wd,'output','in_silico_drs_summary','g1_desc_control.tsv'),np.array(g1desc_all),delimiter='\t')

plt.figure()

plt.hist(np.array(g1desc_all).flatten())
plt.show()

# fast > 25, 0 < moderate <25 

#%% species ranks g1 (ranks all species based on dynamic variance between grp0 and grp1)


# dl = 9

for dl in range(10):

    dict_0 = drs_dict(output_main,'trame',1,dl)
    
    srf = dict_0.rank_sp_g1()
    
    for rep in range(1,10):
        
        dict_current = drs_dict(output_main,'trame',rep+1,dl)
        
        srf_n = dict_current.rank_sp_g1()
        
        srf = srf + srf_n
        
    
    srf.to_csv(os.path.join(wd,'output','in_silico_drs_summary','trame_rank_sp_g1_'+str(dl)+'.tsv'),sep='\t')

#%% species ranks g2 (ranks all species based on dynamic variance between grp0 and grp2)

# dl = 9

for dl in range(10):

    dict_0 = drs_dict(output_main,'trame',1,dl)
    
    srf = dict_0.rank_sp_g2()
    
    for rep in range(1,10):
        
        dict_current = drs_dict(output_main,'trame',rep+1,dl)
        
        srf_n = dict_current.rank_sp_g2()
        
        srf = srf + srf_n
        
    
    srf.to_csv(os.path.join(wd,'output','in_silico_drs_summary','trame_rank_sp_g2_'+str(dl)+'.tsv'),sep='\t')

#%% top sp variation g1 

srf_trame_g1 = {}

for dl in range(10):
    srf_read = pd.read_csv(os.path.join(wd,'output','in_silico_drs_summary','trame_rank_sp_g1_'+str(dl)+'.tsv'),sep='\t',index_col=0,header=0)
    srf_trame_g1[str(dl)] = srf_read


#%%
x1= srf_trame_g1['0']['auc'].values

x2_g1 = np.log10(x1)

x3= x2_g1[~np.isinf(x2_g1)]

x4 = x3[x3>0]

plt.hist(x4)
plt.show()

#%% top sp variation g2

srf_trame_g2 = {}

for dl in range(10):
    srf_read = pd.read_csv(os.path.join(wd,'output','in_silico_drs_summary','trame_rank_sp_g2_'+str(dl)+'.tsv'),sep='\t',index_col=0,header=0)
    srf_trame_g2[str(dl)] = srf_read


#%%
x1= srf_trame_g2['0']['auc'].values

x2_g2 = np.log10(x1)

x3= x2_g2[~np.isinf(x2_g2)]

x4 = x3[x3>0]

plt.hist(x4)
plt.show()

#%%
plt.scatter(range(len(x2_g1)),x2_g1,label='moderate')
plt.scatter(range(len(x2_g2)),x2_g2,label='fast')

plt.ylim(0,max(max(x2_g1),max(x2_g2))*1.25)
plt.ylabel('log10 of AUC sum')
plt.xlabel('species_index')
plt.legend()

plt.show()

#%%

plt.scatter(range(len(x2_g1)),x2_g1)
plt.ylim(0,max(x2_g1)*1.25)
plt.ylabel('log10 of AUC sum')
plt.xlabel('species_index')

plt.show()



#%% split lineage for cell groups, find terminal lineages

    # for g1cx in grp2:
        
# g1cx = 39

trame2_5 = drs_dict(output_main,'trame',2,5) # trametinib replicate 2, dose level 5

drs_dict_test = trame2_5
        
# tout = drs_dict_test.results['output_g1'][str(g1cx)]['output']['tout']/3600
# obs = np.array(obs_grp2[str(g1cx)])[:,obs_idx]
# plt.plot(tout,obs,color='blue',label='grp2')

term_lins = []

for g1cx in trame2_5.grp2:

    desc_all = drs_dict_test.get_desc(g1cx)
    
    n_desc_all = len([item for sublist in desc_all.values() for item in sublist])
    
    
    
    
    
    if n_desc_all > 0:
        
        for gn in range(len(desc_all.keys())):
            gen = gn+2
            gncxs = desc_all['g'+str(gen)]
            if len(gncxs)>0:
                for cx in range(len(gncxs)):
                    gncx = gncxs[cx]
                    desc_gncx = drs_dict_test.get_desc_gc(gen,gncx)
                    if len(desc_gncx) == 0:
                        lin_gncx = drs_dict_test.results['output_g'+str(gen)][str(gncx)]['output']['lin']
                        lin_gncx = lin_gncx+'c'+str(gncx)
                        term_lins.append(lin_gncx)
 
term_lins_outputs = {}

for term_lin in term_lins:
    
    outputs_lin = {}
    
    lin_cells = term_lin.split('c')[1:]
    
    gn = 1
    
    xout_lin = []
    tout_lin = []
    
    for gncx in lin_cells:
        
        output_gncx = drs_dict_test.results['output_g'+str(gn)][str(gncx)]['output']
        xout_gncx = output_gncx['xoutS']
        tout_gncx = output_gncx['tout']
        
        xout_lin.append(xout_gncx)
        tout_lin.append(tout_gncx)
        
        gn+= 1
        
    xout_lin = np.concatenate(xout_lin,axis=0)
    tout_lin = np.concatenate(tout_lin,axis=0)
    
    outputs_lin['xoutS'] = xout_lin
    outputs_lin['tout'] = tout_lin
    
    term_lins_outputs[term_lin] = outputs_lin
    
#%%

# term_lin  = list(term_lins_outputs.keys())[7]
    
# xout_lin = term_lins_outputs[term_lin]['xoutS']

# tout_lin = term_lins_outputs[term_lin]['tout']

# touts_lin = [term_lins_outputs[term_lin_key]['tout'] for term_lin_key in term_lins_outputs.keys()]

# touts_lin = [item for sublist in touts_lin for item in sublist]

# touts_lin = np.unique(np.array(touts_lin))

# touts_lin = touts_lin[:-200]

# interpolated_values = interp1d(tout_lin, xout_lin, axis=0)(touts_lin)


# xx = trame2_5.term_lins(grp2)

#%% example species trajectory for terminal lineages

# all

sp_lin = 'ppAKT'

for term_lin in list(term_lins_outputs.keys()):
    
    xout_lin = term_lins_outputs[term_lin]['xoutS']
    tout_lin = term_lins_outputs[term_lin]['tout']
    sp_traj = xout_lin[:,list(species_all).index(sp_lin)]
    
    plt.plot(tout_lin/3600,sp_traj)
    
plt.show()
    
#% single lineage

term_lins_test = term_lins_outputs

sp_lin = 'Mb'

term_lin  = list(term_lins_test.keys())[9]
    
xout_lin = term_lins_test[term_lin]['xoutS']
tout_lin = term_lins_test[term_lin]['tout']
sp_traj = xout_lin[:,list(species_all).index(sp_lin)]

plt.figure()

plt.plot(tout_lin/3600,sp_traj)
plt.title(str(term_lin))
    
plt.show()



#%% compare grp2/grp0

xx = trame2_5.term_lins(trame2_5.grp2)

term_lin = list(xx.keys())[0]

g1cx_grp0 = 3

output_g0 = drs_dict_test.results['output_g1'][str(g1cx_grp0)]['output']

xout_g0 = output_g0['xoutS']
tout_g0 = output_g0['tout']

xout_g2 = xx[term_lin]['xoutS']
tout_g2 = xx[term_lin]['tout']

tout_compare = np.unique(np.concatenate((tout_g0,tout_g2)))

tp_final = min(max(tout_g0),max(tout_g2))

tout_compare = tout_compare[:np.where(tout_compare >= tp_final)[0][0]]

xout_g0_new = interp1d(tout_g0,xout_g0,axis=0)(tout_compare)
xout_g2_new = interp1d(tout_g2,xout_g2,axis=0)(tout_compare)

xout_diff = (xout_g2_new - xout_g0_new)/xout_g0_new


#%%

sp_compare = 'ppAKT'

y0 = xout_g0_new[:,list(species_all).index(sp_compare)]
y2 = xout_g2_new[:,list(species_all).index(sp_compare)]

plt.plot(tout_compare/3600,y0,label='x_group0')
plt.plot(tout_compare/3600,y2,label='x_group2')



ymax = max(max(y0),max(y2))

plt.ylim(0,ymax*1.25)

plt.xlabel('Time (hours)')
plt.ylabel('Species concentration (nM)')
plt.legend()

plt.show()






#%%


def normalized_me(array1, array2, epsilon=1e-10):
    """
    Calculate the normalized mean squared error between two arrays.
    """
    numerator = array1 - array2
    denominator = array2 + epsilon  # Avoid division by zero
    return np.square(numerator) / np.square(denominator)

#%%


xout_error = normalized_me(xout_g2_new, xout_g0_new)




sp_auc = pd.Series(np.array([np.trapz(xout_error[:,sp_idx],tout_compare) for sp_idx in range(np.shape(xout_error)[1])]),index=species_all)

#%%

plt.plot(tout_compare/3600,xout_error[:,list(species_all).index(sp_compare)])
plt.ylabel('Squared normalized error')
plt.xlabel('Time (hours)')

plt.show()


#%%


plt.hist(sp_auc.values,bins=np.logspace(-8,18,27))

plt.xscale('log')

plt.show()


#%% generate species ranks for all dose levels of Trametinib



for dl in range(10):
    dict_0 = drs_dict(output_main,'trame',1,dl)
    
    srf = dict_0.rank_sp()
    
    for rep in range(1,10):
        
        dict_current = drs_dict(output_main,'trame',rep+1,dl)
        
        srf_n = dict_current.rank_sp()
        
        srf = srf + srf_n
        
    
    srf.to_csv(os.path.join(wd,'output','in_silico_drs_summary','trame_rank_sp_'+str(dl)+'.tsv'),sep='\t')

#%% species ranks heatmaps / mRNA

srf_trame = {}

for dl in range(10):
    srf_read = pd.read_csv(os.path.join(wd,'output','in_silico_drs_summary','trame_rank_sp_'+str(dl)+'.tsv'),sep='\t',index_col=0,header=0)
    srf_trame[str(dl)] = srf_read


#%

model_genes = list(pd.read_csv(os.path.join(wd,'input_files','OmicsData.txt'),sep='\t',index_col=0).index)

srf_heatmap = pd.DataFrame(index=['dl_'+str(dl) for dl in range(10)],columns = ['m_'+str(gene) for gene in model_genes],dtype='float')

for dl in range(10):
    
    srf_mrna = np.array([srf_trame[str(dl)].loc[spc,'score'] for spc in srf_heatmap.columns])
    
    srf_heatmap_dl = [percentileofscore(srf_trame[str(dl)].loc[:,'score'].values,x) for x in srf_mrna]
    
    srf_heatmap.loc['dl_'+str(dl),:] = srf_heatmap_dl


#%

plt.figure(figsize=(24,32))

sns.heatmap(srf_heatmap.iloc[:,:141].transpose())

# plt.show()

plt.savefig(os.path.join(wd,'output','in_silico_drs_summary','mRNA_heatmap.png'))

plt.figure(figsize=(12,16))

sns.clustermap(srf_heatmap.transpose())

plt.show()

#%% 

genes_top = []

pm = 90 # percentile margin

for gene in model_genes:
    
    vals = srf_heatmap.loc[:,'m_'+str(gene)].values
    
    vals_check = vals>pm
    
    if vals_check.all():
        genes_top.append(gene)


#%

srf_heatmap_top = pd.DataFrame(index=['dl_'+str(dl) for dl in range(10)],columns = ['m_'+str(gene) for gene in genes_top],dtype='float')

for gene in genes_top:
        
    srf_heatmap_top.loc[:,'m_'+str(gene)] = srf_heatmap.loc[:,'m_'+str(gene)]
    
plt.figure(figsize=(12,16))

sns.heatmap(srf_heatmap_top.transpose())

plt.show()



plt.figure(figsize=(12,16))

sns.clustermap(srf_heatmap_top.transpose())

plt.show()

# plt.savefig(os.path.join(wd,'output','in_silico_drs_summary','mRNA_heatmap.png'))

#%% plot log10 transformed AUC sum for all species (from pairwise comparisons)

x1= srf_trame['0']['auc'].values

x2 = np.log10(x1)

x3= x2[~np.isinf(x2)]

x4 = x3[x3>0]

plt.hist(x4)
plt.show()


# plt.hist(x4,bins=10)
# plt.show()


