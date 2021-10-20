from time import perf_counter
from typing import List

from graph import GraphInstance
from heuristic import Heuristic
from rules import TaskOrderingRule
from strategies import GRASP, OptimizationProcedure, StationOrientedStrategy, TaskOrientedStrategy
from export import export_instance_result, export_results


def create_instances(quantity: int = 10) -> List[GraphInstance]:
    """Creates up to 10 instances of all possible combinations of graph and variant"""

    graphs = [  # "ARC83.IN2", "BARTHOLD.IN2", "HESKIA.IN2", "LUTZ2.IN2",
        "MITCHELL.IN2",
        # "ROSZIEG.IN2", "SAWYER30.IN2", "WEE-MAG.IN2"
    ]
    variants = ["TS0.25", "TS0.25-med", "TS0.75", "TS0.75-med"]
    instances = [
        GraphInstance(graph, variant, ident)
        for graph in graphs
        for variant in variants
        for ident in range(1, quantity + 1)
    ]

    return instances


def create_heuristics() -> List[Heuristic]:
    """Creates a list of heuristics. These are all possible combinations of optimization strategy and ordering rule"""
    
    strategies: List[OptimizationProcedure] = []
    ordering_rules = TaskOrderingRule.__subclasses__()
    for rule in ordering_rules:
        strategies.append(StationOrientedStrategy(rule()))
        strategies.append(TaskOrientedStrategy(rule()))
        
    for num_iter in [5, 10]:
        strategies.append(GRASP(num_iter))
        
    heuristics = [Heuristic(strategy) for strategy in strategies]

    return heuristics


class Experiment:
    """Model an experiment that takes an GraphInstance and a Heuristic/GRASP"""
    pass


def best_solution(instance_solutions: List) -> int:
    """Returns the minimum number of stations from all solutions"""
    return min([solution['Num_Stations'] for solution in instance_solutions])


def compute_ARD(solution_stations: int, min_stations: int) -> float:
    """Compute the average relative deviation of a solution"""
    ARD = 100 * ((solution_stations - min_stations) / min_stations)
    return ARD


def run_experiments(instances: List[GraphInstance], heuristics: List[Heuristic]):

    solutions = []

    for instance in instances:

        instance_start = perf_counter()

        # Load the data from the instance's .txt-file
        instance.parse_instance()

        # Apply heuristics to instance
        instance_solutions = []
        for heuristic in heuristics:

            heuristic_start = perf_counter()
            stations = heuristic.solve_instance(instance)
            heuristic_end = perf_counter()

            heuristic_runtime = heuristic_end - heuristic_start
            instance_solutions.append({
                'Instance': f"{instance}",
                'Heuristic': f"{heuristic}",
                'Num_Stations': len(stations),
                "Runtime": heuristic_runtime
                #TODO: Add the Sequence for export
            })


        print(f"Instance Postprocessing")
        
        # Find the best solution for the instance in terms of the minimum number of stations
        min_stations = best_solution(instance_solutions)
        
        # Add min_stations and compute Average Relative Deviation for each solution
        for solution in instance_solutions:
            solution['Min_Stations'] = min_stations
            solution['ARD'] = compute_ARD(solution['Num_Stations'], min_stations)
        
        solutions.extend(instance_solutions)
        
        # Export the results for this instance to csv
        export_instance_result(instance_solutions, filename=f"{instance}")

        print("Experiment Runtime:", perf_counter() - instance_start)
        print("=" * 50, "\n")

    return solutions


def main(num_instances: int):

    # Create instances and heuristics
    instances = create_instances(quantity=num_instances)
    heuristics = create_heuristics()

    # run experiments
    solutions = run_experiments(instances, heuristics)

    # save experiments to disc
    export_results(solutions, filename='all_results')


if __name__ == "__main__":
    main(1)
