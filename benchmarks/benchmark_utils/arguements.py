"""
Created on Thurs. 05/16/2024 10:45:00 - JRH

Script defining the arguements for the model-benchmark comparison to prior
validated results of the SPARCED model.
"""

#-----------------------Package Import & Defined Arguements-------------------#
import argparse
import os

wd = os.path.dirname(os.path.abspath(__file__))

sparced_root = ('/'.join(wd.split(os.path.sep)[:wd.split(os.path.sep)
                                              .index('SPARCED')+1]))

benchmarks = [
            "BIM-dependent-ERK-inhibition", "TRAIL-percent-death", "etoposide-induced-cell-death", 
            "proliferation-growth", "DNA-repair", "TRAIL_time-to-death", 
            "inhibition-of-stochastic-apoptosis", "receptor-ligand_cooperativity", 
            "ERK-AKT-dose-response", "regulation-of-stochastic-proliferation", "IFNg-pulse-response",
            "ribosome-doubling-rate", "LINCS-RPPA-Abundance", "stochastic-expression",
            "cell_cycle", "p53-dynamics", "survival-signalling"
]

def parse_args():
    """Retrieve and parse arguments necessary for model creation
    Inputs:
        None

    Returns:
        A namespace populated with all the attributes.
    """

    parser = argparse.ArgumentParser(
        description='Provide arguments to build the SPARCED model')
    parser.add_argument('--observable', 
                        required=False, 
                        type=int, 
                        help='only the observable in observables.tsv is \
                            calculated (1) or if the entire simulation is \
                                saved (0)', 
                        default=1)
    
    parser.add_argument('--name', '-n',
                        required=False, 
                        type=str, 
                        help='the name of the file to save the results', 
                        default=None)
    
    parser.add_argument('--model', '-m', 
                        required = False, 
                        type=str, 
                        help='path to the model dirctory \
                        to be used for unit testing', 
                        default=(os.path.join(sparced_root, 
                                            'SPARCED/models/SPARCED_standard')))
    
    parser.add_argument('--benchmark', '-b', 
                        required = False, 
                        type=str,
                        help=f'benchmark to evaluate the model against, \
                            options are {benchmarks}',
                        default='stochastic-expression')
    
    parser.add_argument('--cores', '-c', 
                        required=False, 
                        type=int,
                        help='Number of cores you which to use \
                            for a parallel process', 
                        default= 1)
    
    return (parser.parse_args())

