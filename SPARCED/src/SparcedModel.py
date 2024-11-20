#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys

from yaml import safe_load

from utils.files_handling import *


# CUSTOM ERRORS

class InvalidModelName(ValueError):
    def __init__(self, message, model_name):
        self.message = message
        self.model_name = model_name

    def __str__(self):
        return(f"SPARCED ERROR: Invalid model name.\n \
                 Name: {self.model_name}\n \
                 Error: {self.message}\n")

class EmptyModelName(InvalidModelName):
    pass


# MODEL

class Model:

    def __init__(self, name="SPARCED_standard",
                 models_directory="./../models/", config_name="config.yaml"):
        # General settings
        self.name = self.set_name(name)
        self.path = append_subfolder(models_directory, self.name)
        self.configuration = self.load_configuration(self.path, config_name)
        self.data_location = append_subfolder(self.path,
                                              self.configuration['location'])
        check_path_existence(self.data_location)
        # Compilation
        self.compilation_files = self.load_compilation_files(
                                 self.data_location,
                                 self.configuration['compilation'])

    def load_configuration(self, path: str | os.PathLike, config_name: str):
        config_path = append_subfolder(path, config_name)
        check_path_existence(config_path)
        with config_path.open() as config_file:
            configuration = safe_load(config_file)
        return(configuration)

    def load_compilation_files(self, data_location: str | os.PathLike,
                                     compilation_config
                                     ) -> dict[str, str | os.PathLike]:
        """Load compilation input file paths

        Note:
            Dictionnary structure is expected to contain:
            > a 'root' item indicating the location of the compilation
              input files subfolder
            > a 'files' item containing a dictionnary of file types and
              their names

        Arguments:
            data_location: The path towards the location of the model's
                           data.
            compilation_config: A dictionnary structured as stated in
                                the __Note__ section.

        Returns:
            A dictionnary structured as key: input file type / value:
            input file path.
        """

        compilation_data_location = append_subfolder(self.data_location,
                                                     compilation_config['root'])
        check_path_existence(compilation_data_location)
        # TODO: adjust for multiple files
        for file_type, file_name in compilation_config['files'].items():
            if file_name != None:
                compilation_config['files'][file_type] = append_subfolder(
                                                         compilation_data_location,
                                                         file_name)
                # Do not check existence of files that will be created upon
                # compilation
                if file_type != "output_parameters":
                    check_path_existence(compilation_config['files'][file_type])
        return(compilation_config['files'])

    def sanitize_name(self, name: str) -> str:
        """Sanitize a name

        Note:
            As Antimony cannot handle the dash ('-') character as a
            model name, any occurence of this character is replaced by
            an underscore ('_').

        Warning:
            This might result into the breakage of some further
            functionalities.

        Arguments:
            name: The name.

        Returns:
            The corresponding sanitized name.
        """

        name = name.replace('-', '_')
        return(name)

    def set_name(self, name: str) -> str:
        """Set a name

        Run validation and sanitization on the name if necessary.

        Arguments:
            name: The name.

        Returns:
            The name or a corresponding sanitized name.
        """

        try:
            self.validate_name(name)
        except EmptyModelNamei as error:
            print(error)
            sys.exit(0)
        except InvalidModelName as error:
            print(error)
            name = self.sanitize_name(name)
        return(name)

    def validate_name(self, name: str) -> bool:
        """Validate a naöe

        Note:
            Name cannot be empty.
            Name should not contain a dash '-' character.

        Argurments:
            name: The name.

        Returns:
            A boolean representing the validity of the name.
        """

        is_valid = False
        if not name:
            raise EmptyModelName("No model name provided.", name)
        elif '-' in name:
            raise InvalidModelName("Dash '-' character not supported.", name)
        else:
            is_valid = True
        return(is_valid)

