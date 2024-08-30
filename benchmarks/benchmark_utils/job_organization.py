import mpi4py.MPI as MPI
from benchmark_utils.petab_file_loader import PEtabFileLoader
from benchmark_utils.utils import Utils
import pandas 
import numpy


class Organizer:
    """This class contains functions that organize the tasks for the MPI processes
    """

    def mpi_communicator():
        """This function initializes the MPI communicator
        Input:
            None
        Output:
            comm: MPI communicator - the MPI communicator
        """

        communicator = MPI.COMM_WORLD
        rank = communicator.Get_rank()
        size = communicator.Get_size()

        return communicator, rank, size


    def broadcast_petab_files(rank: int, communicator: MPI.Comm, 
                            yaml_file: str, model_path: str):

        if rank == 0:
            petab_files = PEtabFileLoader(yaml_file, model_path).__call__()
            petab_files_data = {
                'sbml_file': petab_files.sbml_file,
                'conditions_df': petab_files.conditions_df,
                'measurement_df': petab_files.measurement_df,
                'observable_df': petab_files.observable_df,
                'parameter_df': petab_files.parameter_df,
                'visualization_df': petab_files.visualization_df
            }

            sbml_file = petab_files_data['sbml_file']
            conditions_df = petab_files_data['conditions_df']
            measurement_df = petab_files_data['measurement_df']
            observable_df = petab_files_data['observable_df']
            parameters_df = petab_files_data['parameter_df']

            visualization_df = petab_files_data['visualization_df'] if 'visualization_df' in petab_files_data else None
                
        else:
            petab_files_data = None
            # Broadcasting from root avoids Race Conditions
        petab_files_data = communicator.bcast(petab_files_data, root=0)

        if rank != 0:
            sbml_file = petab_files_data['sbml_file']
            conditions_df = petab_files_data['conditions_df']
            measurement_df = petab_files_data['measurement_df']
            observable_df = petab_files_data['observable_df']
            parameters_df = petab_files_data['parameter_df']

            visualization_df = petab_files_data['visualization_df'] if 'visualization_df' in petab_files_data else None

        return sbml_file, conditions_df, measurement_df, observable_df, parameters_df, visualization_df


    def task_organization(rank: int, size: int, communicator: MPI.Comm, 
                        conditions_df: pandas.DataFrame, measurement_df: pandas.DataFrame):
        """This function assigns tasks to each rank
        Input:
            rank: int - the rank of the MPI process
            size: int - the number of MPI processes
            n_tasks: int - the number of tasks to be distributed
        Output:
            task_list: list - the list of tasks assigned to the rank
        """

        list_of_jobs = Utils._total_tasks(conditions_df, measurement_df)

        total_jobs = len(list_of_jobs)

        rank_jobs_directory = {}

        for i in range(size):

            start_cell, end_cell = Utils._assign_tasks(i, total_jobs, size)
            
            rank_jobs_directory[i] = list_of_jobs[start_cell:end_cell]
            
        # Assign each rank it's task for the round
        rounds_to_complete = Utils._number_of_rounds(total_jobs, size)
        
        return rounds_to_complete, rank_jobs_directory


    def task_assignment(rank: int, size: int, communicator: MPI.Comm,
                        rank_jobs_directory: dict, round_i: int, 
                        conditions_df: pandas.DataFrame, measurement_df: pandas.DataFrame):


        _, rank_jobs_directory = Organizer.task_organization(rank, size, communicator,
                                                                conditions_df, measurement_df) 
        if rank == 0:
            # Assign each rank it's task for the round
            for i in range(size):

                rank_jobs = rank_jobs_directory[i]

                if round_i < len(rank_jobs):
                    rank_job_for_round = rank_jobs[round_i]

                else:
                    rank_job_for_round = None

                communicator.send(rank_job_for_round, dest=i, tag=round_i)
        

        # Receive the task for the round
        rank_task = communicator.recv(source=0, tag=round_i)

        communicator.Barrier()

        return rank_task


    def package_results(xoutS: numpy.array, toutS: numpy.array, 
                        xoutG: numpy.array, condition_id: str, cell: str) -> None:
        """
        This function gathers all of the results from the simulation into a single 
        dictionary to simplify the process of sending the results to the root rank
        
        Input:
            xoutS: numpy.array - the simulation results for the state variables
            toutS: numpy.array - the time points for the state variables
            xoutG: numpy.array - the simulation results for the gene expression variables
            condition_id: str - the condition identifier
            cell: str - the cell identifier
            
        Output:
            rank_results: dict - the results dictionary for the rank
        """
        
        rank_results = {'condition_name': condition_id,
                                'cell': cell,
                                'xoutS': xoutS,
                                'toutS': toutS,
                                'xoutG': xoutG
                        }
        
        return rank_results


    def results_aggregation(size: int, communicator,
                            results_dict: dict, round_i: int, total_jobs: int):
        """This function aggregates the results from the ranks and
        stores them in the final simulation results dictionary
        
        Input:
            size: int - the number of MPI processes
            communicator: MPI communicator - the MPI communicator
            results: dict - the results dictionary
            results: dict - the results dictionary
            round_i: int - the current round
            total_jobs: int - the total number of jobs
            
            Output:
                results_dict: dict - the results dictionary"""

        # Determine the number of tasks to be completed this round, subtract 1
        # to account for the root rank saving results prior. 
        tasks_this_round = Utils._tasks_this_round(size, total_jobs, round_i) - 1

        completed_tasks = 0

        while completed_tasks < tasks_this_round:

            results = communicator.recv(source=MPI.ANY_SOURCE, tag = MPI.ANY_TAG)

            results_dict = Organizer.results_storage(results, results_dict)

            completed_tasks += 1

            if completed_tasks == tasks_this_round:
                break

        return results_dict
    
    
    def results_storage(results_catalogue: dict, results_dict: dict) -> dict:
        """This function stores the results in the results dictionary
        
        Input:
            results_catalogue: dict - the results catalogue
            results_dict: dict - the results dictionary
            
        Output:
            results_dict: dict - the results dictionary"""

        condition_id = results_catalogue['condition_name']
        cell = results_catalogue['cell']
        results_dict[condition_id][f'cell {cell}']['xoutS'] = results_catalogue['xoutS']
        results_dict[condition_id][f'cell {cell}']['toutS'] = results_catalogue['toutS']
        results_dict[condition_id][f'cell {cell}']['xoutG'] = results_catalogue['xoutG']

        return results_dict
    
    def results_storage2(results_catalogue: dict, results_dict: dict) -> dict:
        """This function stores the results in the results dictionary
        
        Input:
            results_catalogue: dict - the results catalogue
            results_dict: dict - the results dictionary
            
        Output:
            results_dict: dict - the results dictionary"""

        condition_id = results_catalogue['condition_name']
        cell = results_catalogue['cell']
        results_dict[f'{condition_id}_{cell}']['xoutS'] = results_catalogue['xoutS']
        results_dict[f'{condition_id}_{cell}']['toutS'] = results_catalogue['toutS']
        results_dict[f'{condition_id}_{cell}']['xoutG'] = results_catalogue['xoutG']
        results_dict[f'{condition_id}_{cell}']['condition_name'] = condition_id
        results_dict[f'{condition_id}_{cell}']['cell'] = cell


        return results_dict