import copy
import random
from abc import ABC, abstractmethod
from graph import Graph
from local_search import improve_solution
from rules import TaskOrderingRule
from station import Station
from task import Task
from typing import List


class OptimizationProcedure(ABC):
    """Abstract class that describes procedures by which a SUALBPS problem can be optimized

    We differ between three types of optimization procedures:
        - the Station oriented strategies (SH),
        - the Task oriented strategies (TH), and
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
    def solve(self, instance: Graph):
        pass
    
    @abstractmethod
    def construct_solution(self, candidate_list: List[Task], cycle_time: int) -> List[Station]:
        pass

    def __str__(self):
        return self.__class__.__name__


class StationOrientedStrategy(OptimizationProcedure):
    """The candidate tasks will be assigned to the current station if processing the task
    does not exceed the instances cycle time. Otherwise a new station is opened."""

    def __init__(self, ordering_rule: TaskOrderingRule):
        self.ordering_rule = ordering_rule

    def solve(self, instance: Graph) -> List[Station]:
       
        print(f"Applying {self} with {self.ordering_rule}")
        candidate_list = copy.deepcopy(instance.tasks)
        solution = self.construct_solution(candidate_list, instance.cycle_time)
        return solution
    
    def construct_solution(self, candidate_list: List[Task], cycle_time: int) -> List[Station]:

        # initialize stations
        stations: List[Station] = [Station(cycle_time)]
        current_station = stations[-1]

        while len(candidate_list):

            # Condition 1: tasks have no precedence relations
            candidates = tasks_without_predecessors(candidate_list)

            # Condition 2: tasks fit into the current station
            candidates =  [task for task in candidates if current_station.can_fit(task)]

            # if there are no candidates for the current station open a new empty station
            if not len(candidates):
                stations.append(Station(cycle_time))
                current_station = stations[-1]
                continue

            # order the list of station candidates
            ordered_candidate_value_list = self.ordering_rule.order_tasks(
                candidates, current_station
            )

            # next task to be sequenced is first in the ordered list of candidates
            next_task = ordered_candidate_value_list[0][0]

            # assign the chosen task to the current station and remove it from candidate list
            current_station.append(next_task)
            candidate_list.remove(next_task)

            # Remove the chosen task as a predecessor from all other candidates
            remove_from_predecessors(next_task, candidate_list)

        return stations


class TaskOrientedStrategy(OptimizationProcedure):
    """The task-oriented procedure (TH) is an iterative procedure which, at each iteration and
    according to a priority rule, assigns one of a group of candidate tasks to a workstation.
    A task is considered a candidate once all of its preceding tasks have been assigned. The
    chosen task is assigned to the first workstation in which it can be assigned (provided
    that it fits in the workstation and that all of its preceding tasks have been assigned). All
    of the workstations remain open until all of the tasks have been assigned, at which point
    the procedure ends. [Martino & Pastor (2010), 3.3]

    TODO: Procedure is not working correctly. How should the tasks be ordered if there are
    multiple stations they could be assigned to and the setup may change the ordering?"""

    def __init__(self, ordering_rule: TaskOrderingRule):
        self.ordering_rule = ordering_rule
    
    def solve(self, instance: Graph) -> List[Station]:
       
        print(f"Applying {self} with {self.ordering_rule}")
        candidate_list = copy.deepcopy(instance.tasks)
        solution = self.construct_solution(candidate_list, instance.cycle_time)
        return solution

    def construct_solution(self, candidate_list: List[Task], cycle_time: int) -> List[Station]:

        # initialize stations
        stations: List[Station] = [Station(cycle_time)]
        current_station = stations[-1]

        while len(candidate_list):

            # Condition 1: candidates are tasks that have no precedence relations
            candidate_tasks = tasks_without_predecessors(candidate_list)

            # order the list of station candidates (TODO: what is the correct station argument?)
            ordered_candidate_value_list = self.ordering_rule.order_tasks(
                candidate_tasks, current_station
            )

            # next task to be sequenced is first in the ordered list of candidates
            next_task = ordered_candidate_value_list[0][0]

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
            current_station.append(next_task)
            candidate_list.remove(next_task)

            # Remove the chosen task as a predecessor from all other candidates
            remove_from_predecessors(next_task, candidate_list)

        return stations


class GRASP(OptimizationProcedure):
    """TODO Docstring"""
    
    def __init__(self, num_iter: int):
        self.num_iter = num_iter
    
    def solve(self, instance: Graph) -> List[Station]:
          
        print(f"Applying GRASP-{self.num_iter} Metaheuristic")
    
        for iteration in range(1, self.num_iter + 1):
            
            # get a mutable copy of the original task list
            candidate_list = copy.deepcopy(instance.tasks)
            
            solution = self.construct_solution(candidate_list, instance.cycle_time)
            improved_solution = improve_solution(solution, instance.cycle_time)

            # the best solution has the lowest number of stations
            if iteration == 1:
                best_solution = improved_solution
            elif len(improved_solution) < len(best_solution):
                best_solution = improved_solution

        return best_solution
    
    def construct_solution(self, candidate_list: List[Task], cycle_time: int) -> List[Station]:

        # Initialise solution with one empty station
        stations = [Station(cycle_time)]
        current_station = stations[-1]
        
        while len(candidate_list):

            # Condition 1: candidates are tasks that have no precedence relations
            candidates = tasks_without_predecessors(candidate_list)

            # Condition 2: tasks fit into the current station
            candidates =  [task for task in candidates if current_station.can_fit(task)]
            
            # If no candidates are found then open a new empty station
            if not len(candidates):
                stations.append(Station(cycle_time))
                current_station = stations[-1]
                continue

            # Find candidates that fulfill a threshold condition
            candidates = restricted_candidates(candidates, current_station)        

            # next task to be sequenced is picked randomly from the restricted candidate list
            next_task = random.choice(candidates)

            # assign the next task to the current station and remove it from candidate list
            current_station.append(next_task)
            candidate_list.remove(next_task)

            # Remove the next task as a predecessor from all other candidates
            remove_from_predecessors(next_task, candidate_list)

        return stations


def tasks_without_predecessors(candidates: List[Task]) -> List[Task]:
    """Returns a list of tasks that have no predecessors"""
    return [task for task in candidates if not len(task.predecessors)]


def remove_from_predecessors(next_task: Task, candidate_list: List[Task]) -> None:
    """Removes the precedence relation of a newly sequenced tasked from all other tasks"""
    [task.remove_predecessor(next_task) for task in candidate_list if next_task.is_predecessor(task)]


def greedy(candidate_tasks: List[Task], current_station: Station) -> List[float]:
    """Calculate the greedy index g() for all candidate tasks with respect to the current station"""

    if current_station.empty():
        return [1 / task.processing_time for task in candidate_tasks]
    else:
        return [1 / (current_station[-1].setup_time(task) + task.processing_time) for task in candidate_tasks]
    
    
def get_threshold(greedy_indices: List[float], alpha: float):
    gmin = min(greedy_indices)
    gmax = max(greedy_indices)
    return gmin + alpha * (gmax - gmin)

    
def restricted_candidates(candidates: List[Task], current_station: Station, alpha: float = 0.3):
    # compute the greedy-Index g() for each candidate task
    greedy_indices = greedy(candidates, current_station)

    # Compute threshold function
    threshold = get_threshold(greedy_indices, alpha)
    
    # Find candidates that pass the threshold condition
    return [task for task, greedy_index in zip(candidates, greedy_indices) if greedy_index <= threshold]


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
