#!/usr/bin/env python
# -*- coding: utf-8 -*-

from typing import IO

import numpy as np
import pandas as pd
import re

import SparcedModel

from utils.data_handling import load_input_data_file


def antimony_write_constant_variables(f_antimony: IO[str], constants: np.ndarray) -> None:
    """Write constant variables in the given Antimony file

    Arguments:
        f_antimony: The open Antimony file.
        constants: The constant variables to declare.

    Returns:
        Nothing.
    """

    f_antimony.write("# Other declarations:\nconst ")
    for const_var in constants[:-1]:
        f_antimony.write("{name}, ".format(name=const_var))
    f_antimony.write("{last_name};\n\n".format(last_name=constants[-1]))

def antimony_write_compartments_names(file: IO[str], compartments: dict[str, str]) -> None:
    """Write compartments names in the given Antimony file

    Note:
        The dictionnary is structured as key: compartment name / value:
        compartment volume.

    Arguments:
        file: The open Antimony file.
        compartments: Content of the input compartments file structured
                      as a dictionnary. For further details, see the
                      __Note__ section.

    Returns:
        Nothing.
    """

    file.write("# Compartments:\n")
    for k in compartments.keys():
        file.write(f"Compartment {k}; ")
    file.write("\n")

def antimony_write_reaction(f_antimony: IO[str], model: SparcedModel.Model) -> None:
    """Write SparcedModel.Model reactions into an Antimony file

    Arguments:
        f_antimony: The open Antimony file.
        model: A SpacedModel.Model.

    Returns:
        A tuple with the parameters' names list and the parameters' values list.
    """

    f_antimony.write("# Reactions:\n")
    # Ratelaws
    ratelaw_sheet = load_input_data_file(model.compilation_files['ratelaws'])
    ratelaws = np.array([line[1:] for line in ratelaw_sheet[1:]], dtype="object")
    ratelaws_ids = np.array([line[0] for line in ratelaw_sheet[1:]], dtype="object")
    # Parameters
    param_names = []
    param_values = []
    param_reaction_ids = []
    param_nbs = []
    for row_nb, reaction in enumerate(ratelaws):
    # Read reaction's species (reactants and products)
    all_reactants = []
    all_products = []
    formula = f"k{row_nb + 1}*"
    if ';' in ratelaw[1]:
        # Reaction is written under the format "reactants ; products"
        raw_reaction = reaction[1].split(';')
        if len(raw_reaction) > 2:
            raise RuntimeError("Reaction has species that do not belong to reactants nor to products.")
        # Reactants and products are written under the format "A + B + C..."
        reactants = raw_reaction[0].split('+')
        products = raw_reaction[1].split('+')
        for r in reactants:
            r = r.strip()
            if r:
                all_reactants.append(r)
                formula += f"{r}*"
        for p in products:
            p = p.strip()
            if p:
                all_products.append(p)
    # Read reaction's rate
    # Mass-action formula
    if 'k' not in reaction[2]:
        formula = formula[:-1]
        param_names.append(f'k{row_nb+1}')
        param_values.append(np.double(reaction[2]))
        param_reaction_ids(ratelaws_ids[row_nb])
        param_nbs.append(int(0))
    # Specified formula (non mass-action)
    else:
        formula = reaction[2]







 else:
        # specific formula (non-mass-action)
        formula = ratelaw[2]
        j = 1
        params = np.genfromtxt(ratelaw[3:], float) # parameters
        params = params[~np.isnan(params)]
        if len(params) == 1:
            paramnames.append("k"+str(rowNum+1)+"_"+str(j))
            paramvals.append(float(ratelaw[j+2]))
            paramrxns.append(ratelaw_sheet[rowNum+1][0])
            paramidxs.append(int(0))
            pattern = 'k\D*\d*'
            compiled = re.compile(pattern)
            matches = compiled.finditer(formula)
            for ematch in matches:
                formula = formula.replace(ematch.group(),paramnames[-1])



        else:
            # specific formula (non-mass-action)
            formula = ratelaw[1]
            j = 1
            params = np.genfromtxt(ratelaw[2:], float) # parameters
            params = params[~np.isnan(params)]
            if len(params) == 1:
                paramnames.append("k"+str(rowNum+1)+"_"+str(j))
                paramvals.append(float(ratelaw[j+1]))
                paramrxns.append(ratelaw_sheet[rowNum+1][0])
                paramidxs.append(int(0))
                pattern = 'k\D*\d*'
                compiled = re.compile(pattern)
                matches = compiled.finditer(formula)
                for ematch in matches:
                    formula = formula.replace(ematch.group(),paramnames[-1])
            else:
                for q,p in enumerate(params):
                    paramnames.append("k"+str(rowNum+1)+"_"+str(j))
                    paramvals.append(float(ratelaw[j+1]))
                    paramrxns.append(ratelaw_sheet[rowNum+1][0])
                    paramidxs.append(q)
                    pattern1 = 'k(\D*)\d*'+'_'+str(j)
                    compiled1 = re.compile(pattern1)
                    matches1 = compiled1.finditer(formula)
                    for ematch in matches1:
                        formula = formula.replace(ematch.group(),paramnames[-1])
                    j +=1
        if ratelaw[0] == 'Cytoplasm':
            valcomp = 5.25e-12
        elif ratelaw[0] == 'Extracellular':
            valcomp = 5.00e-5
        elif ratelaw[0] == 'Nucleus':
            valcomp = 1.75e-12
        elif ratelaw[0] == 'Mitochondrion':
            valcomp = 3.675e-13
        #don't include reactions without products or reactants
        if products == [] and reactants == []:
            pass
        else:
             f.write("  %s: %s => %s; (%s)*%.6e;\n" % (stoic_columnnames[rowNum], " + ".join(reactants), " + ".join(products), formula, valcomp))
    
    # Export parameters for each reaction, with corresponding order within the ratelaw and its value
    params_all = pd.DataFrame({'value':paramvals,'rxn':paramrxns,'idx':paramidxs},index=paramnames)
    params_all.to_csv(f_outp,sep='\t',header=True, index=True)
    # ========== END OF COPY/PASTE ==========
    f.write("\n")
    return((paramnames, paramvals))

def antimony_write_species_names(f_antimony: IO[str], species: np.ndarray) -> None:
    """Write species names and affiliated compartments in the given Antimony file

    Note:
        The first row is considered as a header, and hence it is skipped.
        Species names should be located on the first column of the array.
        Species compartments should be located on the second column of the array.

    Argurments:
        f_antimony: The open Antimony file.
        species: Content of the input species file.

    Returns:
        Nothing.
    """

    f_antimony.write("# Species:\n")
    for i, value in enumerate(species[1:]):
         f_antimony.write("Species {name} in {compartment};\n"
                          .format(name=value[0], compartment=value[1]))
    f_antimony.write("\n")

def antimony_write_unit_definitions(f_antimony: IO[str]) -> None:
    """Write unit definitions in the given Antimony file

    Warning:
        This function contains hard-coded values

    Arguments:
        f_antimony: The open Antimony file.

    Returns:
        Nothing.
    """

    f_antimony.write("# Unit definitions:\n")
    f_antimony.write("  unit time_unit = second;\n")
    f_antimony.write("  unit volume = litre;\n")
    f_antimony.write("  unit substance = 1e-9 mole;\n")
    f_antimony.write("  unit nM = 1e-9 mole / litre;\n\n")

