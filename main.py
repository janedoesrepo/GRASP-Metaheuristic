import exporter
from graph import Graph
from optimizer import GRASP, OptimizationProcedure, StationOrientedStrategy, TaskOrientedStrategy
from rules import TaskOrderingRule
from time import perf_counter
from typing import Dict, List


def create_instances(quantity: int = 10) -> List[Graph]:
    """Creates up to 10 instances of all possible combinations of graph and variant"""

    graphs = [
        # "ARC83.IN2", "BARTHOLD.IN2", "HESKIA.IN2", "LUTZ2.IN2",
        "MITCHELL.IN2",
        # "ROSZIEG.IN2", "SAWYER30.IN2", "WEE-MAG.IN2"
    ]
    variants = ["TS0.25", "TS0.25-med", "TS0.75", "TS0.75-med"]
    instances = [
        Graph(graph, variant, ident)
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
    """Model an experiment that takes an Graph instance and an optimizer"""
    start_time: float = 0.
    solutions: List[Dict] = []
    
    def run(self, instance: Graph, optimizers: List[OptimizationProcedure]):
        self.start_time = perf_counter()
        for optimizer in optimizers:
            optimizer_start = perf_counter()
            stations = optimizer.solve(instance)

            self.solutions.append({
                'Instance': f"{instance}",
                'Strategy': f"{optimizer}",
                'Num_Stations': len(stations),
                "Runtime": perf_counter() - optimizer_start
                #TODO: Add the Sequence for export
            })
        
        # Add best solution and compute Average Relative Deviation to each solution
        best_solution = self.best_solution()
        for solution in self.solutions:
            solution['Min_Stations'] = best_solution
            solution['ARD'] = self.compute_ARD(solution['Num_Stations'], solution['Min_Stations'])     
            
    def best_solution(self) -> int:
        """Returns the minimum number of stations from all solutions"""
        return min(solution['Num_Stations'] for solution in self.solutions)

    @staticmethod
    def compute_ARD(solution_stations: int, min_stations: int) -> float:
        """Compute the average relative deviation of a solution"""
        ARD = 100 * ((solution_stations - min_stations) / min_stations)
        return ARD


def run_experiments(instances: List[Graph], optimizers: List[OptimizationProcedure]):

    solutions = []
    for instance in instances:
        instance.parse_instance()

        experiment = Experiment()
        experiment.run(instance, optimizers)
        exporter.export_instance_result(experiment.solutions, filename=f"{instance}")    
        
        solutions.extend(experiment.solutions)

        print("Experiment Runtime:", perf_counter() - experiment.start_time)
        print("=" * 50, "\n")

    return solutions


def main(num_instances: int):

    # Create instances and optimization procedures
    instances = create_instances(quantity=num_instances)
    optimizers = create_optimizers()

    # run experiments
    results = run_experiments(instances, optimizers)

    # save experiments to disc
    exporter.export_results(results, filename='all_results')


if __name__ == "__main__":
    main(1)
