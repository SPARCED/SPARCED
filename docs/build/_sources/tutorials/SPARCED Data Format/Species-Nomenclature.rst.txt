Species Naming Conventions
==========================

This page defines the standardized naming conventions for species in SPARCED, designed for compatibility with PEtab, SBML, and PCRE2.

General Principles
------------------
1. **Uniqueness**: Each species name must be unique across the model.
2. **Readability**: Names should be human-readable and concise, while avoiding ambiguity.
3. **Compatibility**: Naming conventions comply with PEtab, SBML, and PCRE2 standards.
4. **Minimal Redundancy**: Compartments are specified only if the species resides outside its "home" compartment (e.g., TGFb is extracellular by default).

Naming Structure
----------------
The general structure for species names is as follows:

.. code-block:: text

   [Modifiers][Residue&Position]_[BaseSpecies][__[AdditionalSpecies]][_Compartment]

Where:
------
- `Modifiers`: Prefixes indicating the modification state (e.g., `p` for phosphorylation, `u` for ubiquitination).
- `Residue&Position`: For species with specific post-translational modification (PTM) sites, denote the residue and its position (e.g., `S15` for serine 15).
- `BaseSpecies`: The core species name (e.g., `CyclinD`, `Cdk4`).
- `AdditionalSpecies`: For complexes, additional species are concatenated using `__` (double underscores).
- `Compartment`: The compartment is specified only when the species is outside its default "home" compartment.

Examples
^^^^^^^^

1. **Single Species with PTM**:

   * `pS15_TGFb_cytoplasm`: TGFb phosphorylated at serine 15, located in the cytoplasm.
|
2. **Two-Component Complex**:

   * `pS15_CyclinD__pT298_Cdk4_nucleus`: CyclinD phosphorylated at serine 15 and Cdk4 phosphorylated at threonine 298, in the nucleus.
|
3. **Multi-Component Complex**:

   * `pS15_CyclinD__pT298_Cdk4__pY104_EGFR_membrane`: CyclinD, Cdk4, and EGFR phosphorylated at specific residues, forming a complex at the membrane.

Prefixes
--------

The following table summarizes standard prefixes for species modifiers:

.. list-table:: Prefixes for Species Modifiers
   :header-rows: 1
   :widths: 20 40 40

   * - Prefix
     - Description
     - Example
   * - `p`
     - Phosphorylation
     - `pS15_TGFb`
   * - `u`
     - Ubiquitination
     - `uK48_TGFbR1`
   * - `m`
     - Methylation
     - `mK9_HistoneH3`
   * - `a`
     - Acetylation
     - `aK27_HistoneH3`
   * - `g`
     - Glycosylation
     - `gN100_EGFR`
   * - `c`
     - Cysteinylation
     - `cC100_EGFR`
   * - `i`
     - Inactivated state
     - `i_Cdk4`
   * - `m`
     - mRNA species of Gene names
     - `m_CCND1`

Suffixes
--------

The following table summarizes compartment suffixes and their use cases:

.. list-table:: Suffixes for Compartments
   :header-rows: 1
   :widths: 30 70

   * - Suffix
     - Description
   * - `_extracellular`
     - Species outside the cell.
   * - `_cytoplasm`
     - Species in the cytoplasm.
   * - `_nucleus`
     - Species in the nucleus.
   * - `_endosome`
     - Species bound to a membrane.
   * - `_mitochondria`
     - Species in the mitochondria.

Guidelines for Complexes
------------------------

For complexes, each species is listed in order, separated by double underscores (`__`). If a component species has PTMs, these are specified as part of its name. Compartments are only appended to the entire complex name, not individual components.

**Examples**:
^^^^^^^^^^^^^
|
   - Single PTM Complex: `pS15_CyclinD__Cdk4_cytoplasm`
|
   - Multi-PTM Complex: `pS15_CyclinD__pT298_Cdk4__pY104_EGFR_membrane`
|
Potential Pitfalls
------------------

1. **Ambiguity in Residue Position**:

   - Always specify residues and positions for clarity in PTM names.
   - Example: Avoid `p_CyclinD` if `pS15_CyclinD` is more precise.
|
2. **Complex Names Becoming Too Long**:

   - Avoid redundancy in component names.
   - Use short, standard prefixes for PTMs. Look at synonyms on UniProt for inspiration.
|
3. **Tool Compatibility**:

   - Avoid special characters like parentheses `()` or symbols like `&` that might break tools.

Regex Validation
----------------

The following regular expression ensures compatibility with PEtab, SBML, and PCRE2:

.. code-block:: text

   ^[a-zA-Z0-9_]+(__[a-zA-Z0-9_]+)*(_[a-zA-Z0-9_]+)?$

This regex enforces:
- Alphanumeric names with underscores.
- Double underscores (`__`) for complex species.
- Optional compartment suffixes.

Automating Naming
-----------------

To minimize errors and maintain consistency, consider automating the naming process with a script. Below is an example Python snippet for generating valid species names:

.. code-block:: python

   def generate_species_name(base, ptms=None, compartment=None):
       name = base
       if ptms:
           ptm_str = "__".join([f"{m}{r}" for m, r in ptms])
           name = f"{ptm_str}_{name}"
       if compartment:
           name = f"{name}_{compartment}"
       return name

   # Example Usage
   print(generate_species_name("CyclinD", ptms=[("pS", 15)], compartment="nucleus"))
   # Output: pS15_CyclinD_nucleus

---

