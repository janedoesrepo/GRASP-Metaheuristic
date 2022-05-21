import copy
import random

from sualbsp_solver.data_model.graph import Graph
from sualbsp_solver.data_model.station import Station
from sualbsp_solver.data_model.task_list import TaskList
from sualbsp_solver.solver.local_search import improve_solution
from sualbsp_solver.solver.optimizer import OptimizationProcedure


class GRASP(OptimizationProcedure):
    """TODO Docstring"""

    def __init__(self, num_iter: int) -> None:
        self.num_iter = num_iter

    def solve(self, instance: Graph) -> list[Station]:
        print(f"Applying GRASP-{self.num_iter} Metaheuristic")

        best_solution: list[Station] = []
        for iteration in range(1, self.num_iter + 1):
            # get a mutable copy of the original task list
            candidate_list = TaskList(copy.deepcopy(instance.tasks))

            solution = self.construct_solution(candidate_list, instance.cycle_time)
            improved_solution = improve_solution(solution, instance.cycle_time)

            # the best solution has the lowest number of stations
            if iteration == 1:
                best_solution = improved_solution
            elif len(improved_solution) < len(best_solution):
                best_solution = improved_solution

        return best_solution

    def construct_solution(
        self, candidate_list: TaskList, cycle_time: int
    ) -> list[Station]:
        """Takes a `candidate_list` and assigns them to Stations with `cycle_time`.

        TODO: self is never used
        """

        # Initialise solution with one empty station
        stations = [Station(cycle_time)]
        current_station = stations[-1]

        while len(candidate_list):

            # Condition 1: candidates are tasks that have no precedence relations
            candidates = candidate_list.get_tasks_without_predecessors()

            # Condition 2: tasks fit into the current station
            candidates = candidates.get_tasks_that_fit_station(current_station)

            # if there are no candidates for the current station open a new empty station
            if not len(candidates):
                stations.append(Station(cycle_time))
                current_station = stations[-1]
                continue

            # compute the greedy-Index g() for each candidate task
            greedy_indices = self.get_greedy_indices(candidates, current_station)

            # Compute threshold function
            threshold = self.get_threshold(greedy_indices, alpha=0.3)

            # Find candidates that fulfill a threshold condition
            restricted_candidates = self.get_restricted_candidates(
                candidates, greedy_indices, threshold
            )

            # next task to be sequenced is picked randomly from the restricted candidate list
            next_task = random.choice(restricted_candidates)

            # assign the next task to the current station and remove it from candidate list
            current_station.add_task(next_task)
            candidate_list.remove(next_task)

            # Remove the next task as a predecessor from all other candidates
            candidate_list.remove_from_predecessors(next_task)

        return stations

    def get_greedy_indices(
        self, tasks: TaskList, current_station: Station
    ) -> list[float]:
        """Calculate the greedy index g() for all candidate tasks with respect to the current station"""
        if current_station.empty():
            return [1 / task.processing_time for task in tasks]
        else:
            return [
                1 / (current_station[-1].setup_time(task) + task.processing_time)
                for task in tasks
            ]

    def get_threshold(self, greedy_indices: list[float], alpha: float) -> float:
        gmin = min(greedy_indices)
        gmax = max(greedy_indices)
        return gmin + alpha * (gmax - gmin)

    def get_restricted_candidates(
        self, tasks: TaskList, greedy_indices: list[float], threshold: float
    ) -> TaskList:

        # Find candidates that pass the threshold condition
        return TaskList(
            [
                task
                for task, greedy_index in zip(tasks, greedy_indices)
                if greedy_index <= threshold
            ]
        )
