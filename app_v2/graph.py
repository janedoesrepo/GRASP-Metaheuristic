import pandas as pd
import pathlib
from dataclasses import dataclass, field
from typing import List


def compute_ARD(solution, best_solution) -> float:
    """Compute the average relative deviation of a solution"""
    ARD = 100 * ((solution['m'] - best_solution) / best_solution)
    return ARD
    

@dataclass()
class Task:
    """Implement this at the end. There are other low hanging fruits"""
    id: int
    processing_time: int
    predecessors: List[int] = field(default_factory=list, init=False)
    setup_times: List[int] = field(default_factory=list, init=False)


class GraphInstance:

    def __init__(self, graph, variant, ident):

        self.graph = graph
        self.variant = variant
        self.ident = ident
        
        self.filename = f"{self}.txt"

        self.tasks: List[Task] = []
        
        """TODO: Move this outside of here"""
        self.solutions = {}
        
    def __str__(self):
        return f"{self.graph}_{self.variant}_EJ{self.ident}"

    def parse_instance(self):
        """ Import-function for the data set of Martino and Pastor (2010)
            The data is available at https://www.assembly-line-balancing.de/sualbsp

            line 1:                     n; number of tasks
            line 2:                     p; number of direct precedence relations
            line 3:                     c; cycle time
            lines 4 to 4+n-1:           cl, t; id task, processing time
            lines 4+n to 4+n+p-1:       relations; direct precedence relations in form i,j
            lines 4+n+p to 4+2n+p-1:    tsu; setup times
        """

        with open("data/Instances/" + self.filename, "r") as file:

            # read first three lines
            num_tasks = int(file.readline())
            num_relations = int(file.readline())
            self.cycle_time = int(file.readline())                
            
            # create task ids
            self.task_ids = list(range(num_tasks))
            
            # # Create tasks with id and processing times
            # for _ in range(num_tasks):
            #     task_id, time = file.readline().split(',')
            #     self.tasks.append(Task(task_id, time))
                
            # read processing times
            self.processing_times = []
            for _ in range(num_tasks):
                _, time = file.readline().split(',')
                self.processing_times.append(int(time))
                
            # # Add predecessor ids to each task        
            # for _ in range(num_relations):
            #     predecessor, task_id = file.readline().split(',')
            #     self.tasks[int(task_id)].predecessors.append(predecessor)
                
            # read precedence relations
            self.relations = [[] for _ in range(num_tasks)]
            for _ in range(num_relations):
                a, b = file.readline().split(',')
                self.relations[int(b)].append(int(a))
            
            # # Setup times is a matrice of dim num_tasks x num_tasks
            # for i in range(num_tasks):
            #     setup_times_i = file.readline().split(',')
            #     self.tasks[i].setup_times = list(map(int, setup_times_i))
                
            # read setup times
            self.setups = []
            for _ in range(num_tasks):
                line = file.readline().split(',')
                line = list(map(int, line))
                self.setups.append(line)  
                
            print(f"*Import of {self} successful!*")

    
    def postprocess(self):
        # find best solution BS
        best_solution = min([solution['m'] for _, solution in self.solutions.items()])

        # compute Average Relative Deviation for each solution
        for _, solution in self.solutions.items():
            solution['ARD'] = compute_ARD(solution, best_solution)

        print(f"Writing results to {self}.csv")

        # Set result dir and create it, if it does not exist
        result_dir = pathlib.Path(f"app_v2/results/{self.graph}/")
        result_dir.mkdir(exist_ok=True)

        # Write result to file
        data = [
            [self, heuristic_name, solution["m"], best_solution, solution["ARD"], solution["rt"]]
            for heuristic_name, solution in self.solutions.items()]
        df = pd.DataFrame(data, columns=["Instance", "Heuristic", "Number of Stations", "Best Solution", "ARD", "Runtime"])
        df.to_csv(result_dir/f"{self}.csv", sep=';', index=False)
        return best_solution
