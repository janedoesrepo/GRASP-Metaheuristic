from time import perf_counter
import xlsxwriter

from datahandler.Instance import create_instances
from methods.Heuristic import create_heuristics
from methods.grasp import run_grasp


def main():
    print('-'*25)

    instances = create_instances()
    heuristics = create_heuristics()

    # run experiments
    solutions = {}
    best_solutions = {}
    for instance in instances:

        t0 = perf_counter()
        instance.load()

        for heuristic in heuristics:
            print(f"Applying {heuristic.name} to instance {instance.name}")
            t1 = perf_counter()
            solution = heuristic.apply(instance)
            t2 = perf_counter()
            runtime = t2-t1
            instance.solutions[heuristic.name] = dict(m=len(solution), rt=runtime, sol=solution)

        solutions[instance.name] = instance.solutions

        print(f"Applying GRASP-5 meta heuristic to {instance.name}")
        t3 = perf_counter()
        solution = run_grasp(instance)
        t4 = perf_counter()
        runtime = t4-t3
        instance.solutions['GRASP-5'] = dict(m=len(solution), rt=runtime, sol=solution)

        print(f"Applying GRASP-10 meta heuristic to {instance.name}")
        t5 = perf_counter()
        solution = run_grasp(instance, num_iter=10)
        t6 = perf_counter()
        runtime = t6-t5
        instance.solutions['GRASP-10'] = dict(m=len(solution), rt=runtime, sol=solution)

        print(f"Postprocessing {instance.name}")
        best_solution = instance.postprocess()
        best_solutions[instance.name] = best_solution

        print("Gesamtdauer:", perf_counter() - t0)
        print("-" * 25, "\n")

    print("Writing all results to results.xlsx")
    # create a workbook and a worksheet
    workbook = xlsxwriter.Workbook('results/all_results.xlsx')
    worksheet = workbook.add_worksheet()

    # write headers in bold
    bold = workbook.add_format({'bold': 1})
    worksheet.write('A1', 'Instanz', bold)
    worksheet.write('B1', 'Prozedur', bold)
    worksheet.write('C1', 'Stationszahl', bold)
    worksheet.write('D1', 'BS', bold)
    worksheet.write('E1', 'ARD', bold)
    worksheet.write('F1', 'Laufzeit', bold)

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
    print("Computations successful")


if __name__ == "__main__":
    main()
