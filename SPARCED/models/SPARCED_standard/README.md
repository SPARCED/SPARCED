# The Standard SPARCED Model

## Description

The standard SPARCED model aims to combine all the validated extensions of
SPARCED into one single directory.
As an aspiring WC (whole-cell) model, SPARCED is called to face several
extensions. The standard model is the most up-to-date validated version
of SPARCED, and should always serve as a comparison base before any merging.
We highly encourage you to use the benchmarking tool provided in this
repository to ensure that any alteration or extension does not break the
model.

In consequence, any further improvement of SPARCED should be incorporated into
this model.

## History

This model was originally based on the same input data files as for the
legacy SPARCED model, version 1.3.0 (see the _SPARCED_legacy_ model folder
for further details about that version).
Files that are strictly identical to that version bear the prefix `legacy_`
into their names.

Since December 2024, the SPARCED pipeline has evolved to remove support of
the stoichiometric matrix. In consequence, the Ratelaws file got replaced
by a new one, based on the `noStoicMat` branch of the version 1.3.0 and adapted
to replicate the standard's settings at that moment.

