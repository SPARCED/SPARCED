#!/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thurs. 05/16/2024 10:45:00 - JRH

Script defining the arguements for the model-benchmark comparison to prior
validated results of the SPARCED model.
"""

# -----------------------Package Import & Defined Arguements-------------------#
import argparse
import os

wd = os.path.dirname(os.path.abspath(__file__))

sparced_root = "/".join(
    wd.split(os.path.sep)[: wd.split(os.path.sep).index("SPARCED") + 1]
)

benchmarks = [
    "BIM-dependent-ERK-inhibition.yml",
    "TRAIL-percent-death.yml",
    "etoposide-induced-cell-death.yml",
    "proliferation-growth.yml",
    "DNA-repair.yml",
    "TRAIL_time-to-death.yml",
    "inhibition-of-stochastic-apoptosis.yml",
    "receptor-ligand_cooperativity.yml",
    "ERK-AKT-dose-response.yml",
    "regulation-of-stochastic-proliferation.yml",
    "IFNg-pulse-response.yml",
    "ribosome-doubling-rate.yml",
    "LINCS-RPPA-Abundance.yml",
    "stochastic-expression.yml",
    "cell_cycle.yml",
    "p53-dynamics.yml",
    "survival-signalling.yml",
]


def parse_args():
    """Retrieve and parse arguments necessary for model creation
    Inputs:
        None

    Returns:
        A namespace populated with all the attributes.
    """

    parser = argparse.ArgumentParser(
        description="Provide arguments to build the SPARCED model"
    )
    parser.add_argument(
        "--observable",
        required=False,
        type=int,
        help="only the observable in observables.tsv is \
                            calculated (1) or if the entire simulation is \
                                saved (0)",
        default=1,
    )

    parser.add_argument(
        "--results",
        "-r",
        required=False,
        type=str,
        help="the name of the file to save the results",
        default=None,
    )

    parser.add_argument(
        "--model",
        "-m",
        required=False,
        type=str,
        help="path to the model dirctory \
                        to be used for unit testing",
        default=(os.path.join(sparced_root, "SPARCED/models/SPARCED_standard")),
    )

    parser.add_argument(
        "--benchmark",
        "-b",
        required=False, # False enables SPARCED model to be easily tested against all
        type=str,
        help=f"Path to yaml file of benchmark to be used. \
                            Options include: {benchmarks}",
        default="stochastic-expression",
    )

    parser.add_argument(
        "--cores",
        "-c",
        required=False,
        type=int,
        help="Number of cores you which to use \
                            for a parallel process",
        default=1,
    )

    parser.add_argument(
        "--benchmark_description",
        "-bd",
        required=False,
        type=str,
        help="Description of the benchmark",
        default=None,
    )

    return parser.parse_args()
