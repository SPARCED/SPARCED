#!/usr/bin/env python
# -*- coding: utf-8 -*-

import antimony

from compilation.utils.arguments import parse_args
from compilation.utils.antimony_scripts.antimony_utils import *


def antimony_write_model(model_name, output_dir_path, f_compartments,
                         f_stoichmatrix, f_output_parameters, f_ratelaws,
                         f_species, is_SPARCED):
    """
    Generate an Antimony file based on given data    
    :param model_name: name for the generated antimony model
    :type model_name: [str]
    :param f_compartments: compartments & volumes file
    :type f_compartments: [str]
    :param f_stoichmat: stoichiometric matrix file
    :type f_stoichmat: [str]
    :param f_output_params: output parameters file
    :type f_output_params: [str]
    :param f_ratelaws: ratelaws file
    :type f_ratelaws: [str]
    :param f_species: species file
    :param is_SPARCED: activate hard-coded behaviors of SPARCED
    !type is_SPARCED: [bool]
    :type f_species: [str]
    :return: The file name of the generated Antimony model + compartments and species
    :rtype: ([str], list[str], list[str])
    
    """
    antimony_file = output_dir_path + "ant_" + model_name + ".txt"

    with open(antimony_file,"w") as antimony_model:
        # Write file's header
        if (is_SPARCED):
            antimony_model.write("# PanCancer Model by Birtwistle Lab\n")
        antimony_model.write("model {antimony}()\n\n"
                            .format(antimony=model_name))
        # Write compartments, species and reactions
        compartments, volumes, species, sheet = antimony_init(f_compartments,
                                                              f_species)
        antimony_write_compartments(antimony_model,compartments)
        antimony_write_species(antimony_model,species)
        param_names, param_vals = antimony_write_reactions(antimony_model,
                                                           f_ratelaws,
                                                           f_stoichmatrix,
                                                           f_output_parameters)
        # Write initial conditions
        antimony_write_init_compartments(antimony_model,compartments,volumes)
        antimony_write_init_species(antimony_model,species)
        # Write reaction parameters
        antimony_write_init_reactions(antimony_model,param_names,param_vals)
        # Write other declarations and unit definitions
        antimony_terminal(antimony_model)
        antimony_model.write("\nend") 
    return(antimony_file, compartments, species, sheet)


if __name__ == '__main__':
    args = parse_args()
    # Add path of input directory to input files names
    f_compartments = args.inputdir + args.compartments
    f_stoichmatrix = args.inputdir + args.stoichmatrix
    f_output_params = args.inputdir + args.outputparams
    f_ratelaws = args.inputdir + args.ratelaws
    f_species = args.inputdir + args.species
    # Write model
    antimony_write_model(args.name, args.outputdir, f_compartments,
                         f_stoichmatrix, f_output_params, f_ratelaws, f_species)