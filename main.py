from export import export_instance_result, export_results
from graph import GraphInstance
from rules import TaskOrderingRule
from optimizer import GRASP, OptimizationProcedure, StationOrientedStrategy, TaskOrientedStrategy
from time import perf_counter
from typing import List


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


def create_optimizers() -> List[OptimizationProcedure]:
    """Creates a list of all optimization procedures"""
    
    optimizers: List[OptimizationProcedure] = []
    ordering_rules = TaskOrderingRule.__subclasses__()
    for rule in ordering_rules:
        optimizers.append(StationOrientedStrategy(rule()))
        optimizers.append(TaskOrientedStrategy(rule()))
        
    for num_iter in [5, 10]:
        optimizers.append(GRASP(num_iter))

    return optimizers


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


def run_experiments(instances: List[GraphInstance], strategies: List[OptimizationProcedure]):

    solutions = []
    for instance in instances:
        instance_start = perf_counter()
        instance.parse_instance()

        instance_solutions = []
        for strategy in strategies:

            strat_start = perf_counter()
            stations = strategy.solve(instance)
            strat_end = perf_counter()

            instance_solutions.append({
                'Instance': f"{instance}",
                'Strategy': f"{strategy}",
                'Num_Stations': len(stations),
                "Runtime": strat_end - strat_start
                #TODO: Add the Sequence for export
            })
        
        # Find the solution with the minimum number of stations
        min_stations = best_solution(instance_solutions)
        
        # Add min_stations and compute Average Relative Deviation to each solution
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

    # Create instances and optimization procedures
    instances = create_instances(quantity=num_instances)
    optimizers = create_optimizers()

    # run experiments
    solutions = run_experiments(instances, optimizers)

    # save experiments to disc
    export_results(solutions, filename='all_results')


if __name__ == "__main__":
    main(1)
