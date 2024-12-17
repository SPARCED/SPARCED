#!/bin/bash python3
# -*- coding: utf-8 -*-

#------------------------------------------------------------------------------#
# script name: combine_results.py
# Author: Aurore Amrit & Jonah R. Huggins
# Created on: Tues. Dec. 10th, 2024

# Description: Script to concatenate the results of the SPARCED model into a single
# dataframe. This script is only compatible with the SPARCED model results.
#------------------------------------------------------------------------------#

import numpy as np
import pandas as pd

def combine_results(model, xoutS_all: np.ndarray, 
                    xoutG_all: np.ndarray, tout_all: np.ndarray) -> None:
    """
    Takes nested array results of genes, mRNA, proteins, and time values and 
    concatentates them into a single dataframe. 
    Parameters:
        - model: model object
        - xoutS_all (np.ndarray): array of species values
        - xoutG_all (np.ndarray): array of gene values
        - toutS_all (np.ndarray): array of time values
    Output:
        - pd.DataFrame: dataframe of concatenated results
    """
    # Create a dataframe to store the results
    sparced_results = pd.DataFrame(data = tout_all, columns = ['time'])

    # Get the gene and species names from the model
    species_names = model.getStateIds()
    gene_data = [x for n, x in enumerate(species_names) if 'm_' in x]

    # Add species to the results dictionary
    sparced_results = pd.concat([sparced_results, pd.DataFrame(data = xoutS_all, columns = species_names)], axis=1)

    # Add genes to the results dictionary
    gene_data = gene_data[1:] # Skip header
    resa = [sub.replace('m_', 'ag_') for sub in gene_data]
    resi = [sub.replace('m_', 'ig_') for sub in gene_data]
    gene_data2 = np.concatenate((resa, resi), axis=None)
    sparced_results = pd.concat([sparced_results, pd.DataFrame(data = xoutG_all, columns = gene_data2)], axis=1)
    return sparced_results
