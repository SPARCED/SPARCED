#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
script name: loader.py
Created on Fri Oct. 26th 23:15 2024
Author: Jonah R. Huggins

Description: Series of functions for loading PEtab files and extracting \
details critical towards constructing a SED-ML file from PEtab files.

Output: sbml model object -- model object from the SBML file
        parameter dataframe -- currently this is a clone of the \
        input_files/parameters.txt file
        conditions dataframe -- experimental conditions to be tested, \
        based on PEtab formatting
        measurement dataframe -- experimental measurements, linked by \
        observableId and conditionId, as well as simulation times
        observable dataframe -- details of the observables to be \
        tested, including the observableId, observableName, and \
            observableFormula
        model specifications dataframe -- details of the SPARCED model\
        specifications such as gene sampling method, \
        heterogeneous starting values, and the number \
        of cells to simulate.
        visualization dataframe -- details of the visualization \
        specifications, including the plotId, plotTypeSimulation, \
            xValues, and yValues

"""
# ------------------------------package import----------------------------------#
import os
import yaml
import pandas as pd


# Load the PEtab files
def file_loader(yaml_file: str):
    """
    returns: sbml model object -- model object from the SBML file
                parameter dataframe -- currently this is a clone of the \
                input_files/parameters.txt file
                conditions dataframe -- experimental conditions to be tested, \
                based on PEtab formatting
                measurement dataframe -- experimental measurements, linked by \
                observableId and conditionId, as well as simulation times
                observable dataframe -- details of the observables to be \
                tested, including the observableId, observableName, and \
                    observableFormula
                model specifications dataframe -- details of the SPARCED model\
                specifications such as gene sampling method, \
                heterogeneous starting values, and the number \
                of cells to simulate.
                visualization dataframe -- details of the visualization \
                specifications, including the plotId, plotTypeSimulation, \
                    xValues, and yValues
    """
    yaml_directory = os.path.join(os.path.dirname(yaml_file))

    with open(yaml_file, encoding="utf=8", mode="r") as file:
        yaml_dict = yaml.safe_load(file)

    # Construct full paths to petab files based on the YAML file's directory
    sbml_file = os.path.join(yaml_directory, yaml_dict["problems"][0]["sbml_files"][0])

    parameter_df = pd.read_csv(
        os.path.join(yaml_directory, yaml_dict["parameter_file"]), sep="\t"
    )
    conditions_df = pd.read_csv(
        os.path.join(yaml_directory, yaml_dict["problems"][0]["condition_files"][0]),
        sep="\t",
    )
    measurement_df = pd.read_csv(
        os.path.join(yaml_directory, yaml_dict["problems"][0]["measurement_files"][0]),
        sep="\t",
    )
    observable_df = pd.read_csv(
        os.path.join(yaml_directory, yaml_dict["problems"][0]["observable_files"][0]),
        sep="\t",
    )

    parent_obj = {
        "sbml file": sbml_file,
        "parameters": parameter_df,
        "conditions": conditions_df,
        "measurements": measurement_df,
        "observables": observable_df,
    }

    if "visualization_files" in yaml_dict["problems"][0]:
        visualization_df = pd.read_csv(
            os.path.join(
                yaml_directory, yaml_dict["problems"][0]["visualization_files"][0]
            ),
            sep="\t",
        )

        parent_obj["visualization"] = visualization_df

    return parent_obj
