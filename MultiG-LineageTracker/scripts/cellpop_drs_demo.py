#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
script name: createModel.py
Created on Fri May 12 18:06:40 2023
Author: Arnab Mutsuddy (edited by JRH)

Description: This script is used to run SPARCED model for a given cell 
            population and drug dose.

Output: The script generates output files for each cell in the cell population.
        The output files contain the time course of the Mb species for each 
        cell.

"""
#-----------------------Package Import & Defined Arguements-------------------#
import pandas as pd
import numpy as np

import libsbml
import os
import sys
import importlib
import amici
import argparse
from scipy.signal import find_peaks
import itertools
from datetime import datetime
from mpi4py import MPI
import pickle


#%% Retrieving MPI rank ID
comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()

#%% argparse parameters

parser = argparse.ArgumentParser(description='')

parser.add_argument('--cellpop', metavar='cellpop', help='starting cellpopulation', default = 5)
parser.add_argument('--td',metavar='td', help='cell line doubling time (hrs) ', default = 48)
parser.add_argument('--sim_name', metavar='sim_name', help='insert exp name', default = 'testmpi_tasks')
parser.add_argument('--mb_tr',metavar='mb_tr',help='Mb trough upper limit (nM)', default = 2.0)
parser.add_argument('--exp_time', metavar='exp_time', help='Enter experiment time in hours', default = 72.0)
parser.add_argument('--drug', metavar='drug', help='input drug species name', default = 'trame_EC')
parser.add_argument('--dose', metavar='dose', help='input drug dose uM', default = 0.0)
parser.add_argument('--egf', metavar='egf', help='input E conc in nM', default = 3.308)
parser.add_argument('--ins', metavar='ins', help='input INS conc in nM', default = 1721.76)
parser.add_argument('--hgf', metavar='hgf', help='input HGF conc in nM', default = 0.0)
parser.add_argument('--nrg', metavar='nrg', help='input H conc in nM', default = 0.0)
parser.add_argument('--pdgf', metavar='pdgf', help='input PDGF conc in nM', default = 0.0)
parser.add_argument('--igf', metavar='igf', help='input IGF conc in nM', default = 0.0)
parser.add_argument('--fgf', metavar='fgf', help='input FGF conc in nM', default = 0.0)

# parser.add_argument('--override_param', metavar='override_param',default = 0.0)
# parser.add_argument('--override_ic', metavar='override_ic',default = 0.0)
# parser.add_argument('--override_param_id', metavar='override_param_id',default='k1813')
# parser.add_argument('--override_param_val',metavar='override_param_val',default=0.0002)
# parser.add_argument('--override_ic_file', metavar='override_ic_file',default='ic_k1813')

args = parser.parse_args()


#%%  Define current and working directory, import SPARCED model

cd = os.getcwd()
wd = os.path.dirname(cd)
sys.path.append(os.path.join(wd,'bin'))


sim_name = str(args.sim_name)

output_path = os.path.join(wd,'output',sim_name)

if rank==0:
    if not os.path.exists(output_path):
        os.mkdir(output_path)


sbml_file = "SPARCED.xml"
model_name= sbml_file[0:-4]
model_output_dir = model_name
sys.path.insert(0, os.path.join(wd,model_output_dir))
model_module = importlib.import_module(model_name)
model = model_module.getModel()   


from modules.RunSPARCED import RunSPARCED

#%% 
omics_input = 'OmicsData.txt'
genereg_input = 'GeneReg.txt'

# Stochastic (0) or deterministic (1) gene switching decision point, 
# assigned as stochastic here for a heterogeneous cell population.
flagD = 0

# Deterministic simulation interval between stochastic gene expression updates.
ts = 30

# Length of simulation, user defined via CLI, flag '--exp_time'
th = float(args.exp_time)

# Initial concentrations of SPARCED species
species_all = list(model.getStateIds())

# Assign the CVODES and/or IDAS solvers to an object of the model class, 
# and specify the maximum number of iterations for the forward solver.
solver = model.getSolver()
solver.setMaxSteps = 1e10

# Set the timepoints for the simulation on a fixed 'ts' defined interval
model.setTimepoints(np.linspace(0,ts))

# Set the initial number of cells to start the simulation. 
cell_pop = int(args.cellpop)

#%% User defined (CLI) growth factor conditions
dose_egf = float(args.egf)
dose_ins = float(args.ins)
dose_hgf = float(args.hgf)
dose_fgf = float(args.fgf)
dose_igf = float(args.igf)
dose_pdgf = float(args.pdgf)
dose_nrg = float(args.nrg)

STIMligs_id = ['E', 'H', 'HGF', 'P', 'F', 'I', 'INS']

STIMligs = [dose_egf,dose_nrg,dose_hgf,dose_pdgf,dose_fgf,dose_igf,dose_ins]

# User defined drug dose and species via flag '--drug' and '--dose'
drug = str(args.drug)
dose = float(args.dose)*10e2

species_initializations = np.array(model_module.getModel().getInitialStates())
species_initializations[np.argwhere(species_initializations <= 1e-6)] = 0.0

for l,lig in enumerate(STIMligs_id):
    species_initializations[species_all.index(lig)] = 0

#%% Define output directory for drug dose simulation
output_dose = os.path.join(output_path,drug+'_'+str(float(args.dose)))

if rank==0:
    if not os.path.exists(output_dose):
        os.mkdir(output_dose)

output_dir = output_dose ### JRH: Check for redundant variable



#%% Assign MPI tasks to ranks based on starting cell population
def assign_tasks(rank,n_cells,size):
    
    cells_per_rank = n_cells // int(size)
    remainder = n_cells % int(size)
    
    if rank < remainder:
        my_cells = cells_per_rank + 1
        start_cell = rank * my_cells + 1
    else:
        my_cells = cells_per_rank
        start_cell = rank * cells_per_rank + remainder + 1
        
    return start_cell, start_cell + my_cells

#%% -------------------Preincubation/Heterogenization stage-------------------#
# designed to create 
# variability within the starting cell population to replicate 
# experimentally observed heterogeneity. 

# Preincubation timeframe
th = 48

# initial preincubation cell population size
cellpop_preinc = int(cell_pop)
cell0, cell_end = assign_tasks(rank,cellpop_preinc,size)

# Generate task-specific dictionaries
preinc_dict = {}

for task in range(cell0, cell_end):
    
    np.random.seed()
 
    tstmp = str(datetime.now().strftime("%d %m %Y %H:%M:%S"))
    
    print("Running preincubate (%d) on rank %d | %s" %(task, rank, tstmp))
    
    # Generate randomly initialized cell states for each cell in the population
    xoutS_all, xoutG_all, tout_all = RunSPARCED(flagD,th,
                                                species_initializations,[],
                                                sbml_file,model)

    # Extract the final state of the cell after preincubation for 
    # initial conditions in the subsequent gen 0 simulation.
    preinc_IC = xoutS_all[-1]
    
    # Send cell-specific preincubation results to rank 0
    preinc_dict[task] = {'cell':int(task), 'preinc_IC':preinc_IC}

# Rank 0 stores all preincubation results for all initial cells.
if rank != 0:
    comm.send(preinc_dict,dest=0)

results_preinc = None

### Data Collection Stage ###
if rank == 0:
    # Root rank receives preincubation results from all ranks
    
    results_preinc_recv = []
    results_preinc_recv.append(preinc_dict)
    for r in range(1,size):
        results_preinc_recv.append(comm.recv(source=r))
        
    results_collect = []
    
    for i in range(size):
        results_collect.extend(list(results_preinc_recv[i].values()))
    
    results_preinc = {}
    
    for i in range(len(results_collect)):
        cell = results_collect[i]['cell']
        results_preinc [str(cell)] = results_collect[i]['preinc_IC'] 
        
results_preinc = comm.bcast(results_preinc, root = 0)

# Prevents the simulation from proceeding until all ranks have completed the
# preincubation stage.
comm.Barrier()

#%% ------------------Initiate gen 0 (asynchronous cycling)-------------------#
# Generates a simulation for each cell and grabs only the cyclin B - CDK1
# complex results for each cell in the population, appends it to generation
# 1 initial conditions for said cell. Assigned growth factor conditions 
# from preincubation stage to each cell in the population start here.
th_g0 = 48

cellpop_g0 = cell_pop ### Potentially redunant, solvable with __init__ method? | JRH

output_dir = output_dose ### JRH: Is the output_dose reassigned anywhere? If not, suggest removing.

g0_dict = {}
g0_cell_start, g0_cell_end = assign_tasks(rank,cellpop_g0,size)

for task in range(g0_cell_start, g0_cell_end):
    # Tasks correspond to individual cells in the population
    cell_n = int(task)
    
    np.random.seed()

    tstmp = str(datetime.now().strftime("%d %m %Y %H:%M:%S"))
    
    print("Running gen0 cell (%d) on rank %d | %s" %(cell_n, rank, tstmp))
    
    s_preinc_i = results_preinc[str(cell_n)]
    sp_input = np.array(s_preinc_i)

    sp_input[np.argwhere(sp_input <= 1e-6)] = 0.0
    
    for l,lig in enumerate(STIMligs_id):
        sp_input[species_all.index(lig)] = STIMligs[l]
         
    xoutS_all, xoutG_all, tout_all = RunSPARCED(flagD,th_g0,sp_input,
                                                [],sbml_file,model)
    
    np.random.seed()
    tp_g0 = np.random.randint(0,np.shape(xoutS_all)[0]) 
    ic_g1 = xoutS_all[tp_g0,:]
    
    output_g0_cell = {}

    # Extract the final state of the cell after preincubation for
    # only the cyclin B - CDK1 for each cell in the population.
    output_g0_cell['xoutS'] = xoutS_all[:,list(species_all).index('Mb')]

    # Individual cell outputs are stored in a 
    # dictionary for each cell in the population.
    # Stores cell identifier, Mb timecourse, initial 
    # conditions for gen 1, and division timepoint for gen 0.
    g0_dict[task] = {'cell':cell_n,'result':output_g0_cell,
                     'ic_g1':ic_g1, 'tp_g0':tp_g0}
    
# MPI communication step to send gen 0 results to rank 0, 
# where all results are collected and stored.
if rank!= 0:
    comm.send(g0_dict,dest=0)
      
results_g0 = None
ics_g1 = None
tps_g0 = None

if rank == 0:
    results_g0_recv = []
    results_g0_recv.append(g0_dict)
    for r in range(1,size):
        results_g0_recv.append(comm.recv(source=r))
        
    results_g0_collect = []
    
    for i in range(size):
        results_g0_collect.extend(list(results_g0_recv[i].values()))
    
    results_g0 = {}    
    ics_g1 = {}
    tps_g0 = {}
    
    for i in range(len(results_g0_collect)):
        cell = results_g0_collect[i]['cell']
        results_g0[str(cell)] = results_g0_collect[i]['result']
        ics_g1[str(cell)] = results_g0_collect[i]['ic_g1']
        tps_g0[str(cell)] = results_g0_collect[i]['tp_g0']
        
results_g0 = comm.bcast(results_g0, root = 0)
ics_g1 = comm.bcast(ics_g1, root = 0)
tps_g0 = comm.bcast(tps_g0, root = 0)
comm.Barrier()

# save g0 results
with open(os.path.join(output_dir,"results_g0.pkl"),"wb") as f:
    pickle.dump(results_g0,f) # Write gen 1 output to disk


#%%---------------------additional step for demo (figure 2)-------------------#
#Functions for finding cell division time points and division points
mb_tr = float(args.mb_tr)

def find_dp(xoutS: np.array, species_all=species_all):
    """
    Function to find the division point of a single cell
    using the value of cyclin B - CDK2 complex  trough as a threshold.

    Parameters:
    xoutS : numpy array
        Array of species concentrations over time.

    species_all : list

    Returns:
    dp : int or nan | division point
    
    """
    data = xoutS[:,list(species_all).index('Mb')]
    p,_ = find_peaks(data,height=30)
    b = (np.diff(np.sign(np.diff(data))) > 0).nonzero()[0] + 1
    
    if len(b)!=0:
        b = np.array(b)[data[b]<mb_tr]
    
    if sum(b>p[0]) > 0:
    
        dp = int(b[b>p[0]][0])
        
    else:
        dp = np.nan
    
    return(dp)


def find_dp_all(data):
    """
    Finds all division points in a single cell using the value of 
    cyclin B - CDK2 complex trough as a threshold.
    
    Parameters:
    data : numpy array
        Array of species concentrations over time.

    species_all : list

    Returns:
    dp_all : list | division points
    """
    p,_ = find_peaks(data,height=30)
    b = (np.diff(np.sign(np.diff(data))) > 0).nonzero()[0] + 1
    
    dp_all = []
    for i in range(len(p)):
        b2 = np.where(b>p[i])[0]
        if len(b2)!=0:
            dp_all.append(b[b2[0]])
    
    if len(dp_all)!=0:
        dp_all_actual = list(np.array(dp_all)[data[dp_all]<mb_tr])
        dp_all = dp_all_actual

    return(dp_all)


#%%-----------------------------Generation 1 Cells----------------------------#
# User defined simulation time length, defined via CLI, flag '--exp_time'
exp_time = float(args.exp_time)

th = exp_time + 3.0 ### Why is 3.0 added? | JRH

cellpop_g1 = cell_pop

output_dir = output_dose ### JRH: Is the output_dose reassigned anywhere? If not, suggest removing.

# generation 1 task assignment step
g1_cell_start, g1_cell_end = assign_tasks(rank,cellpop_g1,size)

# Instantiate task-specific dictionaries for generation 1 cells
g1_dict = {}

for task in range(g1_cell_start, g1_cell_end):
    cell_n = int(task)
    
    # First generation identifier starts with 'g1_c' and continues
    #  with the cell number
    cell_name = 'g1_c'+str(cell_n)
    
    tstmp = str(datetime.now().strftime("%d %m %Y %H:%M:%S"))
    
    print("Running gen1 cell (%d) on rank %d | %s" %(cell_n, rank, tstmp))
     
    # Extract gen 0 cell division timepoint and initial conditions
    x_s_g0 = results_g0[str(cell_n)]['xoutS']
    
    np.random.seed()

    # Extract gen 0 starting values for gen 1 simulation    
    tp_g0 = tps_g0[str(cell_n)]    
    sp_input = ics_g1[str(cell_n)]
    sp_input = np.array(sp_input)
    sp_input[np.argwhere(sp_input <= 1e-6)] = 0.0 # is there a functional reason for this? | JRH

    # Assign drug perturbation to the gen 1 cell
    sp_input[list(model.getStateIds()).index(drug)] = dose
    # Gen 1 cell simulation
    xoutS_g1, xoutG_g1, tout_g1 = RunSPARCED(flagD,th,sp_input,
                                             [],sbml_file,model) 
    
    # Extract the final state of the cell after gen 1 simulation
    xoutS_mb_g0 = x_s_g0
    xoutS_mb_g1 = xoutS_g1[:,list(species_all).index('Mb')]
    
    # Concatenate the gen 0 timepoints to the gen 1 timepoints
    tout_g0 = np.arange(0,th_g0*3600+1,ts)
    tout_g0 = tout_g0[0:len(xoutS_mb_g0)]
    if len(tout_g0[:tp_g0]) > 0:
    
        tneg_g0_min = max(tout_g0[:tp_g0]) - 16*3600
        
        tneg_idx_start = np.where(tout_g0[:tp_g0]>tneg_g0_min)[0][0]
        
        tout_g0_neg = tout_g0[:tp_g0][tneg_idx_start:tp_g0] - tout_g0[tp_g0]
        
        xoutS_mb_new = np.concatenate((xoutS_mb_g0[tneg_idx_start:tp_g0],
                                       xoutS_mb_g1),axis=0)
        
        tout_new = np.concatenate((tout_g0_neg,tout_g1),axis=0)
    
    else:
    
        xoutS_mb_new = xoutS_mb_g1
    
        tout_new = tout_g1
   
    # Detect cell divison event in gen 1 cell
    cb_peaks, _ = find_peaks(xoutS_mb_new,height=30)  
    
    # Downsample single cell outputs to every 20th timepoint
    xoutS_lite = np.array(list(itertools.islice(xoutS_g1,0,(len(xoutS_g1)-1),20)))
    xoutG_lite = np.array(list(itertools.islice(xoutG_g1,0,(len(xoutG_g1)-1),20)))
    tout_lite = np.array(list(itertools.islice(tout_g1,0,(len(tout_g1)-1),20)))
    
    g2_start = {}
    
    # Determine division point and gen 2 simulation time
    if len(cb_peaks)>0:
        
        dp_all = find_dp_all(xoutS_mb_new)

        dp = np.nan

        if len(dp_all)>0:
            
            # If we're able to find a division point, we assign it to dp
            if len(np.where(tout_new[dp_all]>0)[0]) > 0:
                dp_idx = np.where(tout_new[dp_all]>0)[0][0]
    
                dp = dp_all[dp_idx]
            
        # If a division point is found, we proceed with the gen 2 simulation
        if ~np.isnan(dp):
            dp_actual = dp - len(tout_new) + len(tout_g1)
            parp_dp = float(xoutS_g1[dp_actual,list(species_all).index('PARP')])
            cparp_dp = float(xoutS_g1[dp_actual,list(species_all).index('cPARP')])
            
            # The PARP / cPARP threshold is used to determine cell death
            if parp_dp > cparp_dp:
            
                tdp_g2_cell = tout_g1[dp_actual]/3600
                
                sp_g2_cell = xoutS_g1[dp_actual]
                
                # Assign the new cell lineage identifier for gen 2
                lin_g2_cell = 'c'+str(int(cell_n))
                
                g2_start['cell'] = int(cell_n)
                g2_start['dp'] = dp
                g2_start['th_g2'] = th- tdp_g2_cell    
                g2_start['lin'] = lin_g2_cell
                g2_start['ic'] = sp_g2_cell
                
                # Downsample gen 1 outputs to every 20th timepoint
                dp1 = np.where(tout_g1 == tout_new[dp])[0][0]
                xoutS_lite = np.array(list(itertools.islice(xoutS_g1,0,(dp1+1),20)))
                xoutG_lite = np.array(list(itertools.islice(xoutG_g1,0,(dp1+1),20)))
                tout_lite = np.array(list(itertools.islice(tout_g1,0,(dp1+1),20)))
    
    # Store gen 1 cell outputs and store as a dictionary pickle file
    output_g1_cell = {}
    
    output_g1_cell['cell'] = int(cell_n)
    output_g1_cell['xoutS'] = xoutS_lite
    output_g1_cell['xoutG'] = xoutG_lite
    output_g1_cell['tout'] = tout_lite
    
    result_g1_cell = {}
    
    result_g1_cell['output'] = output_g1_cell
    result_g1_cell['g2_start'] = g2_start
    
    g1_dict[task] = {'cell': cell_n, 'result': result_g1_cell}

# Gather results from all ranks to rank 0
if rank != 0:
    comm.send(g1_dict,dest=0)

results_g2start = None ### What is the function of this? Is it MPI-related to avoid deadlocks? | JRH

if rank == 0:
    results_g1_recv = []
    results_g1_recv.append(g1_dict)
    for r in range(1,size):
        results_g1_recv.append(comm.recv(source=r))
        
    results_g1_collect = []
    
    for i in range(size):
        results_g1_collect.extend(list(results_g1_recv[i].values()))
    
    results_g1 = {}    
    results_g2start = {}
    for i in range(len(results_g1_collect)):
        cell = results_g1_collect[i]['cell']
        results_g1[str(cell)] = results_g1_collect[i]['result']
        results_g2start[str(cell)] = results_g1_collect[i]['result']['g2_start']

    # Save generation 1 simulation results to disk
    with open(os.path.join(output_dir,"output_g1.pkl"),"wb") as f:
        pickle.dump(results_g1,f)
                
# Broadcast gen 2 details and halt simulation until all ranks have completed
results_g2start = comm.bcast(results_g2start, root = 0)
comm.Barrier()

#------------------------------Generation 2 Cells-----------------------------#
# Extract gen 2 details and evaluate for prior division events, 
# if none are found, the simulation is halted.
g2_start_all = [results_g2start[str(rn+1)] for rn in range(len(results_g2start))]
g2_start_actual = np.array(g2_start_all)[np.where(g2_start_all)[0]]
if len(g2_start_actual) != 0:
    
    th_g2 = [r['th_g2'] for r in g2_start_actual]
    
    lin_g2 = [r['lin'] for r in g2_start_actual]
    
    ic_g2 = [r['ic'] for r in g2_start_actual]

    th_g2 = [[th_g2[i]]+[th_g2[i]] for i in range(len(th_g2))]
    th_g2 = [item for sublist in th_g2 for item in sublist]
    
    lin_g2 = [[lin_g2[i]]+[lin_g2[i]] for i in range(len(lin_g2))]
    lin_g2 = [item for sublist in lin_g2 for item in sublist]
    
    ic_g2 = [[ic_g2[i]]+[ic_g2[i]] for i in range(len(ic_g2))]
    ic_g2 = [item for sublist in ic_g2 for item in sublist]
    
else:
    sys.exit("No division event detected at gen 1")

#%% While loop for running gen n (n>=2) cells until no division 
# events are detected
lin_gn0 = lin_g2

th_gn0 = th_g2

ic_gn0 = ic_g2

cellpop_gn0 = len(th_g2)

g = 2

comm.Barrier() ### What's the purpose for halting here? Does it ensure cell job
# assignment before proceeding to the next generation? | JRH

# Continue simulation until no division events are detected
while cellpop_gn0 > 0:
    
    gn_cell_start, gn_cell_end = assign_tasks(rank,cellpop_gn0,size)
    
    # Generate task-specific dictionaries
    gn_dict = {}
    
    # this proceeds in the same manner as the gen 1 cells (line 394)
    for task in range(gn_cell_start, gn_cell_end):
        
        cell_n = int(task)
        
        th_gc = th_gn0[cell_n-1]
        lin_gc = lin_gn0[cell_n-1]
        
        tstmp = str(datetime.now().strftime("%d %m %Y %H:%M:%S"))
        
        print("Running gen(%d) cell(%d) (lin(%s)) for (%d) hrs on rank %d | \
               %s" %(g,cell_n,lin_gc,th_gc,rank,tstmp))
        
        # Dynamic cell identifier assignment step
        cell_name = 'g'+str(g)+'_c'+str(cell_n)+'_lin_'+str(lin_gn0[cell_n-1])
        
        sp0 = ic_gn0[cell_n-1]
        
        # Simulation via SPARCED
        xoutS_all, xoutG_all, tout_all = RunSPARCED(flagD,th_gc,sp0,
                                                    [],sbml_file,model)
        
        tout_all = tout_all + (th-th_gc)*3600
        
        # Downsample single cell outputs to every 20th timepoint
        xoutS_lite = np.array(list(itertools.islice(xoutS_all,0,
                                                    (len(xoutS_all)-1),20)))
        
        xoutG_lite = np.array(list(itertools.islice(xoutG_all,0,
                                                    (len(xoutG_all)-1),20)))
        
        tout_lite = np.array(list(itertools.islice(tout_all,0,
                                                   (len(tout_all)-1),20)))     
        
        # Find division events in gen n
        cb_peaks, _ = find_peaks(xoutS_all[:, list(species_all).index('Mb')],
                                 height=30)
    
        gn1_start = {}        
        
        # Determine gen n division timepoints and gen (n+1) simulation times
        if len(cb_peaks)>0:
            
            dp = find_dp(xoutS_all,tout_all)
    
            if ~np.isnan(dp):
                
                parp_dp = float(xoutS_all[dp,list(species_all).index('PARP')])
                cparp_dp = float(xoutS_all[dp,list(species_all).index('cPARP')])
                
                if parp_dp > cparp_dp:
                    
                
                    tdp_gn_cell = tout_all[dp]/3600
                    
                    sp_gn_cell = xoutS_all[dp]
                    
                    lin_gn_cell = str(lin_gn0[cell_n-1])+'c'+str(cell_n)
                    
                    # Assign the new cell lineage dictionary entry for gen (n+1)
                    gn1_start['cell'] = int(cell_n)
                    gn1_start['dp'] = dp
                    gn1_start['th_gn'] = th- tdp_gn_cell    
                    gn1_start['lin'] = lin_gn_cell
                    gn1_start['ic'] = sp_gn_cell                             
    
                    # Downsample gen n outputs to every 20th timepoint
                    xoutS_lite = np.array(list(itertools.islice(xoutS_all,0,(dp+1),20)))
                    xoutG_lite = np.array(list(itertools.islice(xoutG_all,0,(dp+1),20)))
                    tout_lite = np.array(list(itertools.islice(tout_all,0,(dp+1),20)))
                    
        output_gn_cell = {}
        output_gn_cell['xoutS'] = xoutS_lite
        output_gn_cell['xoutG'] = xoutG_lite
        output_gn_cell['tout'] = tout_lite
        output_gn_cell['lin'] = str(lin_gc)
        
        result_gn_cell = {}
        
        result_gn_cell['output'] = output_gn_cell
        result_gn_cell['gn1_start'] = gn1_start
        
        gn_dict[task] = {'cell': cell_n, 'result': result_gn_cell}

    # For all cells in gen n, send results to rank 0    
    if rank!=0:
        comm.send(gn_dict,dest=0)
        
    results_gn1start = None
    if rank == 0:
        results_gn_recv = []
        results_gn_recv.append(gn_dict)
        for r in range(1,size):
            results_gn_recv.append(comm.recv(source=r))
            
        results_gn_collect = []
        
        for i in range(size):
            results_gn_collect.extend(list(results_gn_recv[i].values()))
        
        results_gn = {}
        results_gn1start = {}    
        for i in range(len(results_gn_collect)):
            cell = results_gn_collect[i]['cell']
            results_gn[str(cell)] = results_gn_collect[i]['result']
            results_gn1start[str(cell)] = results_gn_collect[i]['result']['gn1_start']
            
        with open(os.path.join(output_dir,"output_g"+str(g)+".pkl"),"wb") as f:
            pickle.dump(results_gn,f) # Save gen n outputs to disk

    # Broadcast gen (n+1) details
    results_gn1start = comm.bcast(results_gn1start, root = 0)
    
    comm.Barrier()
    
    gn1_start_all = [results_gn1start[str(rn+1)] \
                     for rn in range(len(results_gn1start))]
    
    gn1_start_actual = np.array(gn1_start_all)[np.where(gn1_start_all)[0]]
        
    th_gn = [r['th_gn'] for r in gn1_start_actual]
    
    lin_gn = [r['lin'] for r in gn1_start_actual]
    
    ic_gn = [r['ic'] for r in gn1_start_actual]

    th_gn = [[th_gn[i]]+[th_gn[i]] for i in range(len(th_gn))]
    th_gn = [item for sublist in th_gn for item in sublist]
    
    lin_gn = [[lin_gn[i]]+[lin_gn[i]] for i in range(len(lin_gn))]
    lin_gn = [item for sublist in lin_gn for item in sublist]
    
    ic_gn = [[ic_gn[i]]+[ic_gn[i]] for i in range(len(ic_gn))]
    ic_gn = [item for sublist in ic_gn for item in sublist]
    
    cellpop_gn = len(th_gn)
    
    cellpop_gn0 = cellpop_gn
    
    if cellpop_gn0 > 0:
        
        print("Division event detected at gen(%d)" %(g))
        g += 1
        
        lin_gn0 = lin_gn

        th_gn0 = th_gn
        
        ic_gn0 = ic_gn
    else:
         print("No division event detected at gen(%d)" %(g))
        
sys.exit("Finishing simulation...")            

