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

class ObservableCalculator:
    def __init__(self, yaml_file:str, results_dict: dict, 
                 observable_df: pd.DataFrame, measurement_df: pd.DataFrame, 
                 model: str):
        """This class is designed to calculate observable values from \
            simulation results.
            
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
        """isolate only the observables of interest from the simulation data. \
        Primary function is to cut down on data saved.

        Returns: modified results dictionary containing only the observables of 
        interest
        """
        observableIds = self.observable_df['observableId'].unique()

        observable_arrays = {}

        for item in self.results_dict:

            conditionId = item['conditionId']
            cell = item['cell']
            xoutS = item['xoutS']
            
            # if the conditionId and observable are matched in the 
            # measurement_df, add the observable to the interesting_observables 
            # list
            interesting_observables = []
            for observableId in observableIds:

                # calculate the observable values from the simulation results
                observable_array = self.observable_caluculator(observableId, xoutS)

                # add the observable to the observable_arrays dictionary
                observable_arrays[observableId] = observable_array

                # add the observable values to the results_dict if the 
                # observable is associated with the conditionId in the measurement_df
                if (
                    (
                        self.measurement_df['simulationConditionId']==conditionId
                        ).any() 
                        and (
                            self.measurement_df['observableId'] == observableId
                            ).any()
                    ):
                    
                    interesting_observables.append(observableId)

            # add the observable values to the results_dict
            for observable in interesting_observables:
                item[f'simulation {observable}'] = observable_arrays[observable]
        
            # remove the xoutS from the results_dict
            del item['xoutS']

        # add the experimental data to the results_dict
        for item in self.results_dict:
            item = self._add_experimental_data(item)

        # reduce timepoints in the simulation results to match the experimental 
        # data
        for item in self.results_dict:
            item['toutS'] = self._timepoint_reduction(item['toutS'])

        return self.results_dict


    def observable_caluculator(self, observable: str, 
                               xoutS: np.array)-> np.array:
        """Calculate the observable values from the simulation results.

        Parameters:
        - observable (str): The observable of interest. Should be a column in \
            the observable dataframe.
        - xoutS (np.array): The simulation results.
        Returns:
        - observable_array(np.array): Array containing the observable values.
        """
        try:
            assert (observable in self.observable_df['observableId'].values, 
            f'{observable} is not in the observable dataframe')

            species_ids = list(self.model.getStateIds())

            # replace species name strings in the observable_formula with the 
            # corresponding species index in the results_dict
            observable_formula = str(observable['observableFormula'])

            # Search the observable formula for species names
            species = re.findall(r'\b[A-Za-z](?:[A-Za-z0-9_]*[A-Za-z0-9])?\b', 
                                 observable_formula)
            
            for species_i in species:
                
                # Construct the regex pattern to match the species name exactly
                pattern = r'\b{}\b'.format(re.escape(species_i))

                # Replace only the exact matches of the species name in the formula
                observable_formula = (re.sub(pattern, 
                                             xoutS[:, species_ids.index("{species_i}")], 
                                             observable_formula))

            observable_answer = eval(observable_formula)

            return observable_answer

        except AssertionError as e:
            print(e)
            pass
    

    def _add_experimental_data(self, item: tuple)-> tuple:
        """
        Returns a dictionary of experimental data for each observable and condition,
        matching simulation results dictionary format.

        Parameters:
        - item (tuple): Tuple containing the simulation results for a \
            single condition.

        Returns:
        - item (tuple): Modified tuple containing the simulation results and \
            experimental data.
        """

        # Account for the preequilibration condition
        preequilibration_condition = (
            self.measurement_df.loc[
            self.measurement_df['simulationConditionId']==item['preequilibrationConditionId']
            ]
            )

        if not preequilibration_condition.empty:
            non_preequilibration_df = self.measurement_df.drop(preequilibration_condition.index)

        else:
            non_preequilibration_df = self.measurement_df

        # Group by observableId and simulationConditionId
        grouped_data = non_preequilibration_df.groupby(['observableId', 'simulationConditionId'])

        # look for experimental data in the measurements file by exculding all
        #  NaN values in measurement_df['measurement']
        if self.measurement_df['measurement'].isna().all():
            print('No experimental data to compare to')
            return item
        
        # Create a dictionary to store the experimental data
        item['experiment_data'] = {}

        # match the experimental data to the simulation results
        for (observableId, conditionId), group in grouped_data:
            
            measurements = group['measurement'].values

            item[f'experiment {observableId}'] = measurements

        return item


    def _timepoint_reduction(self, toutS: np.array)-> np.array:
        """Reduce the number of timepoints in the simulation results. to match
            the number of timepoints in the experimental data.
            
        Parameters:
        - toutS (np.array): The timepoints from the simulation results.

        Returns:
        - toutS (np.array): The reduced timepoints.
        """
        # Ensure first that there is no experimental values in the measurement
        # before reducing the timepoints, if none are found, return the original
        if self.measurement_df['measurement'].isna().all():
            return toutS

        # Find the minimum number of timepoints in the measurement data
        unique_timepoints = self.measurement_df['time'].unique()

        toutS = np.delete(toutS, np.where(toutS != unique_timepoints))
        
        return toutS