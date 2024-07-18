#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thurs. 07/18/2024 2:00pm - JRH

Creates a new benchmark given a name 

- potential to add more features in the future

"""

#-----------------------Package Import & Defined Arguements-------------------#
import os
import shutil
import datetime
from typing import Dict, List
from pathlib import Path
from arguements import parse_args
args = parse_args()

#-----------------------Function Definition-----------------------------------#
class BenchmarkCreator:
    """
    Class containing functions to create a new benchmark
    """
    def create_new_benchmark() -> dict[str, list[str]]:
        """
        Creates a new benchmark given a name
        """

        assert os.path.basename(os.getcwd()) == 'benchmark_utils', \
              "Please run this script from the benchmark_utils directory"

        # Get the name of the benchmark
        assert args.name is not None, "Please provide a name for the benchmark \
using the --name or -n argument"
        
        name = args.name

        project_dir = Path(f"../{name}")
        project_dir.mkdir(parents=True, exist_ok=True)

        # List of files to create
        files_to_create = [
            "README.md",
            "conditions.tsv",
            "measurements.tsv",
            "observables.tsv",
            "parameters.tsv",
            "model_specification.tsv",
            f"{name}.yml"
        ]

        # Create each file in the project directory
        for file_name in files_to_create:
            file_path = project_dir / file_name
            file_path.touch()

        curated_decision = input("Would you like to create a curated benchmark? (y/n): ")
        if curated_decision == "y":
            BenchmarkCreator.curated_benchmark_creator()

        else:

            if args.benchmark_description and os.path.isfile(args.benchmark_description):
                with open(f"../{name}/README.md", "w") as f:
                    f.write(args.benchmark_description)
            else:
                with open(f"../{name}/README.md", "w") as f:
                    f.write(f"# {name}\n\nThis is a new benchmark created by the benchmark_utils package")

            BenchmarkCreator.populate_yml_file(f"../{name}/{name}.yml")

        print(f"Created new benchmark: {name}")
        return {"name": [name]}


    def curated_benchmark_creator() -> dict[str, list[str]]:
        """
        if prompted by the user; walks through a series of prompts to create a
        curated benchmark based on the user's input.

        Returns:
            dict[str, list[str]]: A dictionary containing the name of the benchmark
            and the list of files created 
        """
        
        # Get the name of the benchmark
        name = input("Enter the name of the benchmark: ")

        # Create the benchmark
        project_dir = Path(f"../{name}")
        project_dir.mkdir(parents=True, exist_ok=True)

        # List of files to create
        files_to_create = [
            "README.md",
            "conditions.tsv",
            "measurements.tsv",
            "observables.tsv",
            "parameters.tsv",
            "model_specification.tsv",
            f"{name}.yml"
        ]

        # Create each file in the project directory
        for file_name in files_to_create:
            file_path = project_dir / file_name
            file_path.touch()

        ReadMe_decision = input("Would you like to add a README file to the benchmark? (y/n): ")
        if ReadMe_decision == "y":
            BenchmarkCreator.readme_generator()
        else:
            pass

        Measurements_decision = input("Would you like to add a measurements file to the benchmark? (y/n): ")
        if Measurements_decision == "y":
            BenchmarkCreator.measurements_generator()
        else:
            pass

        yaml_decision = input("Would you like to add a YAML file to the benchmark? (y/n): ")
        if yaml_decision == "y":
            BenchmarkCreator.populate_yml_file(f"../{name}/{name}.yml")
        else:
            pass

        return {"name": [name]}


    def readme_generator() -> Dict[str, List[str]]:
        """
        Generates a README file for the benchmark with metadata including
        date created and author.
        """
        # Get the author information
        author = input("Enter the author of the benchmark: ")

        # Get the description of the benchmark
        benchmark_description = input("Enter the description of the benchmark: ")

        # Get the current UTC date and time
        date_created = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S UTC")

        # Define the content for the README file
        readme_content = f"""# Benchmark README

    **Date Created:** {date_created}

    **Author:** {author}

    ## Benchmark Description

    {benchmark_description}
    """

        # Write the content to the README file
        with open(f"../{args.name}/README.md", "w") as f:
            f.write(readme_content)


    def measurements_generator() -> dict[str, list[str]]:
        """
        Generates a measurements file for the benchmark
        """
        # Get the path to the measurements file
        measurements = input("Enter the path to the measurements file: ")
        
        # verify that the measurements file is a list of measurements
        with open(measurements, "r") as f:
            measurement_data = f.readlines()
        
            # Write the measurements to the measurements file under the
            # measurements column of the tsv file
            with open(f"../{args.name}/measurements.tsv", "w") as f:
                f.write("measurements\n")
                for line in measurement_data:
                    f.write(line)


    def populate_yml_file(file_path) -> __file__:
        """
        Opens an existing YAML file and populates it with specified information.

        :param file_path: Path to the existing YAML file
        :param sbml_file_path: Path to the SBML file to be included
        """
        
        import yaml

        # Define the data to be added
        data = {
            'format_version': 1,
            'parameter_file': 'parameters.tsv',
            'problems': [
                {
                    'condition_files': ['conditions.tsv'],
                    'model_specification_files': ['model_specification.tsv'],
                    'measurement_files': ['measurements.tsv'],
                    'observable_files': ['observables.tsv'],
                    'sbml_files': ['{path}']
                }
            ]
        }

        # Read the existing content of the YAML file if it exists
        file = Path(file_path)
        if file.is_file():
            with open(file_path, 'r') as f:
                existing_data = yaml.safe_load(f) or {}
        else:
            existing_data = {}

        # Update the existing content with new data
        existing_data.update(data)

        # Write the updated content back to the YAML file
        with open(file_path, 'w') as f:
            yaml.safe_dump(existing_data, f, default_flow_style=False)


#-----------------------Main Function-----------------------------------------#
# Create the new benchmark, comment out if you want to run the unit test
if __name__ == "__main__":
    BenchmarkCreator.create_new_benchmark()




#-----------------------Unit Test Function-----------------------------------#
def remove_directory(name):
    project_dir = Path(f"../{name}")
    if project_dir.exists() and project_dir.is_dir():
        shutil.rmtree(project_dir)

def test_create_new_benchmark():
    """
    Tests the create_new_benchmark function
    """
    name = args.name

    # Remove the directory if it exists
    remove_directory(name)

    # Ensure the directory has been removed
    assert not os.path.isdir(f"../{name}"), f"{name} directory should not exist before test"

    # Create the new benchmark
    BenchmarkCreator.create_new_benchmark()

    # Ensure the directory has been created
    assert os.path.isdir(f"../{name}"), f"{name} directory should exist after creation"

    # Remove the directory again
    remove_directory(name)

    # Ensure the directory has been removed
    assert not os.path.isdir(f"../{name}"), f"{name} directory should not exist after cleanup"

    print("create_new_benchmark function passed")


# -----------------------Unit Test Function-----------------------------------#
# Uncomment this function to run the unit test
# if __name__ == "__main__":
#     test_create_new_benchmark()