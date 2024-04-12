#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys

import amici
from antimony import *
import libsbml

from compilation.utils import *
from compilation.utils.amici_scripts.amici_utils import define_observables
from compilation.utils.antimony_scripts.model_writing import antimony_write_model
from compilation.utils.sbml_scripts.model_annotation import sbml_annotate_model


def create_model(f_observables, model_name, f_compartments, f_stoichmatrix,
                 output_dir_path, f_output_parameters, f_ratelaws, f_species,
                 verbose, is_SPARCED):

    """
    Generate Antimony, SBML and AMICI models based on given input data
    
    :param f_observables: path to the observables file
    :type f_observables: [str]
    :param model_name: desired name for the generated Antimony, SBML and AMICI models
    :type model_name: [str]
    :param f_compartments: path to the compartments & volumes file
    :type f_compartments: [str]
    :param f_stoichmatrix: path to the stoichiometric matrix file
    :type f_stoichmatrix: [str]
    :param f_output_dir_path: path to the desired output directory
    :type f_output_dir_path: [str]
    :param f_output_parameters: path to the output parameters file
    :type f_output_parameters: [str]
    :param f_ratelaws: path to the ratelaws file
    :param f_ratelaws: [str]
    :param f_species: path to the species file
    :type f_species: [str]
    :param verbose: verbose
    :type verbose: [bool]
    :param is_SPARCED: activate hard-coded behaviors for SPARCED
    :type is_SPARCED: [bool]
    :return: Nothing TODO change this
    :rtype: [void]

    """
    # ------------------------------- ANTIMONY --------------------------------
    # Create and load an Antimony model
    antimony_file_name, compartments, species, compartments_full = \
            antimony_write_model(model_name, output_dir_path, f_compartments,
                                 f_stoichmatrix, f_output_parameters,
                                 f_ratelaws, f_species, is_SPARCED)
    try:
        assert not loadFile(antimony_file_name) == -1
    except:
        print("{name}: Failed to load Antimony file".format(name=model_name))
        sys.exit(0)
    else:
        if verbose: print("{name}: Success loading Antimony file"
                         .format(name=model_name))
    # --------------------------------- SBML ----------------------------------
    # Convert the newly created Antimony model into an SBML model
    sbml_file_name = output_dir_path + "sbml_" + model_name + ".xml"
    try:
        assert not writeSBMLFile(sbml_file_name, model_name) == 0
    except:
        print("{name}: Failed to convert Antimony file to SBML"
             .format(name=model_name))
        sys.exit(0)
    else:
        if verbose: print("{name}: Success converting Antimony file to SBML"
                         .format(name=model_name))
    # Annotate the SBML model
    sbml_annotate_model(sbml_file_name, species, compartments_full)
    # --------------------------------- AMICI ---------------------------------
    # Import
    sbml_reader = libsbml.SBMLReader()
    sbml_doc = sbml_reader.readSBML(sbml_file_name)
    sbml_model = sbml_doc.getModel()
    sbml_importer = amici.SbmlImporter(sbml_file_name)
    # Set all the rate parameters as constant (faster compilation)
    const_params = [params.getId() \
                    for params in sbml_model.getListOfParameters()]
    # Create Observables
    # observables = define_observables(f_observables, compartments_full, species) 
    # Compile
    model_output_dir = output_dir_path + "amici_" + model_name
    # TODO: add observables and constant parameters (currently broken also in
    # the original script actually)
    sbml_importer.sbml2amici(model_name, model_output_dir, verbose=verbose)
    if verbose: print("{name}: Sucess compiling the model"
                     .format(name=model_name))

def launch_model_creation():
    """
    Small routine to process parsed arguments and call create_model
    """
    args = parse_args()
    # Process arguments
    is_SPARCED = not args.wild  # if it's not wild then it's SPARCED
    # Add path of input directory to input files names                          
    f_observables = args.inputdir + args.observables
    f_compartments = args.inputdir + args.compartments                          
    f_stoichmatrix = args.inputdir + args.stoichmatrix                          
    f_output_params = args.inputdir + args.outputparams                         
    f_ratelaws = args.inputdir + args.ratelaws                                  
    f_species = args.inputdir + args.species                                    
    # Create model                                                              
    create_model(f_observables, args.name, f_compartments, f_stoichmatrix,
                 args.outputdir, f_output_params, f_ratelaws, f_species,
                 args.verbose, is_SPARCED)

if __name__ == '__main__':
    launch_model_creation()
