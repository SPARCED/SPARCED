#!/usr/bin/env python
# -*- coding: utf-8 -*-


# AMICI
AMICI_FOLDER_PREFIX = "amici_"

# ANTIMONY
ANTIMONY_FILE_PREFIX = "ant_"
ANTIMONY_FILE_SUFFIX = ".txt"
ANTIMONY_HEADER = "Erdem et al., Nat Commun 2022"  # TODO: Move to YAML

# DEFAULT GENERAL VALUES
DEFAULT_CONFIG_FILE = "config.yaml"
DEFAULT_CONFIG_FILES_EXTENSION = ".yaml"
DEFAULT_MODEL_NAME = "SPARCED_standard"
DEFAULT_MODELS_DIRECTORY = "./../models/"

# OUTPUT
DEFAULT_OUTPUT_FILE_EXTENSION = ".txt"

# SBML
SBML_FILE_PREFIX = "sbml_"
SBML_FILE_SUFFIX = ".xml"

# UNITS
UNIT_DEF_NM = "1e-9 mole / litre"
UNIT_SUBSTANCE = "1e-9 mole"
UNIT_TIME = "second"
UNIT_VOLUME = "litre"

# YAML (main configuration file)
YAML_DATA_LOCATION = "location"
# Compilation keywords
YAML_COMPILATION_DATA_LOCATION = "directory"
YAML_COMPILATION_FILES = "files"
YAML_COMPILATION_KEYWORD = "compilation"
# -- Input files keywords
YAML_COMPARTMENTS = "compartments"
YAML_OUTPUT_PARAMETERS = "output_parameters"
YAML_RATELAWS = "ratelaws"
YAML_SPECIES = "species"
# Experiment keywords
YAML_EXPERIMENT_DATA_LOCATION = "directory"
YAML_EXPERIMENT_KEYWORD = "experiments"
YAML_EXPERIMENT_NAME = "name"
# Simulation keywords
YAML_SIMULATION_DATA_LOCATION = "directory"
YAML_SIMULATION_FILES = "files"
YAML_SIMULATION_KEYWORD = "simulation"
# -- Input files keywords
YAML_GENES_REGULATION = "genes_regulation"
YAML_OMICS_DATA = "omics"

# YAML (experiment configuration file)
YAML_EXPERIMENT_EXCHANGE = "exchange"
YAML_EXPERIMENT_NB_REPLICATES = "population_size"
YAML_EXPERIMENT_OUTPUT_DIRECTORY = "output_directory"
YAML_EXPERIMENT_PROTOCOL = "protocol"
YAML_EXPERIMENT_STAMP_OUTPUT = "stamp"
YAML_EXPERIMENT_VERBOSE = "verbose"
# -- Protocol settings
YAML_PROTOCOL_DURATION = "duration"
YAML_PROTOCOL_IS_DETERMINISTIC = "deterministic"
YAML_PROTOCOL_NAME = "name"
YAML_PROTOCOL_PERTURBATIONS = "perturbations"
YAML_PROTOCOL_PERTURBATIONS_ID = "perturbations_id"
