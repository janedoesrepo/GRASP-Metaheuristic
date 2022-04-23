import copy
import random
from abc import ABC, abstractmethod
from typing import List

from data_model import Graph, Station, TaskList

from solver.local_search import improve_solution
from solver.rule import TaskOrderingRule


class OptimizationProcedure(ABC):
    """Abstract class that describes procedures by which a SUALBPS problem can be optimized

    We differ between three types of optimization procedures:
        - the Station oriented strategy (SH),
        - the Task oriented strategy (TH), and
        - the GRASP Metaheuristics

    Ordering rules for candidate selection are:
        - Maximum setup time plus processing times (MaxTS)
        - Minimum setup time plus processing times (MinTS)
        - Maximum setup times (MaxS)
        - Minimum setup times (MinS)

    When we refer to strategy SH-MaxTS, we mean a station oriented strategy that selects next candidate tasks
    (those whose predecessors have already been assigned and can fit in the actual open station) by the
    MAXimum processing time plus setup time.

    Hence, the list of optimization pocedures that have been defined and tested are:
        - SH-MaxTS, SH-MaxS, SH-MinTS, SH-MinS and
        - TH-MaxTS, TH-MaxS, TH-MinTS, TH-MinS as well as
        - GRASP-5, GRASP-10
    """

    @abstractmethod
    def solve(self, instance: Graph) -> List[Station]:
        pass
    
    @abstractmethod
    def construct_solution(self, candidate_list: TaskList, cycle_time: int) -> List[Station]:
        pass

    def __str__(self) -> str:
        return self.__class__.__name__


class StationOrientedStrategy(OptimizationProcedure):
    """The candidate tasks will be assigned to the current station if processing the task
    does not exceed the instances cycle time. Otherwise a new station is opened."""

    def __init__(self, ordering_rule: TaskOrderingRule) -> None:
        self.ordering_rule = ordering_rule

    def solve(self, instance: Graph) -> List[Station]:
       
        print(f"Applying {self} with {self.ordering_rule}")
        task_list = TaskList(copy.deepcopy(instance.tasks))
        solution = self.construct_solution(task_list, instance.cycle_time)
        return solution
    
    def construct_solution(self, task_list: TaskList, cycle_time: int) -> List[Station]:

        # initialize stations
        stations: List[Station] = [Station(cycle_time)]
        current_station = stations[-1]

        while len(task_list):

            # Condition 1: tasks have no precedence relations
            candidates = task_list.without_predecessors()

            # Condition 2: tasks fit into the current station
            candidates = candidates.that_fit(current_station)

            # if there are no candidates for the current station open a new empty station
            if not len(candidates):
                stations.append(Station(cycle_time))
                current_station = stations[-1]
                continue

            # order the list of station candidates
            ordered_candidates = self.ordering_rule.order_tasks(
                candidates, current_station
            )

            # next task to be sequenced is first in the ordered list of candidates
            next_task = ordered_candidates[0]

            # assign the chosen task to the current station and remove it from candidate list
            current_station.add_task(next_task)
            task_list.remove(next_task)

            # Remove the chosen task as a predecessor from all other candidates
            task_list.remove_from_predecessors(next_task)

        return stations


class TaskOrientedStrategy(OptimizationProcedure):
    """The task-oriented procedure (TH) is an iterative procedure which, at each iteration and
    according to a priority rule, assigns one of a group of candidate tasks to a workstation.
    A task is considered a candidate once all of its preceding tasks have been assigned. The
    chosen task is assigned to the first workstation in which it can be assigned (provided
    that it fits in the workstation and that all of its preceding tasks have been assigned). All
    of the workstations remain open until all of the tasks have been assigned, at which point
    the procedure ends. [Martino & Pastor (2010), 3.3]

    TODO: Procedure seems to not be working correctly. How should the tasks be ordered if there are
    multiple stations they could be assigned to and the setup may change the ordering?"""

    def __init__(self, ordering_rule: TaskOrderingRule) -> None:
        self.ordering_rule = ordering_rule
    
    def solve(self, instance: Graph) -> List[Station]:
       
        print(f"Applying {self} with {self.ordering_rule}")
        task_list = TaskList(copy.deepcopy(instance.tasks))
        solution = self.construct_solution(task_list, instance.cycle_time)
        return solution

    def construct_solution(self, task_list: TaskList, cycle_time: int) -> List[Station]:

        # initialize stations
        stations: List[Station] = [Station(cycle_time)]
        current_station = stations[-1]

        while len(task_list):

            # Condition 1: candidates are tasks that have no precedence relations
            candidates = task_list.without_predecessors()

            # order the list of station candidates
            ordered_candidates = self.ordering_rule.order_tasks(
                candidates, current_station
            )

            # next task to be sequenced is first in the ordered list of candidates
            next_task = ordered_candidates.first

            # assign next task to first station it fits in
            for station in stations:
                if not station.can_fit(next_task):
                    continue
                break
            else:
                # in case for-loop did not encounter a break-statement, else is invoked.
                # the chosen task did not fit in any open station -> open a new station
                stations.append(Station(cycle_time))  # open new station
                current_station = stations[-1]

            # assign the chosen task to the current station and remove it from candidate list
            current_station.add_task(next_task)
            task_list.remove(next_task)

            # Remove the chosen task as a predecessor from all other candidates
            task_list.remove_from_predecessors(next_task)

        return stations


class GRASP(OptimizationProcedure):
    """TODO Docstring"""
    
    def __init__(self, num_iter: int) -> None:
        self.num_iter = num_iter
    
    def solve(self, instance: Graph) -> List[Station]:         
        print(f"Applying GRASP-{self.num_iter} Metaheuristic")

        best_solution: List[Station] = []
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
    
    def construct_solution(self, candidate_list: TaskList, cycle_time: int) -> List[Station]:
        """TODO: self is never used"""
        # Initialise solution with one empty station
        stations = [Station(cycle_time)]
        current_station = stations[-1]
        
        while len(candidate_list):

            # Condition 1: candidates are tasks that have no precedence relations
            candidates = candidate_list.without_predecessors()

            # Condition 2: tasks fit into the current station
            candidates = candidates.that_fit(current_station)
            
            # if there are no candidates for the current station open a new empty station
            if not len(candidates):
                stations.append(Station(cycle_time))
                current_station = stations[-1]
                continue

            # Find candidates that fulfill a threshold condition
            restricted_candidates = candidates.restricted_candidates(current_station)        

            # next task to be sequenced is picked randomly from the restricted candidate list
            next_task = random.choice(restricted_candidates)

            # assign the next task to the current station and remove it from candidate list
            current_station.add_task(next_task)
            candidate_list.remove(next_task)

            # Remove the next task as a predecessor from all other candidates
            candidate_list.remove_from_predecessors(next_task)

        return stations

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
