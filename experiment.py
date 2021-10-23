from graph import Graph
from optimizer import OptimizationProcedure
from time import perf_counter
from typing import Dict, List


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
    