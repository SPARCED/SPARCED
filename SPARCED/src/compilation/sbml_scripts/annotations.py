#!/usr/bin/env python
# -*- coding: utf-8 -*-

import libsbml
import numpy as np


def sbml_annotate_model(
    file_path: str, compartments: np.ndarray, species: np.ndarray
) -> None:
    """Annotate species and compartments of the given SBML model

    Arguments:
        file_path: The path towards the SBML file.
        compartments: Content of the compartments input file.
        species: Content of the species input file.

    Returns:
        Nothing.
    """

    # Import SBML file
    reader = libsbml.SBMLReader()
    document = reader.readSBML(file_path)
    sbml_model = document.getModel()
    # Set annotations
    write_compartments_annotations(sbml_model, compartments)
    write_species_annotations(sbml_model, species)
    # Export the annotated SBML file
    writer = libsbml.SBMLWriter()
    writer.writeSBML(document, file_path)


def write_compartments_annotations(file, compartments: np.ndarray) -> None:
    """Set compartments annotations in the given SBML file

    Note:
        First row should be the header and will be skipped.
        First column contains the compartments names.
        Annotations are expected to be located on the 3rd column of the
        array.

    Arguments:
        file: The loaded SBML file.
        compartments: Content of the compartments input file as
                      specified in the __Note__ section.

    Returns:
        Nothing.
    """

    for row in compartments[1:]:
        file.getCompartment(row[0]).setAnnotation(row[2])


def write_species_annotations(file, species: np.ndarray) -> None:
    """Set species annotations in the given SBML file

    Note:
        First row should be the header and will be skipped.
        Annotations are expected to be located between the 4th and the
        last column of the array.

    Arguments:
        file: The loaded SBML file.
        species: Content of the species input file.

    Returns:
        Nothing.
    """

    for i, row in enumerate(species[1:]):
        all_annotations = ""
        for column in range(4, len(row)):
            annotation = str(row[column].strip())
            if annotation:
                all_annotations += " " + row[column]
        file.getSpecies(row[0]).setAnnotation(all_annotations)
