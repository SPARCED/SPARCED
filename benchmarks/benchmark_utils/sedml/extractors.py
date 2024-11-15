#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
script name: extractors.py
Created on Mon. Oct. 28th 23:15 2024
Author: Jonah R. Huggins

Description: Series of functions for extracting details critical towards \
constructing a SED-ML file from PEtab files.

Output: 

"""
# ------------------------------package import----------------------------------#
import pandas as pd
import libsbml


def extract_simulation_times(condition_id, measurements_df) -> dict:
    """
    Extracts the start and end times for a particular simulation condition.

    Parameters
    - condition_id (str): The ID of the simulation condition.
    - measurements_df (pd.DataFrame): The measurements dataframe.

    Returns
    - initial_time (float): The initial time of the simulation.
    - output_start_time (float): The time at which the output starts.
    - output_end_time (float): The end time of the simulation.
    - number_of_steps (int): The number of steps in the simulation.

    TODO: Add functionality for preequilibration being treated as\
          output_start_time.
    """

    # Extract initial time
    timepoints = measurements_df["time"][
        measurements_df["simulationConditionId"] == condition_id
    ].unique()

    initial_time = timepoints.min()

    output_start_time = timepoints.min()

    output_end_time = timepoints.max()

    number_of_steps = len(timepoints)

    return {
        "initialTime": initial_time,
        "outputStartTime": output_start_time,
        "outputEndTime": output_end_time,
        "numberOfSteps": number_of_steps,
    }


def get_model_id(sbml_file) -> str:
    """
    Extracts the metaid of the model from the SBML file.

    Parameters
    - sbml_file (str): The path to the SBML file.

    Returns
    - metaid (str): The metaid of the model.
    """
    reader = libsbml.SBMLReader()
    document = reader.readSBML(sbml_file)
    model = document.getModel()

    return model.getId()


def extract_data(measurements_df: pd.DataFrame) -> dict:
    """
    Extracts the condition- and observable matched data from the measurements \
    dataframe.

    Parameters
    - measurements_df (pd.DataFrame): The measurements dataframe.

    Returns
    - data_dict (dict): A dictionary of the data extracted from the \
    measurements dataframe.
    """

    data_dict = {}

    for _, measurement in measurements_df.iterrows():
        condition_id = measurement["simulationConditionId"]
        observable_id = measurement["observableId"]
        time = measurement["time"]
        value = measurement["measurement"]

        if condition_id not in data_dict:

            data_dict[condition_id] = {}

        if observable_id not in data_dict[condition_id].keys():
            data_dict[condition_id][observable_id] = []

        data_dict[condition_id][observable_id].append((time, value))

    return data_dict


# ------------------------------end of script----------------------------------#
