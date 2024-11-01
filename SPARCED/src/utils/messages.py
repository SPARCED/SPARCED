#!/usr/bin/env python
# -*- coding: utf-8 -*-

class CustomText:
    ANTIMONY_HEADER = "PanCancer Model by Birtwistle and Erdem Labs"
    ANTIMONY_NM = "1e-9 mole / litre"
    ANTIMONY_SUBSTANCE = "1e-9 mole"
    ANTIMONY_TIME_UNIT = "second"
    ANTIMONY_VOLUME = "litre"

class WorkflowMessage:
    AMICI_MODEL_COMPILATION_SUCCESS = "Success compiling the model"
    ANTIMONY_CONVERT_TO_SBML_FAILURE = "Failed to convert Antimony file to SBML"
    ANTIMONY_CONVERT_TO_SBML_SUCCESS = "Success converting Antimony file to SBML"
    ANTIMONY_LOAD_FILE_FAILURE = "Failed to load Antimony file"
    ANTIMONY_LOAD_FILE_SUCCESS = "Success loading Antimony file"

    def __setattr__(self, name, value):
        raise TypeError("Workflow messages are immutable.")

