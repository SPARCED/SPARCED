===============================================================================
Model Compilation
===============================================================================

General
-------------------------------------------------------------------------------

Main function to generate a SPARCED model

.. autofunction:: compilation.create_and_compile_model()

Additional functions for model creation and compilation

.. autofunction:: compilation.compile_model()

.. autofunction:: compilation.create_model()


AMICI
-------------------------------------------------------------------------------

Model compilation

.. autofunction:: model_compilation.compile_sbml_to_amici()

Utilities

.. autofunction:: amici_utils.define_observables()

.. autofunction:: amici_utils.extract_amici_model_name()


Antimony
-------------------------------------------------------------------------------

Main functions to generate an Antimony file

.. autofunction:: creation.antimony_create_file()

.. autofunction:: creation.antimony_write_file()

Define basic elements into an Antimony file

.. autofunction:: definitions.define_compartments()

.. autofunction:: definitions.define_species()

.. autofunction:: define_units()

Set initial conditions of an Antimony file

.. autofunction:: initial_conditions.set_compartments_ic()

.. autofunction:: initial_conditions.set_reactions_ic()

.. autofunction:: intiial_conditions.set_species_ic()

Write reactions into an Antimony file

.. autofunction:: reactions._read_reactions_species()

.. autofunction:: reactions.write_reactions()


Conversion
-------------------------------------------------------------------------------

.. autofunction:: antimony_to_sbml.convert_antimony_to_sbml()


SBML
-------------------------------------------------------------------------------

Find location of the SBML file

.. autofunction:: creation.build_sbml_model_path()

.. autofunction:: creation.get_sbml_model_path()

Annotate an SBML model

.. autofunction:: annotations.sbml_annotate_model()

.. autofunction:: annotations.write_species_annotations()

