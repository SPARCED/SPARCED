#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


class Visualizer:
    """This class is designed to plot and save the visualization data. The \
    information within the visualization dataframe must conform to PEtab \
    standards.

    Attributes:
        yaml_file: str - path to the YAML file
        results_dict: dict - dictionary containing the simulation results
        visualization_df: str - path to the visualization dataframe
        observable_df: str - path to the observable dataframe
        model: str - path to the SBML model
        measurement_df: str - path to the measurement dataframe
    """


    def __init__(self, yaml_file: str, results_dict: dict, 
                 visualization_df: pd.DataFrame, observable_df: pd.DataFrame,
                   measurement_df: pd.DataFrame):
        """This class is designed to plot and save the visualization data.
        input:
            yaml_file: str - path to the YAML file
            result_dict: dict - dictionary containing the simulation results
            visualization_df: str - path to the visualization dataframe
            observable_df: str - path to the observable dataframe
            model: str - path to the SBML model
            measurement_df: str - path to the measurement dataframe
        """
        self.yaml_file = yaml_file
        self.results_dict = results_dict
        self.visualization_df = visualization_df
        self.observable_df = observable_df
        self.measurement_df = measurement_df


    def dynamic_plot(self):
        """Parses the information within the visualization dataframe and 
        plots simulation data accordingly. Information within the 
        visualization dataframe must conform to PEtab standards.

        output: plots the simulation data according to the visualization dataframe
        """

        # Get unique plots
        unique_plots = self.visualization_df['plotId'].unique()

        num_rows, num_cols, plot_position_matrix = generate_position_matrix(len(unique_plots))
        unique_plt_positions = {}

        for i, plotId in enumerate(unique_plots):
            # Find the position from the matrix
            row, col = np.where(plot_position_matrix == i)
            row, col = row[0], col[0]
            unique_plt_positions[plotId] = (row, col)

        # Set global plot parameters
        plt.rcParams['axes.labelsize'] = 14
        plt.rcParams['xtick.labelsize'] = 12    
        plt.rcParams['ytick.labelsize'] = 12
        plt.rcParams['legend.fontsize'] = 12
        plt.rcParams['font.weight'] = 'bold' 

        # Create a subplot figure with the determined grid size
        fig, axes = plt.subplots(num_rows, num_cols, figsize=(num_cols * 4, num_rows * 4))

        # Ensure axes is always a 2D array
        if num_rows == 1 and num_cols == 1:
            axes = np.array([[axes]])
        elif num_rows == 1 or num_cols == 1:
            axes = axes.reshape((max(num_rows, num_cols),1))

        for i, plotId in enumerate(self.visualization_df['plotId']):
            # Get the plot information
            plot_info = self.condense_plot_information(i)

            # Find the position from the matrix
            row, col = unique_plt_positions[plotId]

            identifier = self.retrieve_identifier(plot_info['datasetId'], self.results_dict)
            attribute = plot_info['yValues'] # refers to PEtab observableId

            # Add experimental data to the plot_info dictionary if it exists
            plot_info = self.build_experiment_plot_information(plot_info, attribute, identifier)

            # Swap the attribute for the actual data
            plot_info['xValues'] = self.swap_attribute_for_data(identifier, plot_info['xValues'])
            plot_info['yValues'] = self.swap_attribute_for_data(identifier, attribute)

         

            if plot_info['plotTypeSimulation'] == 'ScatterPlot':
                self.scatter_plot(axes, plot_info, row, col, identifier)  

            elif plot_info['plotTypeSimulation'] == 'LinePlot':
                self.line_plot(axes, plot_info, row, col, identifier)  

            elif plot_info['plotTypeSimulation'] == 'BarPlot':
                self.bar_plot(axes, plot_info, row, col, identifier)             

            axes[row, col].set_xlabel(plot_info['xLabel'], weight='bold')
            axes[row, col].set_ylabel(plot_info['yLabel'], weight='bold')
            axes[row, col].set_xscale(plot_info['xScale'])
            axes[row, col].set_yscale(plot_info['yScale'])
            axes[row, col].set_title(plot_info['plotName'], weight='bold')

        # Remove unused subplots
        for i in range(len(unique_plots), num_rows * num_cols):
            row, col = np.where(plot_position_matrix == i)
            row, col = row[0], col[0]

            fig.delaxes(axes[row, col])

        # Get unique handles and labels for the legend
        lines_labels = [ax.get_legend_handles_labels() for ax in fig.axes]
        unique_lines = []
        unique_labels = set()
        for lines, labels in lines_labels:
            for line, label in zip(lines, labels):
                if label not in unique_labels:
                    unique_lines.append(line)
                    unique_labels.add(label)
                else:
                    idx = list(unique_labels).index(label)
                    if unique_lines[idx] != line:
                        unique_lines[idx] = line

        # # Adjust layout
        plt.tight_layout()

        return fig


    def condense_plot_information(self, ith_plotId: pd.Series) -> dict:
        """ Iterates over the eval_column_contents function to condense the
        plot information into a dictionary. Dictionary is then sent to each 
        plotting function to generate the plots.
        
        Parameters: 
        - ith_plotId (pd.Series): series containing the plotId
            
        Returns:
        - plot_information (dict): dictionary containing the plot information
        """

        scale_dict = {'lin': 'linear', 'log10': 'log'}

        plot_information = {}
        # Turn the i'th row in the visualization dataframe into a dictionary
        for column in self.visualization_df.columns:
            plot_information[column] = self.visualization_df[column][ith_plotId]

        # Swap the 'lin' attribute for 'linear'
        plot_information['xScale'] = scale_dict[plot_information['xScale']]
        plot_information['yScale'] = scale_dict[plot_information['yScale']]

        return plot_information


    def swap_attribute_for_data(self, identifier: str, attribute: dict.items):
        """Swaps the attribute in the plot_info dict for the actual data in the 
        results_dict.
        
        Parameters:
        - identifier (str): identifier
        - attribute (dict.items): attribute

        Returns:
            data: dict - data
        """
        if attribute == 'time':
            data = self.results_dict[identifier][attribute]
        else:
            data = self.results_dict[identifier][f'simulation {attribute}']

        return data


    def retrieve_identifier(self, datasetId: str, results_dict: dict) -> str:
        """ Retrieves the identifier from the either the visualization dataframe\
        or the results dictionary, dependent on if the identifier is in the\
        results dictionary or not.
        
        Parameters:
        - datasetId (str): datasetId
        - results_dict (dict): results dictionary

        Returns:
        - identifier (str): identifier
        """
        if datasetId in results_dict.keys():
            identifier = datasetId
        else:
            identifier = ([key for key in results_dict.keys() if results_dict[key]['conditionId'] == datasetId][0])

        return identifier


    def build_experiment_plot_information(self, plot_info:dict,
                                          attribute: dict.items,
                                           identifier: str) -> dict:
        """
        The observable_calculator function pairs simulation observables with \
        experimental data. Since it's not that intelligent, it differentiates via\
        'simulation' and 'experiment' added onto the beginning of the observableId. \
        This function will update a simulation's plot_info dictionary with the \
        experimental data.
        
        Parameters:
        - identifier (str): condition identifier
        - attribute (dict.items): observableId attribute
        - plot_info (dict): dictionary containing the plot information

        Returns:
        - plot_info (dict): dictionary containing the plot information
        """

        # conditional to check if the experiment data exists
        if f'experiment {attribute}' in self.results_dict[identifier].keys():
            plot_info['Exp yValues'] = self.results_dict[identifier][f'experiment {attribute}']
            plot_info['Exp Color'] = 'black'
            plot_info['Exp legendEntry'] = 'experiment'

        return plot_info


    # def replicate_plot_settings(ax, replicate: int)-> plt.axis:
    #     """Provided a replicate, reassigns the specific attributes of the plot
    #     to have a lower alpha value, and a smaller linewidth.
        
    #     Parameters:
    #         ax: plt.axis - axis object
    #         replicate: int - replicate number
        
    #     Returns:
    #         ax: plt.axis - axis object with updated settings
    #     """
    #     ax.lines[replicate].set_alpha(0.5)
    #     ax.lines[replicate].set_linewidth(1)
    
        # return ax
        

    def scatter_plot(self, ax: plt.axis, row: int, col: int,
                     plot_info: dict, identifier: str) -> plt.axis:
        """Generates a scatter plot based on the provided parameters. Inspects 
        plot_info for experimental data and pairs it with the simulation data in 
        the same plot.
        
        Parameters:
        - ax (plt.axis): axis object
        - plot_info (dict): dictionary containing the plot information
        - identifier (str): PEtab conditionId identifier
    
        Returns:
        - ax (plt.axis) - axis object
        """
        ax[row, col].scatter(plot_info['xValues'], plot_info['yValues'], 
                            label=plot_info['legendEntry'], 
                            color=plot_info['Color'], 
                            linewidth=3)

        if 'Exp yValues' in plot_info.keys():
            ax[row, col].scatter(plot_info['xValues'], plot_info['Exp yValues'], 
                                label=plot_info['Exp legendEntry'], 
                                color=plot_info['Exp Color'], 
                                linewidth=3)
            
        ax[row, col].legend(loc='best', frameon=False)


    def line_plot(self, ax: plt.axis, plot_info: dict, row: int, col: int,
                   identifier: str) -> plt.axis:
        """Generates a line plot based on the provided parameters
        
        Parameters:
        - ax (plt.axis): axis object
        - plot_info (dict): dictionary containing the plot information
        - identifier (str): PEtab conditionId identifier
        
        Returns:
        - ax (plt.axis) - axis object
        """
        ax[row, col].plot(plot_info['xValues'], plot_info['yValues'],
                          label=plot_info['legendEntry'],
                          color=plot_info['Color'],
                          linewidth=3)
        
        if 'Exp yValues' in plot_info.keys():
            ax[row, col].plot(plot_info['xValues'], plot_info['Exp yValues'], 
                              label=plot_info['Exp legendEntry'], 
                              color=plot_info['Exp Color'], 
                              linewidth=3)
            
        ax[row, col].legend(loc='best', frameon=False)


    def bar_plot(self, ax: plt.axis, plot_info: dict, row: int, col: int,
                 identifier: str) -> plt.axis:
        """Generates a bar plot based on the provided parameters

        Parameters:
        - ax (plt.axis): axis object
        - plot_info (dict): dictionary containing the plot information
        - identifier (str): PEtab conditionId identifier

        Returns:
        - ax (plt.axis) - axis object
        """
        ax[row, col].bar(plot_info['xValues'], plot_info['yValues'],
                         label=plot_info['legendEntry'],
                         color=plot_info['Color'])
        
        if 'Exp yValues' in plot_info.keys():
            ax[row, col].bar(plot_info['xValues'], plot_info['Exp yValues'], 
                             label=plot_info['Exp legendEntry'], 
                             color=plot_info['Exp Color'],
                                alpha=0.5)

        ax[row, col].legend(loc='best', frameon=False)

@staticmethod
def generate_position_matrix(num_plots):
    """Generates a position matrix based on the number of plots to be generated
    input:
        num_plots: int - number of plots to be generated

    output:
        num_rows: int - number of rows in the plot grid
        num_cols: int - number of columns in the plot grid
        position_matrix: np.array - matrix containing the position of each plot
            in the grid
    """

    side_length = int(np.ceil(np.sqrt(num_plots)))
    
    position_matrix = np.arange(side_length ** 2).reshape((side_length,
                                                            side_length)).T
    
    num_rows, num_cols = position_matrix.shape

    return num_rows, num_cols, position_matrix
