import pandas as pd


def create_instances(quantity=10) -> list:
    graphs = ["ARC83.IN2", "BARTHOLD.IN2", "HESKIA.IN2", "LUTZ2.IN2",
              "MITCHELL.IN2", "ROSZIEG.IN2", "SAWYER30.IN2", "WEE-MAG.IN2"]
    variants = ["TS0.25", "TS0.25-med", "TS0.75", "TS0.75-med"]
    instances = [Instance(graph, variant, ident) for graph in graphs for variant in variants for ident in
                 range(1, quantity)]
    return instances


class Instance:

    def __init__(self, graph, variant, ident):
        self.name = f"{graph}_{variant}_EJ{ident}"
        self.graph = graph
        self.variant = variant
        self.filename = f"{self.name}.txt"

        self.num_tasks = None
        self.num_relations = None
        self.cycle_time = None

        self.task_ids = None

        self.processing_times = None
        self.relations = None
        self.setups = None

        self.solutions = dict()

    def load(self):
        """ Import-function for the data set of Martino and Pastor (2010)
                The data is available at https://www.assembly-line-balancing.de/sualbsp

                line 1:                     n; number of tasks
                line 2:                     p; number of direct precedence relations
                line 3:                     c; cycle time
                lines 4 to 4+n-1:           cl, t; id task, processing time
                lines 4+n to 4+n+p-1:       relations; direct precedence relations in form i,j
                lines 4+n+p to 4+2n+p-1:    tsu; setup times
            """

        with open("data/" + self.filename, "r") as file:

            # read first three lines
            self.num_tasks = int(file.readline())
            self.num_relations = int(file.readline())
            self.cycle_time = int(file.readline())

            # create task ids
            self.task_ids = list(range(self.num_tasks))

            # read processing times
            self.processing_times = []
            for _ in range(self.num_tasks):
                _, time = file.readline().split(',')
                self.processing_times.append(int(time))

            # read precedence relations
            self.relations = [[] for _ in range(self.num_tasks)]
            for _ in range(self.num_relations):
                a, b = file.readline().split(',')
                self.relations[int(b)].append(int(a))

            # read setup times
            self.setups = []
            for _ in range(self.num_tasks):
                line = file.readline().split(',')
                line = [int(element) for element in line]
                self.setups.append(line)

            print(f"*Import of {self.name} successful!*")

    def postprocess(self):
        # find best solution BS
        best_solution = min([solution['m'] for _, solution in self.solutions.items()])

        # compute Average Relative Deviation for each solution
        for _, solution in self.solutions.items():
            ARD = 100 * ((solution['m'] - best_solution) / best_solution)
            solution['ARD'] = ARD

        print(f"Writing results_new to {self.name}.csv")
        data = [
            [self.name, heuristic_name, solution["m"], best_solution, solution["ARD"], solution["rt"]]
            for heuristic_name, solution in self.solutions.items()]
        df = pd.DataFrame(data, columns=["Instance", "Heuristic", "Number of Stations", "Best Solution", "ARD", "Runtime"])
        df.to_csv(f"results/{self.graph}/{self.name}.csv", sep=';', index=False)
        return best_solution
