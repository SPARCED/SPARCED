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
        for condition in self.data:
            time_of_death[condition] = []
            for cell in self.data[condition]:
                dead_simulation = np.array(self.data[condition][cell][self.observable_name]['toutS']\
                                           [self.data[condition][cell][self.observable_name]['xoutS'] > 100.0])
                if dead_simulation.size > 0:
                    dead_simulation_times = dead_simulation[0]             
                    time_of_death[condition].extend(dead_simulation_times.flatten().tolist())
                else:
                    time_of_death[condition].append(np.nan)
        return time_of_death
    

    def average_time_to_death(self):   
        """"Returns the time for the average simulated cell death for each condition in the results dictionary
        
        output: dictionary containing the average time to death for each condition"""

        time_of_death = self.time_to_death()
        for condition, cell_times in self.time_to_death().items():
            time_of_death[condition] = np.mean([time for time in time_of_death[condition] if time is not None])

        return time_of_death


    def death_ratio(self, percent:Optional[bool] = False):
        """Returns the ratio of dead cells, should be proceeded by collect_the_dead function
        time_to_death: dictionary containing the times to death for each cell per condition from the time_to_death function

        output: dictionary containing the ratio of dead cells for each condition"""

        dead_cells = {}
        for condition, cell_times in self.time_to_death().items():
            dead_cells[condition] = 0
            total_cells = len(self.data[condition])
            dead_cells[condition] += sum(1 for time in cell_times if time is not np.nan)
            # dead_cells[condition] = [dead_cells[condition] * (1 / total_cells) if total_cells !=0 else None for condition in dead_cells]
            dead_cells[condition] = dead_cells[condition] / total_cells if total_cells != 0 else None
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
        # alive_ratio = [(1 - x)*100 for x in death_ratio.values()]
        return alive_ratio 