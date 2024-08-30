
# -*- coding: utf-8 -*-
#!/usr/bin/env python     
"""
Created on Thurs. 05/16/2024 10:45:00 - JRH

Script to automate model-benchmark comparison to prior validated results of
the SPARCED model.

Provide a path to the model directory and the script will run all benchmarks, 
outputing visual results to a 'results' directory within the model directory 
for anlysis. 

Users are anticipated to compare simulation results to prior validated results.
"""

#-----------------------Package Import & Defined Arguements-------------------#
import os
from arguements import parse_args
import subprocess, sys

# Parse the arguements
args = parse_args()

# Check if the model directory was provided
try:
    assert args.model is not None
except:
    print("Please provide a path to the model directory")
    sys.exit(1)

try:
    assert args.cores is not None
except:
    print ("Number of cores is not assigned, defaulting to 1")

#-----------------------Function to Run All Benchmarks-------------------------#
def run_all_benchmarks(model_path: str | os.PathLike) -> None:
    """
    Run all benchmarks in the benchmarks directory
    Input:
        Model: Path to the model directory

    Output:
        simulation results for all benchmarks to a 'results' directory
        within the model directory
    """

    os.chdir('..')

    benchmarks = _get_list_of_benchmarks()

    for benchmark in benchmarks:

        # Run the benchmark
        print(f"Running benchmark {benchmark}")

        Command = f"mpiexec -n {args.cores} python __main__.py \
                -m {model_path} -b {benchmark}"

        try: 
            result = subprocess.run(Command, shell=True, check=True, 
                                    #stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                                    capture_output=True, text=True)
            print("Command output:", result.stdout)
            print("Command error:", result.stderr)
        
        except subprocess.CalledProcessError as e:
            print("Command failed with exit status", e.returncode)
            print("Error output:", e.stderr)

        subprocess.run(Command, shell=True, check=True, 
                       stdout=subprocess.PIPE, stderr=subprocess.PIPE)


def _get_list_of_benchmarks() -> list:
    """ Return a list of all benchmarks to be run. Users defining new 
        benchmarks should add them to this list.
    Inputs:
        None

    Returns:
        A list of all benchmarks to be run: list of strings
    
    """
    return ["BIM-dependent-ERK-inhibition", 
            "TRAIL-percent-death", 
            "etoposide-induced-cell-death", 
            "proliferation-growth", 
            "DNA-repair", 
            "TRAIL_time-to-death",
            "LINCS-RPPA-Abundance",
            "inhibition-of-stochastic-apoptosis",
            "stochastic-expression",
            "receptor-ligand_cooperativity", 
            "cell_cycle", 
            "p53-dynamics", 
            "ERK-AKT-dose-response", 
            "regulation-of-stochastic-proliferation", 
            "IFNg-pulse-response",
            "ribosome-doubling-rate",
            "survival-signalling"]


#-----------------------Run All Benchmarks------------------------------------#
if __name__ == '__main__':
    run_all_benchmarks(args.model)


