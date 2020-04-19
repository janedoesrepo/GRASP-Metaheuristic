from time import perf_counter
import xlsxwriter
import pandas as pd

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

        # Run GRASP-5
        print(f"Applying GRASP-5 meta heuristic to {instance.name}")
        t3 = perf_counter()
        solution = run_grasp(instance)
        t4 = perf_counter()
        runtime = t4-t3
        instance.solutions['GRASP-5'] = dict(m=len(solution), rt=runtime, sol=solution)
    #
    #     # Run GRASP-10
    #     print("Applying GRASP-10 meta heuristic to " + instance)
    #     num_iter = 10
    #     t5 = perf_counter()
    #     _, _, solution = grasp(task_ids, relations, processing_times, setups, cycle_time, num_iter, alpha)
    #     t6 = perf_counter()
    #     runtime = t6-t5
    #     instance_solutions['GRASP-10'] = dict(m=len(solution), rt=runtime, sol=solution)
    #
        """ Postprocessing """
        t7 = perf_counter()
        runtime = t7 - t0

        # find best solution BS for each instance
        best_solution = min([solution['m'] for _, solution in instance.solutions.items()])
        best_solutions[instance.name] = best_solution

        # compute Average Relative Deviation for each solution
        for _, solution in instance.solutions.items():
            ARD = 100 * ((solution['m'] - best_solution) / best_solution)
            solution['ARD'] = ARD

        print(f"Writing results_new to {instance.name}_pd.xlsx")
        data = [
            [instance.name, heuristic_name, solution["m"], best_solutions[instance.name], solution["ARD"], solution["rt"]]
            for heuristic_name, solution in instance.solutions.items()]
        df = pd.DataFrame(data, columns=["Instanz", "Heuristik", "Stationszahl", "Beste Lösung", "ARD", "Runtime"])
        df.to_excel(f"results_new/{instance.name}_pd.xlsx", index=False)

        print("Gesamtdauer:", runtime)
        print("-" * 25, "\n")

    # TODO Write data via pandas
    """ Write all solutions to a single xlsx-file """
    print("Writing results_new to results.xlsx")

    # create a workbook and a worksheet
    workbook = xlsxwriter.Workbook('results_new/' + 'results.xlsx')
    worksheet = workbook.add_worksheet()

    # write headers in bold
    bold = workbook.add_format({'bold': 1})
    worksheet.write('A1', 'Instanz', bold)
    worksheet.write('B1', 'Prozedur', bold)
    worksheet.write('C1', 'Stationszahl', bold)
    worksheet.write('D1', 'BS', bold)
    worksheet.write('E1', 'ARD', bold)
    worksheet.write('F1', 'Laufzeit', bold)

    # write data
    # data = [
    #     [instance.name, heuristic_name, solution["m"], best_solutions[instance.name], solution["ARD"], solution["rt"]]
    #     for heuristic_name, solution in instance.solutions.items()]
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

    # close workbook
    workbook.close()

    print("Computations successful")


if __name__ == "__main__":
    # import timeit
    # setup = "from datahandler.test import create_instances"
    # print(timeit.timeit("create_instances()", setup=setup, number=100000))

    main()
