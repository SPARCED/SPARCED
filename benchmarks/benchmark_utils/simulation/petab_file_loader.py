import os
import sys
import yaml
import pandas as pd
from benchmark_utils.simulation.utils import Utils as utils

class PEtabRules:
    """PEtab rules for the conditions, measurement, observable, and visualization dataframes
    """
    @staticmethod
    def conditions_df_rules():
        """
        PEtab-defined rules for the conditions dataframe
        
        Returns:
        - conditions_df_rules (dict): conditions dataframe with the rules applied
        """
        return {
            'conditionId': {'type': 'str',
                        'required': True, 
                        'default': None,
                        'options': None},
            'conditionName': {'type': 'str',
                        'required': False, 
                        'default': None,
                        'options': None},
        }


    @staticmethod
    def measurement_df_rules():
        """
        PEtab-defined rules for the measurement dataframe to follow 

        Returns:
        - measurement_df_rules (dict): measurement dataframe with the rules applied

        """
        return {
            'observableId': {'type': 'str',
                        'required': True, 
                        'default': None, # References observables.observableID
                        'options': None},
            'simulationConditionId': {'type': 'str',
                        'required': True, 
                        'default': 'condition["conditionId"]', # References conditionsTable.conditionID
                        'options': None},
            'measurement': {'type': 'float',
                        'required': False, 
                        'default': None,
                        'options': None},
            'time': {'type': 'float',
                        'required': True, 
                        'default': 0.0,
                        'options': None},
            'observableParameters': {'type': 'str',
                        'required': True, 
                        'default': None,
                        'options': None},
            'noiseParameters': {'type': 'str',
                        'required': False, 
                        'default': None,
                        'options': None},
            'datasetId': {'type': 'str',
                        'required': False, 
                        'default': None,
                        'options': None},
            'replicateId': {'type': 'str',
                        'required': False, 
                        'default': 1,
                        'options': None},
        }


    @staticmethod
    def observable_df_rules():
        """
        PEtab-defined rules for the observable dataframe to follow

        Returns:
        - observable_df_rules (dict): observable dataframe with the rules applied
        """
        return {
            'observableId': {'type': 'str',
                        'required': True, 
                        'default': None,
                        'options': None},
            'observableName': {'type': 'str',
                        'required': False, 
                        'default': None,
                        'options': None},
            'observableFormula': {'type': 'str',
                        'required': True, 
                        'default': None,
                        'options': None},
            'observableTransformation': {'type': 'str',
                        'required': False, 
                        'default': None,
                        'options': None},
            'noiseFormula': {'type': 'str',    
                        'required': False, 
                        'default': None,
                        'options': None},
            'noiseDistribution': {'type': 'str',
                        'required': False, 
                        'default': None,
                        'options': None},
        }


    @staticmethod
    def visualization_df_rules():
        """
        PEtab-defined rules for the visualization dataframe
        Returns:
        - visualization_df_rules (dict): visualization dataframe with the rules applied
        """
        return {'plotId': {'type': 'str',
                                'required': True, 
                                'default': None,
                                'options': None},
                    'plotName': {'type': 'str', 
                                    'required': False, 
                                    'default': None, 
                                    'options': None},
                    'plotTypeSimulation': {'type': 'str', 
                                            'required': False, 
                                            'default': 'LinePlot',
                                            'options': ['LinePlot', 'ScatterPlot', 'BarPlot']},
                    'plotTypeData': {'type': 'str',
                                        'required': False,
                                        'default': 'MeanAndSD', 
                                        'options': ['MeanAndSD', 'MeanAndSEM', 
                                                    'replicates', 'provided']},
                    'datasetId': {'type': 'str',
                                    'required': False, 
                                    'default': None, 
                                    'options': None},
                    'xValues': {'type': 'str',
                                    'required': False, 
                                    'default': 'time', 
                                    'options': None},
                        'xOffset': {'type': 'str',
                                    'required': False, 
                                    'default': 0, 
                                    'options': None},
                    'xLabel': {'type': 'str', 
                                'required': False, 
                                'default': 'Time (hours)', 
                                'options': None},
                    'xScale': {'type': 'str', 
                                'required': False, 
                                'default': 'lin', 
                                'options': ['lin', 'log', 'log10', 'order']},
                    'yValues': {'type': 'str',
                                    'required': False,
                                    'default': None, 
                                    'options': None},
                        'yOffset': {'type': 'str',
                                    'required': False, 
                                    'default': 0, 
                                    'options': None},
                    'yScale': {'type': 'str',
                                'required': False,
                                'default': 'lin',
                                'options': ['lin', 'log', 'log10', 'order']},
                    'yLabel': {'type': 'str', 
                                'required': False,
                                'default': None, 
                                'options': None},
                        'legendEntry': {'type': 'str',
                                        'required': False,
                                        'default': None, 
                                        'options': None},
                        'Color': {'type': 'str',
                                'required': False, 
                                    'default': None,
                                    'options': None},
                    }


    @staticmethod
    def check_if_option(rule_dict: dict, column: str, value: str):
        """Checks if a value is in the options list for a given column
        input:
            rule_dict: dict - dictionary of rules for the dataframe
            column: str - column to check the value against
            value: str - value to check against the options list
        output:
            value: str - value if it is in the options list
        """
        if value in rule_dict[column]['options']:
            return value
        else:
            raise ValueError(f"{value} is not a valid option for {column}")


    @staticmethod
    def add_required_columns(df: pd.DataFrame, rule_dict: dict):
        """Checks if all required columns in the rules dictionary are present \
            in the dataframe. If not, adds the column with default values.
        input:
            df: pd.DataFrame - dataframe to check
            rule_dict: dict - dictionary of rules for the dataframe

        output:
            df: pd.DataFrame - dataframe with the column added if necessary
        """
        for column in rule_dict:
            if rule_dict[column]['required'] and column not in df.columns:
                # Add the corresponding rule default value to the column
                df[column] = PEtabRules.retrieve_default_value(rule_dict, column)

        return df


    @staticmethod
    def retrieve_default_value(rule_dict:dict, column: str):
        """Retrieves the default value for a given column
        input:
            column: str - column to retrieve the default value for
        output:
            default_value: str - default value for the column
        """
        default_value = rule_dict[column]['default']

        return default_value


    @staticmethod
    def eval_df_contents(df: pd.DataFrame, rule_dict: dict):
        """Evaluates the contents of a dataframe and fills in missing values with
        default values if necessary.

        Parameters:
            df: pd.DataFrame - dataframe to evaluate
            rule_dict: dict - dictionary of rules for the dataframe
        Returns:
            df: pd.DataFrame - evaluated dataframe
        """
        for column in rule_dict:
            try:
                df[column]
            except KeyError:
                df = PEtabRules.add_required_columns(df, rule_dict)

            if df[column] == 'None':
                df[column] = PEtabRules.retrieve_default_value(rule_dict, column)
            else:
                df[column] = df[column]

            try:
                PEtabRules.check_if_option(rule_dict, column, df[column])
            except KeyError:
                sys.exit(1)

        return df


# Load the PEtab files
class PEtabFileLoader:
    """Load PEtab files from a given YAML file.
    input:
        yaml_file: str - path to the YAML file"""
    conditions_df_rules = PEtabRules.conditions_df_rules()
    measurement_df_rules = PEtabRules.measurement_df_rules()
    observable_df_rules = PEtabRules.observable_df_rules()
    visualization_df_rules = PEtabRules.visualization_df_rules()


    def __init__(self, yaml_file: str):
        """
        Initializes the PEtabFileLoader object with the path to the YAML file.

        Parameters:
        - yaml_file (str): path to the YAML file

        Returns:
        - SBML file (str): path to the SBML file
        - conditions_df (pandas.DataFrame): the conditions dataframe
        - measurement_df (pandas.DataFrame): the measurement dataframe
        - observable_df (pandas.DataFrame): the observable dataframe
        - parameter_df (pandas.DataFrame): the parameters dataframe
        - visualization_df (pandas.DataFrame): the visualization dataframe
        """
        self.yaml_file = yaml_file

        yaml_directory = os.path.join(os.path.dirname(self.yaml_file))

        with open(self.yaml_file, encoding="utf-8", mode="r") as file:
            yaml_dict = yaml.safe_load(file)

        # Construct full paths to petab files based on the YAML file's directory
        self.sbml_file = os.path.join(
            yaml_directory, yaml_dict["problems"][0]["sbml_files"][0]
        )

        self.parameter_df = pd.read_csv(
            os.path.join(yaml_directory, yaml_dict["parameter_file"]), sep="\t"
        )
        self.conditions_df = pd.read_csv(
            os.path.join(
                yaml_directory, yaml_dict["problems"][0]["condition_files"][0]
            ),
            sep="\t",
        )
        self.measurement_df = pd.read_csv(
            os.path.join(
                yaml_directory, yaml_dict["problems"][0]["measurement_files"][0]
            ),
            sep="\t",
        )
        self.observable_df = pd.read_csv(
            os.path.join(
                yaml_directory, yaml_dict["problems"][0]["observable_files"][0]
            ),
            sep="\t",
        )

        # The model specification files detail
        if "model_specification_files" in yaml_dict["problems"][0]:
            model_specs = pd.read_csv(
                os.path.join(
                    yaml_directory,
                    yaml_dict["problems"][0]["model_specification_files"][0],
                ),
                sep="\t",
            )
            self.conditions_df = pd.merge(
                self.conditions_df, model_specs, on="conditionId"
            )

        if "visualization_files" in yaml_dict["problems"][0]:
            self.visualization_df = pd.read_csv(
                os.path.join(
                    yaml_directory, yaml_dict["problems"][0]["visualization_files"][0]
                ),
                sep="\t",
            )


    def __call__(self):
        """
        Performs a series of rule checks on the PEtab files, filling in missing
        attributes with default values if necessary required. 

        Parameters:
        - self: PEtabFileLoader object

        Returns:
        - sbml_file (str): path to the SBML file
        - conditions_df (pandas.DataFrame): the conditions dataframe
        - measurement_df (pandas.DataFrame): the measurement dataframe
        - observable_df (pandas.DataFrame): the observable dataframe
        - parameter_df (pandas.DataFrame): the parameters dataframe
        - visualization_df (pandas.DataFrame): the visualization dataframe
        """
        dataframes = [self.conditions_df, self.measurement_df, 
                      self.observable_df]

        if "visualization_df" in self.__dict__:
            dataframes.append(self.visualization_df)

        for df in dataframes:
            if df is self.conditions_df:
                rule_dict = PEtabFileLoader.conditions_df_rules
            elif df is self.measurement_df:
                rule_dict = PEtabFileLoader.measurement_df_rules
            elif df is self.observable_df:
                rule_dict = PEtabFileLoader.observable_df_rules
            elif df is self.visualization_df:
                rule_dict = PEtabFileLoader.visualization_df_rules

            else:
                raise ValueError(f"Dataframe {df} not recognized")

            df = PEtabRules.eval_df_contents(df, rule_dict)


        return (self.yaml_file, self.sbml_file, self.conditions_df, 
                self.measurement_df, self.observable_df, self.parameter_df,
                self.visualization_df)
