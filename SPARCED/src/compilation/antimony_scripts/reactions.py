#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import re
from typing import IO

import numpy as np
import pandas as pd

from utils.data_handling import load_input_data_file


def read_reactions_species(reaction, formula):
    """
    Arguments:
        reaction:   The reaction description.
        formula:    The formula string.

    Returns:
        A tuple structured as (formula, reactants, products).
    """

    total_reactants = []
    total_products = []
    # Reaction is written under the format "reactants ; products"
    if ';' in reaction:
        split_reaction = reaction.split(';')
        if len(split_reaction) > 2:
            raise RuntimeError("Reaction has species that do not belong to reactants nor to products.")
        # Reactants and products are written under the format "A + B + C..."
        reactants = split_reaction[0].split('+')
        products = split_reaction[1].split('+')
        for r in reactants:
            r = r.strip()
            if r:
                total_reactants.append(r)
                formula += f"{r}*"
        for p in products:
            p = p.strip()
            if p:
                total_products.append(p)
    return(formula, total_reactants, total_products)

def antimony_write_reactions(file: IO[str], f_ratelaws: str | os.PathLike,
                             f_output_parameters: str | os.PathLike) -> None:
    """Write SparcedModel.Model reactions into an Antimony file

    Arguments:
        f_antimony: The open Antimony file.
        model: A SpacedModel.Model.

    Returns:
        A tuple with the parameters' names list and the parameters'
        values list.
    """

    file.write("# Reactions:\n")
    # Ratelaws
    ratelaw_sheet = load_input_data_file(f_ratelaws)
    ratelaws = np.array([line[1:] for line in ratelaw_sheet[1:]],
                        dtype="object")
    ratelaws_ids = np.array([line[0] for line in ratelaw_sheet[1:]],
                            dtype="object")
    # Parameters
    param_names = []
    param_values = []
    param_reaction_ids = []
    param_nbs = []
    for row_nb, reaction in enumerate(ratelaws):
        # Read reaction's species (reactants and products)
        formula = f"k{row_nb + 1}*"
        formula, reactants, products = read_reactions_species(reaction[1],
                                                              formula)
        # Read reaction's rate
        # Skip if no reactants nor products
        if reactants == [] and products == []:
            continue
        # Mass-action formula
        if 'k' not in reaction[2]:
            formula = formula[:-1]
            param_names.append(f'k{row_nb+1}')
            param_values.append(np.double(reaction[2]))
            param_reaction_ids.append(ratelaws_ids[row_nb])
            param_nbs.append(int(0))
        # Specified formula (non mass-action)
        else:
            formula = reaction[2]
            params = pd.to_numeric(reaction[3:], errors='coerce')
            params = params[~np.isnan(params)]
            j = 1
            if len(params) == 1:
                param_names.append(f"k{row_nb + 1}_{j}")
                param_values.append(float(reaction[j + 2]))
                param_reaction_ids.append(ratelaws_ids[row_nb])
                param_nbs.append(int(0))
                # Search for pattern matches
                # k - non numerical character - numerical character
                pattern = "k\D*\d*"
                compiled = re.compile(pattern)
                matches = compiled.finditer(formula)
                for m in matches:
                    formula = formula.replace(m.group(),param_names[-1])
            else:
                for q, p in enumerate(params):
                    param_names.append(f"k{row_nb + 1}_{j}")
                    param_values.append(float(reaction[j + 2]))
                    param_reaction_ids.append(ratelaws_ids[row_nb])
                    param_nbs.append(q)
                    pattern = f"k(\D*)\d*_{j}"
                    compiled = re.compile(pattern)
                    matches = compiled.finditer(formula)
                    for m in matches:
                        formula = formula.replace(m.group(),param_names[-1])
                    j +=1
        file.write(f"{ratelaws_ids[row_nb]}: {'+'.join(reactants)} => {'+'.join(products)}; ({formula})*{reaction[0]};\n")
    # Export parameters for each reaction, with corresponding order within the ratelaw and its value
    params_all = pd.DataFrame({'value': param_values,
                               'rxn': param_reaction_ids,
                               'idx': param_nbs}, index=param_names)
    params_all.to_csv(f_output_parameters, sep='\t', header=True, index=True)
    file.write("\n")
    return(param_names, param_values)

