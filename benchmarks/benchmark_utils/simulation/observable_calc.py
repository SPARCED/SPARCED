#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
script name: Observable_calc.py
Created on Fri April 24 18:00:00 2024
Author: Jonah R. Huggins

Description: This script is designed to calculate observable values from 
             simulation results.

Output: dictionary containing the observables of interest

"""
#-----------------------Package Import & Defined Arguements-------------------#

import re
import numpy as np
import pandas as pd
from typing import Optional


class ObservableCalculator:
    def __init__(self, yaml_file:str, results_dict: dict, 
                 observable_df: pd.DataFrame, measurement_df: pd.DataFrame, 
                 model: str):
        """This class is designed to calculate observable values from simulation results.
        input:
            yaml_file: str - path to the YAML file
            results_dict: dict - dictionary containing the simulation results
            observable_df: str - path to the observable dataframe
            model: libSBML model - the model used for the simulation
        """
        self.yaml_file = yaml_file
        self.results_dict = results_dict
        self.observable_df = observable_df
        self.measurement_df = measurement_df
        self.model = model


    def __call__(self):
        """isolate only the observables of interest from the simulation data. Primary function is to cut down on data.

        output: dictionary containing the observables of interest"""

        species_ids = list(self.model.getStateIds()) # assign species IDs to a list

        observable_dict = {} # Instantiate the observable dictionary, dictionary structure will be condition -> cell -> observable -> xoutS, toutS, xoutG
        for condition in self.results_dict:
            observable_dict[condition] = {} # Instatiate the condition dictionary
            for cell in self.results_dict[condition]:
                observable_dict[condition][cell] = {} # Instantiate the cell dictionary
                for _, observable in self.observable_df.iterrows():
                    observable_formula = str(observable['observableFormula'])
                        # Search the obs formula for species names
                        # species = re.findall(r'\b\w+(?:\.\w+)?\*\w+(?:\.\w+)?\b', obs_formula)
                    species = re.findall(r'\b[A-Za-z](?:[A-Za-z0-9_]*[A-Za-z0-9])?\b', observable_formula)
                    for species_i in species:
                        # Construct the regex pattern to match the species name exactly
                        pattern = r'\b{}\b'.format(re.escape(species_i))
        #                 # Replace only the exact matches of the species name in the formula
                        observable_formula = re.sub(pattern, f'self.results_dict[condition]["{cell}"]["xoutS"][:, species_ids.index("{species_i}")]', observable_formula)

                    obs = eval(observable_formula)

                    observable_name = observable['observableId']
                    observable_dict[condition][cell][observable_name] = {}
                    observable_dict[condition][cell][observable_name]['xoutS'] = obs
                    observable_dict[condition][cell][observable_name]['toutS'] = self.results_dict[condition][cell]['toutS']
                    if 'xoutG' in self.results_dict[condition][cell]:
                        observable_dict[condition][cell][observable_name]['xoutG'] = self.results_dict[condition][cell]['xoutG']

        return observable_dict

    def _sum_unique_dict_entries(self):
        """Sum the unique entries in the results dictionary."""
        unique_entries = {}
        for key, value in self.results_dict.items():
            unique_entries[f'{key}'] = []
            for sub_key, sub_value in value.items():
                unique_entries[f'{key}'].append(1)
            unique_entries[f'{key}'] =  sum(unique_entries[f'{key}'])
        return unique_entries
    
    def _add_experimental_data(self, observable_dict: dict):
        """
        Returns a dictionary of experimental data for each observable and condition,
        matching simulation results dictionary format.

        Parameters:
        - yaml_file (str): Path to the yaml file.

        Returns:
        - result_dict (dict): Dictionary containing experimental data.
        """

        result_dict = observable_dict
        if 'preequilibrationConditionId' in self.measurement_df.columns:
            no_preequilibrations_df = (self.measurement_df.drop(
                self.measurement_df[self.measurement_df['simulationConditionId'] == self.measurement_df['preequilibrationConditionId']].index))

            # Group by observableId and simulationConditionId
            grouped_data = no_preequilibrations_df.groupby(['observableId', 'simulationConditionId'])
        else:
            grouped_data = self.measurement_df.groupby(['observableId', 'simulationConditionId'])
            
        # look for experimental data in the measurements file by exculding all NaN values in measurement_df['measurement']
        # if all values are NaN, then there is no experimental data to compare to
        if self.measurement_df['measurement'].isna().all():
            print('No experimental data to compare to')
            return observable_dict

        for (observable, condition), condition_data in grouped_data:
            for cell in result_dict[condition]:
                result_dict[condition][cell][f'experiment {observable}'] = {}
            for i in range(0, self._sum_unique_dict_entries()[condition]):
                result_dict[condition][f'cell {i}'][f'experiment {observable}']['toutS'] = condition_data['time'].values
                result_dict[condition][f'cell {i}'][f'experiment {observable}']['xoutS'] = condition_data['measurement'].values
        
        return result_dict
