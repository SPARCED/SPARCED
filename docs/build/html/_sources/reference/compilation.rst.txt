===============================================================================
Compilation
===============================================================================

General
-------------------------------------------------------------------------------

.. autofunction:: compilation.create_model()

.. autofunction:: compilation.create_and_compile()

.. autofunction:: compilation.compile_model() 

AMICI
-------------------------------------------------------------------------------

Creation

.. autofunction:: creation.create_folder()

Legacy

.. autofunction:: legacy.define_observables()

Antimony
-------------------------------------------------------------------------------

Creation

.. autofunction:: creation.antimony_create_file()

.. autofunction:: creation.antimony_write_file()

Definitions

.. autofunction:: definitions.define_compartments()

.. autofunction:: definitions.define_species()

.. autofunction:: definitions.define_units()

Initial Conditions

.. autofunction:: initial_conditions.set_compartments_ic()

.. autofunction:: initial_conditions.set_reactions_ic()

.. autofunction:: initial_conditions.set_species_ic()

.. autofunction:: reactions._read_reactions_species()

.. autofunction:: reactions.write_reactions()

Conversion scripts
-------------------------------------------------------------------------------

.. autofunction:: antimony_to_sbml.convert_antimony_to_sbml()

.. autofunction:: sbml_to_amici.sbml_convert_to_amici()

SBML
-------------------------------------------------------------------------------

Annotations

.. autofunction:: annotations.sbml_annotate_model()

.. autofunction:: annotations.write_compartments_annotations()

.. autofunction:: annotations.write_species_annotations()

Creation

.. autofunction:: creation.build_sbml_model_path()

.. autofunction:: creation.get_sbml_model_path()

