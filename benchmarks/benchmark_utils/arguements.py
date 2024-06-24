import argparse
import os


wd = os.path.dirname(os.path.abspath(__file__))

sparced_root = ('/'.join(wd.split(os.path.sep)[:wd.split(os.path.sep)
                                              .index('SPARCED')+1]))

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
                        required = True, 
                        type=str, 
                        help='path to the model dirctory \
                        to be used for unit testing', 
                        default=(os.path.join(sparced_root, 
                                            'SPARCED/models/SPARCED_standard')))
    
    parser.add_argument('--benchmark', '-b', 
                        required = False, 
                        type=str,
                        help='benchmark to evaluate the model against',
                        default='stochastic-expression')
    
    parser.add_argument('--cores', '-c', 
                        required=False, 
                        type=int,
                        help='Number of cores you which to use \
                            for a parallel process', 
                        default= 1)
    
    return (parser.parse_args())