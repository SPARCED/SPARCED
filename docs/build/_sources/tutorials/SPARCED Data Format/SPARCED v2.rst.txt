SPARCED input file format specification
===============================================================================
This page explains the SPARCED data format, which is a standardized format for 
encoding biological models in a machine-readable format. SPARCED is designed to 
be compatible with PEtab, SBML, and PCRE2, and is intended to facilitate the 
exchange of biological models between different software tools.

The SPARCED file format is not trying to re-invent an already well defined and
established format (i.e. SBML), we simply want to provide systems biologists 
with a standardized format with the goal of merging various desparate 
pathway models into a single kinetic model. Constructing the SPARCED model includes
the use of such tools, including conversion from the tabular format sepcified here
to Antimony, then to SBML, and finally to AMICI in order for the model to be simulated.

General Principles
------------------
1. **Model-Merging**: SPARCED files are intended to be easily merged with other SPARCED files, allowing users to combine models from different sources.
2. **Compatibility**: SPARCED is designed to be converted from the tabular format specified here (inspired by PEtab) to Antimony, SBML, and AMICI models.
3. **Human-Readable**: SPARCED files are designed to be human-readable, with clear and concise syntax that is easy to understand.
4. **Machine-Readable**: SPARCED files are also machine-readable, with a well-defined structure that can be parsed by software tools.

File Organization
-----------------
SPARCED files are organized into 7 tabular files, each of which contains a specific type of information critical towards building systems biology models:

1. **Species**: Defines the species in the model, including their names, initial concentrations, compartment locations, and UniProt annotations.
2. **RateLaws**: Defines the rate laws for the model, including the reaction names, home compartments, equations, kinetic parameters, and references.
3. **Compartments**: Defines the compartments in the model, including their names, sizes, and GO annotations.
4. **Observables**: Defines the model observables; the compartment-corrected summations of all formats of a protein.
5. **OmicsData** (optional): Defines the omics data used to constrain the model, including the data type, values, and references.
6. **GeneReg** (optional): Defines transcriptional activation and inhibition relationships between genes and transcription factors. 
7. **Initializer** (optional): Defines information for model initialization.

**Remarks**
- all model entities, column names, and row names are case-sensitive.

Species table
-------------
The `Species` table defines the species in the model, including their names, 
initial concentrations, compartment locations, and UniProt annotations. Further, 
contains information about the species in the deterministic module. 
Each row corresponds to one species (protein, protein complex, post-transcriptionally 
modified species). Transcripts (in nM) are also included in this file because 
they are regarded as species with updated concentrations in the stochastic 
module every 30(s) and are used in translation rate laws.

.. list-table:: Species Table
   :header-rows: 1
   :widths: 25 25 25 25
   :class: species-table

   * - `speciesId`
     - `compartment`
     - `initialConcentration`
     - `UniProt`
   * - STRING
     - STRING
     - FLOAT
     - STRING
   * - e.g.
     - 
     - 
     - 
   * - `Cd__Cdk4__p27`
     - `cytoplasm`
     - 0.787522147
     - P24385,P30279, P30281, P11802, Q00534, P46527

Detailed field descriptions
+++++++++++++++++++++++++++
- `speciesId` [STRING, NOT NULL]: The unique identifier for the species, following 
the SPARCED species naming convention. Strict adherence to the naming convention
is required for compatibility with PEtab, SBML, and PCRE2. 
   - see `Species-Nomenclature <https://sparced.readthedocs.io/en/latest/tutorials/Building-SPARCED-Input-Files/Species-Nomenclature.html>_.`
    for more information.

- `compartment` [STRING, NOT NULL]: The compartment in which the species resides.
    - Must be one of the compartments defined in the `Compartments` table.
    - Must be consistent with the compartment specified in the species name.

- `initialConcentration` [FLOAT, NOT NULL]: The initial concentration of the species.
    - Must be a non-negative number.

- `UniProt` [STRING, OPTIONAL]: The UniProt identifiers for the species.
    - Multiple UniProt identifiers should be separated by commas.
    - Must be consistent with the species name.
    - Preferably, in the same order as the species name. 
    - For species identifiers representing multiple proteins (i.e. `Cd` represents in 
    this case CyclinD1, CyclinD2, and CyclinD3), the UniProt identifiers should be
    separated by commas in alpha-numeric order.

Ratelaws Table
--------------

The `Ratelaws` table defines the reactions in the deterministic module, 
including reaction names, home compartments, rate laws, and parameters. 
Each row corresponds to a single reaction, and the order of rows must align with
 the columns in the `StoichiometricMatrix` input file. Reactions can follow 
 either a simple mass-action law or a complex rate law formula with parameters 
 defined explicitly.

.. list-table:: Ratelaws Table
   :header-rows: 1
   :widths: 15 25 60
   :class: ratelaws-table

   * - Column
     - Description
     - Example
   * - `reactionId`
     - STRING
     - `vC23`
   * - `compartment`
     - STRING
     - `Nucleus`
   * - `rateLaw`
     - STRING or FLOAT
     - `kC23_1*(Cd__Cdk4/(kC23_2+Cd__Cdk4))`
   * - `parameter_1`
     - FLOAT (OPTIONAL)
     - `0.09444444`
   * - `parameter_2`
     - FLOAT (OPTIONAL)
     - `10`

Detailed Field Descriptions
---------------------------

- **`reactionId`** [STRING, NOT NULL]: The unique identifier for the reaction.  
  - Must be unique in the file and typically follows a naming convention indicating 
  the sub-module (e.g., `vA1` for Apoptosis, `vC1` for Cell Cycle).  

- **`compartment`** [STRING, NOT NULL]: The home compartment where the reaction occurs.  
  - Must match a defined compartment in the `Compartments` table.  
  - Defines the effective search volume for reactants and products, and volumetric 
  corrections may apply for species in different compartments.  

- **`rateLaw`** [STRING or FLOAT, NOT NULL]: Specifies the rate law for the reaction.  
  - If a FLOAT is provided, the reaction follows a mass-action law, and the value 
  is the rate constant (units: nM/s).  
  - If a STRING is provided, the reaction follows the specified formula, which 
  must include species names and parameter names consistent with the model.  

- **`parameter_n`** [FLOAT, OPTIONAL]: Parameters used in the rate law formula.  
  - Parameter names must start with `k` and be unique within the formula (e.g., `k1`, `k2`).  
  - Values are provided in appropriate units (e.g., nM or seconds).  
  - Parameters are automatically renamed during model generation for consistency.  

Notes for Users
+++++++++++++++

- The compartments for reactions must be defined in the `Compartments` table and 
are used to rescale concentrations when reactants and products reside in different volumes.  
- Parameters in rate law formulas are extracted and renamed in the `ParamsAll` output file for reference.  
- Ensure the number and order of rows in this file match the columns in the `StoichiometricMatrix`.  

Compartments Table
------------------

The `Compartments` table specifies the cellular compartments in the model, 
including their names, volumes, and corresponding Gene Ontology (GO) terms. 
These compartments define the spatial context for species and reactions, 
ensuring consistency across the model's input files.

.. list-table:: Compartments Table
   :header-rows: 1
   :widths: 25 25 50
   :class: compartments-table

   * - Column
     - Description
     - Example
   * - `compartmentId`
     - STRING
     - `cytoplasm`
   * - `volume`
     - FLOAT (LITERS)
     - `2.1e-12`
   * - `goTerm`
     - STRING
     - `GO:0005737`

Detailed Field Descriptions
---------------------------

- **`compartmentId`** [STRING, NOT NULL]: The unique identifier for the compartment.  
  - Must match the compartment names listed in the `Species` and `Ratelaws` input files.  

- **`volume`** [FLOAT, NOT NULL]: The volume of the compartment in liters.  
  - Must be a non-negative value.  
  - Defines the physical size of the compartment for scaling concentrations and reactions.  

- **`goTerm`** [STRING, OPTIONAL]: The Gene Ontology (GO) term associated with the compartment.  
  - Provides a standardized identifier for the compartment’s biological context.  
  - Example: `GO:0005737` for cytoplasm.  

Notes for Users
+++++++++++++++

- The compartment names must be consistent across all input files, including `Species` and `Ratelaws`.  
- Volumes are used to calculate concentration-based scaling factors when species 
and reactions involve multiple compartments.  
- GO terms are optional but recommended for better integration with external 
databases and annotation tools.  

Observables table
-----------------
The `Observables` table defines the mapping of model species to the measurable 
quantities (observables) used for simulations and analysis.  
Each observable corresponds to the compartmental-volume-corrected summation of
 all formats of a protein. Entries in this table indicate whether a specific 
 species contributes to a given observable.  

.. list-table:: Observables Table
   :header-rows: 1
   :widths: 20 40 40
   :class: observables-table

   * - Column
     - Description
     - Example
   * - `observableId`
     - STRING: The unique identifier for each observable.
     - `pEGFR`
   * - `speciesId`
     - STRING: The unique identifier for each species, following SPARCED species naming conventions.
     - `EGFR_Y1068`
   * - `compartment`
     - STRING: The compartment associated with the species.  
       Must align with the compartments listed in the `Compartments` table. 
     - `cytoplasm`
   * - `inObservable`
     - INTEGER: Binary indicator (1 if the species contributes to the observable, 0 otherwise).
     - `1`

Detailed field descriptions
+++++++++++++++++++++++++++
- `observableId` [STRING, NOT NULL]: The unique identifier for each observable, 
which typically corresponds to a measurable feature of interest, such as the 
total phosphorylation of a receptor.  
    - Observables are defined based on experimental data and model requirements.
    - Ensure unique naming conventions to prevent conflicts during model generation.  

- `speciesId` [STRING, NOT NULL]: The unique identifier for the species that may contribute to the observable.  
    - Matches species defined in the `Species` table.  

- `compartment` [STRING, OPTIONAL]: The compartment in which the species resides.  
    - Should match the compartment associated with the species in the `Species` and `Compartments` tables.

- `inObservable` [INTEGER, NOT NULL]: Indicates whether the species contributes to the observable.  
    - Must be either `1` (species contributes) or `0` (species does not contribute).  
    - This binary mapping allows summation of species concentrations to compute observable values.

Usage
+++++
The `Observables` table is used as input to the AMICI model compiler during the 
simulation process. It defines how species concentrations are aggregated into
 observables, enabling the calculation of measurable outputs for model validation
  and comparison with experimental data. 

OmicsData Table
---------------

The `OmicsData` table contains information about gene-level parameters, mRNA levels, 
and protein levels used in the model. It serves as a central repository for 
integrating gene copy numbers, mRNA molecule counts, and protein abundance with
 rate constants for transcription, translation, and degradation. Each row
  corresponds to one gene, identified by its HGNC name, and includes various 
  ebiological and kinetic parameters essential for the deterministic and stochastic modules.

.. list-table:: OmicsData Table  
   :header-rows: 1  
   :widths: 15 15 15 15 15 15 15 15 15 15 15  
   :class: omicsdata-table  

   * - Column  
     - Description  
     - Example  
   * - `geneId`  
     - STRING  
     - `TP53`  
   * - `geneCopyNumber`  
     - INTEGER  
     - `2`  
   * - `mRNA_copyNumber`  
     - FLOAT  
     - `1500.0`  
   * - `rateConstant_inactivation`  
     - FLOAT (s⁻¹)  
     - `0.0002`  
   * - `rateConstant_activation`  
     - FLOAT (s⁻¹)  
     - `0.0015`  
   * - `constitutiveTranscription`  
     - FLOAT (molecules/s)  
     - `1.0`  
   * - `maximalTranscription`  
     - FLOAT (molecules/s)  
     - `5.0`  
   * - `mRNA_degradation`  
     - FLOAT (s⁻¹)  
     - `0.002`  
   * - `protein_copyNumber`  
     - INTEGER  
     - `50000`  
   * - `protein_halfLife`  
     - FLOAT (s)  
     - `3600.0`  
   * - `translationRate`  
     - FLOAT (s⁻¹)  
     - `0.003`  

Detailed field descriptions
+++++++++++++++++++++++++++

- **`geneId`** [STRING, NOT NULL]: The HGNC identifier of the gene.  
  - Must be unique in the file.  

- **`geneCopyNumber`** [INTEGER, NOT NULL]: The number of copies of the gene present in the cell.  
  - Represents genomic-level data.  

- **`mRNA_copyNumber`** [FLOAT, NOT NULL]: The number of mRNA molecules per cell (mpc).  
  - Represents transcript-level abundance.  

- **`rateConstant_inactivation`** [FLOAT (s⁻¹), NOT NULL]: The rate constant for gene inactivation.  

- **`rateConstant_activation`** [FLOAT (s⁻¹), NOT NULL]: The rate constant for gene activation.  

- **`constitutiveTranscription`** [FLOAT (molecules/s), OPTIONAL]: Baseline transcription rate for the gene.  

- **`maximalTranscription`** [FLOAT (molecules/s), OPTIONAL]: Maximal transcription rate for the gene under activation conditions.  

- **`mRNA_degradation`** [FLOAT (s⁻¹), NOT NULL]: The degradation rate constant of the mRNA.  

- **`protein_copyNumber`** [INTEGER, OPTIONAL]: The number of protein molecules per cell (mpc).  
  - Represents proteomic-level abundance.  

- **`protein_halfLife`** [FLOAT (s), OPTIONAL]: The half-life of the protein in seconds.  

- **`translationRate`** [FLOAT (s⁻¹), OPTIONAL]: The rate constant for mRNA translation.  

Notes for Users
+++++++++++++++

- All rate constants are based on data from the Bouhaddou2018 model and literature.  
- Users can add new genes (rows) using RNA-seq data for mRNA estimation. 
For missing rate constants, median values from the existing dataset can provide a reasonable starting point.  

GeneReg table
-------------
The `GeneReg` table defines transcriptional activation and inhibition interactions 
in the SPARCED model. Each row corresponds to a gene, and each column corresponds
 to a species that acts as an activator or repressor of transcriptional activity.  

.. list-table:: GeneReg Table
   :header-rows: 1
   :widths: 20 40 40
   :class: genereg-table

   * - Column
     - Description
     - Example
   * - `geneId`
     - STRING: The HGNC-compliant name of the gene being regulated.
     - `CDKN1A` (p21)
   * - `speciesId_1`, `speciesId_2`, ..., `speciesId_n`
     - STRING: Columns representing each regulator species defined in the `Species` table.  
       A species can act as an activator or repressor of transcriptional activity.
     - `TP53`
   * - `regulation`
     - STRING: Regulatory effect of the species on the gene. Defined as a 
     combination of a hill coefficient (A) and a half-maximal concentration (B),
      separated by a semicolon (`A; B`).  
       Positive `A` values indicate activation; negative `A` values indicate repression.
     - `2; 0.5`

Detailed field descriptions
+++++++++++++++++++++++++++
- `geneId` [STRING, NOT NULL]: The name of the gene being regulated, written in HGNC format.  
    - Gene names must match the names in the `Species` table for consistency.

- `speciesId_*` [STRING, OPTIONAL]: The species acting as regulators of the gene.  
    - Defined in columns corresponding to regulatory species.
    - Regulatory species must exist in the `Species` table and can act as activators or repressors.

- `regulation` [STRING, OPTIONAL]: Describes the regulatory effect of a species on gene transcription.  
    - Format: `A; B`, where:  
      - `A` is the Hill coefficient, with positive values for activation and negative values for repression.  
      - `B` is the half-maximal concentration of the regulatory effect.  
    - If no regulation exists, this field is set to `0`.  

Usage
+++++
The `GeneReg` table is utilized by the stochastic module of the SPARCED model to
 update mRNA levels during simulations. Non-zero entries define the quantitative
  parameters of transcriptional regulation, which determine how species influence
   gene expression.  

Guidelines for Extension
++++++++++++++++++++++++
To include additional transcriptional regulators in the SPARCED model:  
1. Add new columns for each additional regulatory species.  
2. Populate the columns with the appropriate rate constants in the `A; B` format.  
3. Ensure consistency with the `Species` and `Genes` tables for naming and structure.

Initializer file (Optional)
---------------------------
The `Initializer` file provides optional information for model initialization.
 It defines species concentrations, mRNA level adjustments, parameter values,
  observable exclusions, and parameter scan ranges. This file is used to 
  establish a starting point for deterministic simulations, such as serum-starved
   MCF10A cells under specific experimental conditions.

.. list-table:: Initializer File
   :header-rows: 1
   :widths: 15 45 40
   :class: initializer-table

   * - Column(s)
     - Description
     - Example
   * - `speciesId`, `initialConcentration`
     - STRING, FLOAT: Specifies species and their starting concentrations.  
       This information initializes species concentrations.
     - `EGFR`, `0.5`
   * - `mRNAId`, `initialLevel`
     - STRING, FLOAT: Defines adjustments to mRNA levels for specific genes.
     - `CDKN1A`, `2.0`
   * - `parameterId`, `initialValue`, `units`
     - STRING, FLOAT, STRING: Specifies parameter names, their initial values, and associated units.  
       Used for initializing specific model parameters.
     - `k_deg`, `0.01`, `1/s`
   * - `observableId_excluded`
     - STRING: Defines observables excluded from translation rate adjustments.  
       Ensures these observables are not modified during initialization.
     - `Cyclin_D1`
   * - `parameterId`, `minValue`, `maxValue`
     - STRING, FLOAT, FLOAT: Describes the parameter scan range for a single parameter.  
       Used for sensitivity analysis or optimization during initialization.
     - `k_on`, `0.1`, `10.0`

Detailed field descriptions
+++++++++++++++++++++++++++
1. **Species Concentrations**  
   - `speciesId` [STRING, OPTIONAL]: Name of the species being initialized.  
     Must match species names in the `Species` table.  
   - `initialConcentration` [FLOAT, OPTIONAL]: Initial concentration of the species (in model-defined units).

2. **mRNA Level Adjustments**  
   - `mRNAId` [STRING, OPTIONAL]: Name of the mRNA species being adjusted.  
   - `initialLevel` [FLOAT, OPTIONAL]: Initial mRNA level for the species.

3. **Parameter Values**  
   - `parameterId` [STRING, OPTIONAL]: Name of the parameter being initialized.  
     Parameter names should match those defined in the `ParamsAll` or `Ratelaws` file.  
   - `initialValue` [FLOAT, OPTIONAL]: Starting value of the parameter.  
   - `units` [STRING, OPTIONAL]: Units of the parameter, consistent with the model specification.

4. **Observable Exclusions**  
   - `observableId_excluded` [STRING, OPTIONAL]: Name of the observable excluded from translation rate adjustments.

5. **Parameter Scan Range**  
   - `parameterId` [STRING, OPTIONAL]: Name of the parameter for single-parameter scans.  
   - `minValue` [FLOAT, OPTIONAL]: Minimum value in the scan range.  
   - `maxValue` [FLOAT, OPTIONAL]: Maximum value in the scan range.

Usage
+++++
The `Initializer` file is especially useful for setting up simulations where 
specific biological conditions must be reflected, such as:  
- Serum-starved MCF10A cells that remain quiescent without external growth factor stimulation.  
- Customizing initial species levels or parameter values to match experimental data.  
- Running sensitivity analyses by scanning parameter ranges.  
