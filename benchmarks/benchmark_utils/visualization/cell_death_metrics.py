#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
script name: cell_death_metrics.py
Created on April 24 18:00:00 2024
Author: Jonah R. Huggins

Description: This script is designed as a helper script to visualizations
             for population dynamics in the SPARCED model.

Output: Metrics used for calculating the death of cells in the simulation

"""
#-----------------------Package Import & Defined Arguements-------------------#

import numpy as np
from typing import Optional

class CellDeathMetrics:
    def __init__(self, data, observable_name):
        """ This is extended functionality for the observable calculator class. 
        It is designed to calculate different death point metrics for each cell in the simulation results.

        data: dictionary containing the simulation results from ObservableCalculator
        observable_name: name of the observable to be used to determine time of death
        """
        self.data = data
        self.observable_name = observable_name


    def time_to_death(self):
        """"Returns the time for each simulated cell death for each condition in the results dictionary
        
        output: dictionary containing the times to death for each cell per condition"""

        time_of_death = {}
        for entry in self.data:
            time_of_death[entry] = {}
            time_of_death[entry]['value'] = []

            # Definition point for a dead cell
            dead_simulation = np.array(self.data[entry]['toutS']\
                                        [self.data[entry][f'{self.observable_name}'] > 100.0])
            
            if dead_simulation.size > 0:
                dead_simulation_times = dead_simulation[0] # Grabs first instance of dead cell
                # sends the time of death to the value list.
                time_of_death[entry]['value'].extend(dead_simulation_times.flatten().tolist())
                

            else:
                time_of_death[entry]['value'].append(np.nan)

            time_of_death[entry]['conditionId'] = self.data[entry]['conditionId']
            time_of_death[entry]['cell'] = self.data[entry]['cell']

        # Final time of death variable contains len(data.keys()) matching entries
        # each with the corresponding conditionId and cell number, as well as the 
        # time in which they died. 
        return time_of_death
    

    def average_time_to_death(self):
        """Returns the average time to death for each condition in the results dictionary
        
        output: dictionary containing the average time to death for each condition"""

        time_of_death = self.time_to_death()

        condition_averaged_times = {}

        for entry in time_of_death:
            condition = entry['conditionId']
            time = entry['value']
            if condition not in condition_averaged_times:
                condition_averaged_times[condition] = []
            
            condition_averaged_times[condition].append(time)

        for condition, times in condition_averaged_times.items():
            condition_averaged_times[condition] = np.mean(times)
        
        return condition_averaged_times


    def death_ratio(self, percent:Optional[bool] = False):
        """ Returns the ratio of dead cells for each condition in the results\
              dictionary
        Parameters:
        - time_to_death (dict): dictionary containing the times to death for \
            each cell per condition from the time_to_death function

        Returns:    
        - dead_cells (dict): dictionary containing the ratio of dead cells for \
            each condition"""

        dead_cells = {}

        cells_per_condition = {}
        for entry, entry_info in self.time_to_death().items():
            condition = entry_info['conditionId']
            if condition not in dead_cells:
                dead_cells[condition] = 0

            if entry_info['value'][0] is not np.nan:
                dead_cells[condition] += 1

            if condition not in cells_per_condition:
                cells_per_condition[condition] = 0
            cells_per_condition[condition] += 1

        for condition, dead_count in dead_cells.items():
            dead_cells[condition] = dead_count / cells_per_condition[condition]
            if percent:
                dead_cells[condition] = dead_cells[condition] * 100

        return dead_cells
    
    
    def alive_ratio(self, percent:Optional[bool] = False):
        """Returns the ratio of alive cells, should be proceeded by collect_the_dead function
        
        output: dictionary containing the ratio of alive cells for each condition"""

        death_ratio = self.death_ratio()
        if percent == True:
            alive_ratio = [(1 - x)*100 for x in death_ratio.values()]
        else:
            alive_ratio = [(1 - x) for x in death_ratio.values()]

        return alive_ratio 
    

