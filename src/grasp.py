# load system packages
from copy import deepcopy

# load own packages
from construction import constructSolution
from improvement_neu import improveSolution


def grasp(cl, relations, t, tsu, c, iterations, greedyfactor):

    # initialise solution sets
    constructed_solutions = []
    improved_solutions = []

    alpha = greedyfactor    # Greedy-Factor
    num_iter = iterations   # Number of GRASP-Iterations

    """ Start Greedy Randomized Search Procedure (GRASP) """

    for i in range(1, num_iter+1):
        # Construct a solution and save it to the list of all constructed solutions
        constructed_solution = constructSolution(cl[:], deepcopy(relations), t, tsu, alpha, c)
        constructed_solutions.append(constructed_solution)

        # Improve the constructed solution and save it to the list of all improved solutions
        improved_solution = improveSolution(constructed_solution, relations, t, tsu, c)
        improved_solutions.append(improved_solution)

        if i == 1:
            best_solution = improved_solution
        elif len(improved_solution) < len(best_solution):
            best_solution = improved_solution

    return constructed_solutions, improved_solutions, best_solution
