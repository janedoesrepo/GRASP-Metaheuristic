from time import perf_counter
from typing import List

from app_v2.graph import GraphInstance
from app_v2.grasp import run_grasp
from app_v2.heuristic import Heuristic
from app_v2.io import export_instance_result, export_results
from app_v2.rules import TaskOrderingRule
from app_v2.strategies import OptimizationStrategy


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

    strategies = OptimizationStrategy.__subclasses__()
    orderings = TaskOrderingRule.__subclasses__()
    heuristics = [
        Heuristic(strategy(), ordering())
        for strategy in strategies
        for ordering in orderings
    ]

    return heuristics


class Experiment:
    """Model an experiment that takes an GraphInstance and a Heuristic/GRASP"""
    pass


def compute_ARD(solution_stations: int, min_stations: int) -> float:
    """Compute the average relative deviation of a solution"""
    ARD = 100 * ((solution_stations - min_stations) / min_stations)
    return ARD


def run_experiments(instances: List[GraphInstance], heuristics: List[Heuristic]):

    solutions = []
    best_solutions = {}

    for instance in instances:

        t0 = perf_counter()

        instance_solutions = {}
        # Load the data from the instance's .txt-file
        instance.parse_instance()

        # Apply heuristics to instance
        for heuristic in heuristics:

            t1 = perf_counter()
            stations = heuristic.solve_instance(instance)
            t2 = perf_counter()

            heuristic_runtime = t2 - t1
            instance_solutions[f"{heuristic}"] = {
                'Instance': f"{instance}",
                'Heuristic': f"{heuristic}",
                'Num_Stations': len(stations),
                "Runtime": heuristic_runtime,
            }
        
        # Apply GRASP to instance
        iterations = [5, 10]

        for num_iterations in iterations:
            print(f"Applying GRASP-{num_iterations} Metaheuristic")

            grasp_start = perf_counter()
            stations = run_grasp(instance)
            grasp_end = perf_counter()

            grasp_runtime = grasp_end - grasp_start
            instance_solutions[f"GRASP-{num_iterations}"] = {
                'Instance': f"{instance}",
                'Heuristic': f"GRASP-{num_iterations}",
                'Num_Stations': len(stations),
                "Runtime": grasp_runtime,
            }

 
        print(f"Postprocessing")
        # Find the best solution for the instance in terms of the minimum number of stations
        min_stations = min([result['Num_Stations'] for _, result in instance_solutions.items()])
        
        # compute Average Relative Deviation for each solution
        for _, result in instance_solutions.items():
            result['Min_Stations'] = min_stations
            result['ARD'] = compute_ARD(result['Num_Stations'], min_stations)
        
        # Export the results for this instance to csv
        export_instance_result(f"{instance}", instance_solutions)
        
        best_solutions[f"{instance}"] = min_stations

        print("Experiment Runtime:", perf_counter() - t0)
        print("-" * 25, "\n")

    return solutions, best_solutions


def main(num_instances: int):

    # Create instances and heuristics
    instances = create_instances(quantity=num_instances)
    heuristics = create_heuristics()

    # run experiments
    solutions, best_solutions = run_experiments(instances, heuristics)

    # save experiments to disc
    export_results(solutions, best_solutions)


if __name__ == "__main__":
    main(1)
