from time import perf_counter
import xlsxwriter

from app_v2.graph import GraphInstance
from app_v2.methods.heuristic import Heuristic
from app_v2.methods.grasp import run_grasp
from typing import List

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
    """Creates a list of heuristics of all possible combinations of optimization strategy and ordering rule"""
    
    """With __subclasses__ we can add a new strategies and rules without having to change the code here"""
    strategies = OptimizationStrategy.__subclasses__()
    orderings  = TaskOrderingRule.__subclasses__()          
    heuristics = [Heuristic(strategy(), ordering()) for strategy in strategies for ordering in orderings]
    
    return heuristics


def export_results(solutions, best_solutions) -> None:
    """Writes the solutions to an excel workbook"""
    
    print("Writing all results to results.xlsx")
    # create a workbook and a worksheet
    workbook = xlsxwriter.Workbook('app_v2/results/all_results.xlsx')
    worksheet = workbook.add_worksheet()

    # write headers in bold
    bold = workbook.add_format({'bold': 1})
    worksheet.write('A1', 'Instance', bold)
    worksheet.write('B1', 'Heuristic', bold)
    worksheet.write('C1', 'Stations', bold)
    worksheet.write('D1', 'BS', bold)
    worksheet.write('E1', 'ARD', bold)
    worksheet.write('F1', 'Runtime', bold)

    row = 1
    for instance, apply_heuristic in solutions.items():
        for heuristic, solution in apply_heuristic.items():
            worksheet.write_string(row, 0, instance)
            worksheet.write_string(row, 1, heuristic)
            worksheet.write_number(row, 2, solution['m'])
            worksheet.write_number(row, 3, best_solutions[instance])
            worksheet.write_number(row, 4, solution['ARD'])
            worksheet.write_number(row, 5, solution['rt'])
            row += 1

    workbook.close()


def run_experiments(instances: List[GraphInstance], heuristics: List[Heuristic]):
    
    solutions = {}
    best_solutions = {}
    
    for instance in instances:

        t0 = perf_counter()
        instance.load()

        # Apply heuristics to instance
        for heuristic in heuristics:
            print(f"Applying {heuristic.name} to instance {instance.name}")
            t1 = perf_counter()
            solution = heuristic.apply(instance)
            t2 = perf_counter()
            runtime = t2-t1
            instance.solutions[heuristic.name] = {'m': len(solution), 'rt': runtime, 'sol': solution}

        solutions[instance.name] = instance.solutions

        print(f"Applying GRASP-5 meta heuristic to {instance.name}")
        t3 = perf_counter()
        solution = run_grasp(instance)
        t4 = perf_counter()
        runtime = t4-t3
        instance.solutions['GRASP-5'] = {'m': len(solution), 'rt': runtime, 'sol': solution}

        print(f"Applying GRASP-10 meta heuristic to {instance.name}")
        t5 = perf_counter()
        solution = run_grasp(instance, num_iter=10)
        t6 = perf_counter()
        runtime = t6-t5
        instance.solutions['GRASP-10'] = {'m': len(solution), 'rt': runtime, 'sol': solution}

        print(f"Postprocessing {instance.name}")
        best_solution = instance.postprocess()
        best_solutions[instance.name] = best_solution

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