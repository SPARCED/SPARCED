#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
script name: sparced_simulation.py
Created on Thurs. 04/23/2024 9:00:00
Author: Jonah R. Huggins

Description: This file conducts user defined, condition-specific simulations \
using SPARCED and returns the results as nested NumPy arrays.

Output:
- xoutS_all (np.ndarray): The species concentrations at each timepoint
- tout_all (np.ndarray): The timepoints at which the species concentrations \
    were recorded
- xoutG_all (np.ndarray): The gene expression values at each timepoint

"""

# -----------------------Package Import & Defined Arguements-------------------#
import os
import sys
import math
import libsbml
import importlib
import numpy as np
import pandas as pd
from benchmark_utils.simulation.utils import Utils as utils

# Get the directory path
wd = os.path.dirname(os.path.abspath(__file__))
# Ensure the SPARCED root and bin directories are in the system path
sparced_root = "/".join(
    wd.split(os.path.sep)[: wd.split(os.path.sep).index("SPARCED") + 1]
)
sys.path.append(os.path.join(sparced_root, "SPARCED/src/"))
from simulation.modules.RunSPARCED import RunSPARCED


class Simulation:
    def __init__(
        self,
        yaml_file: str,
        conditions_df: pd.DataFrame,
        measurement_df: pd.DataFrame,
        parameters_df: pd.DataFrame,
        sbml_file: str,
    ):
        """This class is designed to simulate the experimental replicate model.
        input:
            yaml_file: str - path to the YAML file
            model: str - path to the SBML model
            conditions_df: pd.DataFrame - the conditions dataframe
            measurement_df: pd.DataFrame - the measurement dataframe
            parameters_df: pd.DataFrame - the parameters dataframe
            sbml_file: str - path to the SBML file
        """

        self.yaml_file = yaml_file
        self.conditions_df = conditions_df
        self.measurement_df = measurement_df
        self.parameters_df = parameters_df
        self.sbml_file = sbml_file

        # Load the SPARCED model
        self.model, self.f_genereg, self.f_omics = self.load_sparced_model()

    def run_single_simulation(self, condition: pd.Series) -> np.ndarray:
        """This function runs the simulation for a single condition.
        input:
            condition: pd.Series - the condition to simulate
        output:
            result: pd.DataFrame - the simulation results
        """

        # Look for heterogenize parameters in the condition
        if "heterogenize" in condition and not math.isnan(condition["heterogenize"]):
            self.model = self._heterogenize(condition)

        if "preequilibrationConditionId" in condition and not math.isnan(
            condition["preequilibrationConditionId"]
        ):
            self.model._preequilibrate(condition)

        species_ids = list(self.model.getStateIds())

        # # Set the perturbations for the simulation
        self.model, self.f_omics = self._set_perturbations(condition)

        # Set the timepoints for the simulation
        simulation_timeframe = self.measurement_df["time"][
            self.measurement_df["simulationConditionId"].isin(condition)
        ].max()

        self.model.setTimepoints(np.linspace(0, 30))

        # Find gene sampling method, flagD
        perturbations = list(self.conditions_df.columns[2:])
        if "flagD" in perturbations:
            flagD = condition["flagD"]
        else:
            flagD = 1

        # Run the simulation
        xoutS_all, xoutG_all, tout_all = RunSPARCED(
            flagD=flagD,
            th=(simulation_timeframe / 3600),
            spdata=[],
            genedata=[],
            sbml_file=self.sbml_file,
            model=self.model,
            f_genereg=self.f_genereg,
            f_omics=self.f_omics,
        )

        return xoutS_all, tout_all, xoutG_all

    def _preequilibrate(self, condition: pd.Series) -> pd.DataFrame:
        """This function assigns a set of conditions that replicate
        prior experimental conditions before the primary stimulus of
        interest.

        input:
            condition: pd.Series - the condition to simulate

        output:
            preequilibrated_model: pd.DataFrame - the preequilibrated model
        """

        # Isolate the preequilibration condition if included in the measurement
        # table
        preequilibrate_condition = (
            self.measurement_df.loc[
                self.measurement_df["simulationConditionId"]
                == condition["conditionId"],
                "preequilibrationConditionId",
            ]
            .dropna()
            .unique()
        )

        # account for no preequilibration condition being found
        if len(preequilibrate_condition) == 0:
            return self.model

        # set perturbations for the simulation
        self.model, self.f_omics = self._set_perturbations(condition)

        # Find gene sampling method, flagD
        flagD = self.conditions_df.loc[
            self.conditions_df["conditionId"] == preequilibrate_condition[0], "flagD"
        ].values[0]

        # Find the time frame for the preequilibration simulation
        simulation_timeframe = self.measurement_df["time"][
            self.measurement_df["preequilibrationConditionId"].isin(condition)
        ].max()

        species_initializations = np.array(self.model.getInitialStates())

        self.model.setTimepoints(np.linspace(0, 30))

        # Run the simulation
        xoutS_all, _, _ = RunSPARCED(
            flagD,
            simulation_timeframe,
            species_initializations,
            [],
            self.sbml_file,
            model=self.model,
            f_genereg=self.f_genereg,
            f_omics=self.f_omics,
        )

        # Return the final values
        self.model.setInitialStates(xoutS_all[-1])

        return self.model

    def _set_perturbations(self, condition: pd.Series) -> libsbml.Model:
        """This function sets the perturbations for the simulation.
        input:
            condition: pd.Series - the condition to simulate
        output:
            model: libsbml.Model - the updated SBML model
        """

        perturbations = list(self.conditions_df.columns[2:])

        for perturbant in perturbations:
            try:
                self.model = utils._set_species_value(
                    self.model, perturbant, condition[perturbant]
                )
            except:
                pass

            try:
                self.model = utils._set_parameter_value(
                    self.model, perturbant, condition[perturbant]
                )
            except:
                pass

            try:
                self.model = utils._set_compartmental_volume(
                    self.model, perturbant, condition[perturbant]
                )
            except:
                pass

            try:
                # Change the OmicsData values and save the prior values
                self.f_omics = utils._set_transcription_values(
                    omics_data=self.f_omics,
                    gene=perturbant,
                    value=condition[perturbant],
                )
            except:
                pass

        return self.model, self.f_omics

    def _heterogenize(self, condition: pd.Series) -> libsbml.Model:
        """This function runs the 'runSPARCED function and returns the final
        values, thus creating the simulated appearance of asynchrony among
        replicates.
        input:
            condition: pd.Series - the condition to simulate
        output:
            heterogenized_initial_values: pd.DataFrame - the heterogenized
            initial values
        """

        heterogenize = condition["heterogenize"]

        simulation_time = int(heterogenize) / 3600

        self.model.setTimepoints(np.linspace(0, 30))

        # TODO: Find a better mechanism for setting signaling ligands to 0
        growth_factors = ["E", "H", "HGF", "P", "F", "I", "INS"]

        for species in growth_factors:
            self.model = utils._set_species_value(self.model, species, 0)

        xoutS_all, _, _ = RunSPARCED(
            flagD=0,
            th=simulation_time,
            spdata=[],
            genedata=[],
            sbml_file=self.sbml_file,
            model=self.model,
            f_genereg=self.f_genereg,
            f_omics=self.f_omics,
        )

        self.model.setInitialStates(xoutS_all[-1])

        return self.model

    def load_sparced_model(self):
        """
        This function loads the SPARCED model.

        Parameters:
            None

        Returns:
        - model (libsbml.Model): The SBML model
        - genereg (pandas.DataFrame): The gene regulation pandas DataFrame
        - omicsdata (pandas.DataFrame): The OmicsData pandas DataFrame
        """
        # Create an instance of the AMICI model.
        sys.path.append(self.sbml_file)
        utils._add_amici_path(self.sbml_file)

        sparced = utils._swig_interface_path(self.sbml_file)
        sys.path.append(sparced)
        SPARCED = importlib.import_module(sparced.split("/")[-1].split(".")[0])
        model = SPARCED.getModel()
        solver = model.getSolver()
        solver.setMaxSteps = 1e10

        # Gene regulation and OmicsData files are used for stochastic gene
        # expression.
        genereg, omicsdata = utils._extract_simulation_files(self.sbml_file)

        return model, genereg, omicsdata
