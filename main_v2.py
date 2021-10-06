from time import perf_counter
from typing import List

from app_v2.graph import GraphInstance
from app_v2.methods.grasp import run_grasp
from app_v2.methods.heuristic import Heuristic
from app_v2.methods.io import export_results
from app_v2.methods.rules import TaskOrderingRule
from app_v2.methods.strategies import OptimizationStrategy


def create_instances(quantity: int = 10) -> List[GraphInstance]:
    """Creates up to 10 instances of all possible combinations of graph and variant"""
    
    graphs = [#"ARC83.IN2", "BARTHOLD.IN2", "HESKIA.IN2", "LUTZ2.IN2",
              "MITCHELL.IN2",
              # "ROSZIEG.IN2", "SAWYER30.IN2", "WEE-MAG.IN2"
              ]
    variants = ["TS0.25", "TS0.25-med", "TS0.75", "TS0.75-med"]
    instances = [GraphInstance(graph, variant, ident) for graph in graphs for variant in variants for ident in range(1, quantity+1)]
    
    return instances


def create_heuristics() -> List[Heuristic]:
    """Creates a list of heuristics. These are all possible combinations of optimization strategy and ordering rule"""
    
    strategies = OptimizationStrategy.__subclasses__() # Using __subclasses__ allows for adding a new strategy or rule without having to change the code here
    orderings  = TaskOrderingRule.__subclasses__()          
    heuristics = [Heuristic(strategy(), ordering()) for strategy in strategies for ordering in orderings]
    
    return heuristics


class Experiment:
    """Model an experiment that takes an instance and a Huristic/GRASP"""
    pass


def run_experiments(instances: List[GraphInstance], heuristics: List[Heuristic]):
    
    solutions = {}
    best_solutions = {}
    
    for instance in instances:

        t0 = perf_counter()
        
        # Load the data from the instance's .txt-file
        instance.parse_instance()

        # Apply heuristics to instance
        for heuristic in heuristics:
        
            t1 = perf_counter() 
            solution = heuristic.solve_instance(instance)
            t2 = perf_counter()
            
            runtime = t2-t1
            instance.solutions[heuristic] = {'m': len(solution), 'rt': runtime, 'sol': solution}
            print(f"Solution: {len(solution)}")

        solutions[instance] = instance.solutions

        # print(f"Applying GRASP-5 metaheuristic")
        # t3 = perf_counter()
        # solution = run_grasp(instance)
        # t4 = perf_counter()
        # runtime = t4-t3
        # instance.solutions['GRASP-5'] = {'m': len(solution), 'rt': runtime, 'sol': solution}

        # print(f"Applying GRASP-10 metaheuristic")
        # t5 = perf_counter()
        # solution = run_grasp(instance, num_iter=10)
        # t6 = perf_counter()
        # runtime = t6-t5
        # instance.solutions['GRASP-10'] = {'m': len(solution), 'rt': runtime, 'sol': solution}

        print(f"Postprocessing")
        best_solution = instance.postprocess()
        best_solutions[instance] = best_solution

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
    enable_tests=False
    main(1)
    
    if enable_tests:
        from app_v2.graph import Task
        from app_v2.methods.rules import MaxTSOrdering, MinTSOrdering
        from app_v2.methods.strategies import StationOrientedStrategy, TaskOrientedStrategy
        import random
        import copy
        
        """Test Heuristic Creation"""
        strategy = StationOrientedStrategy()
        print(strategy)
        
        ordering = MinTSOrdering()
        print(ordering)
        
        heuristic = Heuristic(strategy, ordering)
        print(heuristic)
        
        SH_maxTSHeuristic = Heuristic(StationOrientedStrategy(), MaxTSOrdering())
        
        """Test Instance Creation"""
        instance = GraphInstance("MITCHELL.IN2", "TS0.25", 1)
        instance.parse_instance()
        
        # """Solve an instance"""
        # solution1 = SH_maxTSHeuristic.solve_instance(instance)
        # print(len(solution1) )
        # solution2 = heuristic.solve_instance(instance)
        # print(len(solution2))
        
        """Test Task Creation and Removal"""
        task1 = Task(1, random.randint(0, 10))
        task1.predecessors = [0,3,4]
        task2 = Task(2, random.randint(0, 10))
        task2.predecessors = [1,3,4]
        
        # can we remove a task from a list?
        print("Remove task1 from list")
        tasks = [task1, task2]
        print(tasks)
        
        tasks.remove(task1)
        print(tasks)
        
        # can we deepcopy tasks?
        print("Make a deepcopy of task2 and remove predecessor 1")
        task2_copy = copy.deepcopy(task2)
        task2_copy.predecessors.remove(1) 
        print(task2)
        print(task2_copy)
        
        print("Deepcopy a list of tasks and remove predecessor 3 from the first task")
        tasks.append(task1)
        tasks_copy = copy.deepcopy(tasks)
        tasks_copy[0].predecessors.remove(3)
        print(tasks)
        print(tasks_copy)

