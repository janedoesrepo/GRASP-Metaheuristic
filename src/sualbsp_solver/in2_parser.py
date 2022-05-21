import sys
from pathlib import Path

from sualbsp_solver.data_model.graph import Graph
from sualbsp_solver.data_model.task import Task


class ParseError(ValueError):
    """Error while parsing a file."""

    pass


def parse_graph(filepath: Path) -> Graph:
    """Parses a file in the IN2-format into a Graph object.

    IN2-format:
        line 1:                     n: number of tasks
        line 2:                     p: number of direct precedence relations
        line 3:                     c: cycle time
        lines 4 to 4+n-1:           cl, t: task id (starts with 0), processing time
        lines 4+n to 4+n+p-1:       relations: direct precedence relations in form i,j
        lines 4+n+p to 4+2n+p-1:    tsu: setup times
    """
    try:
        with open(filepath) as f:

            # Read meta information
            num_tasks = int(f.readline())
            num_relations = int(f.readline())
            cycle_time = int(f.readline())

            # Create Tasks with id and processing times
            tasks: list[Task] = []
            for _ in range(num_tasks):
                task_id, processing_time = f.readline().split(",")
                tasks.append(Task(int(task_id), int(processing_time)))

            # Add the ids of the predecessor to each Task
            for _ in range(num_relations):
                predecessor_id, successor_id = f.readline().split(",")
                tasks[int(successor_id)].predecessors.append(int(predecessor_id))

            # Add the setup times from one Task to all other Tasks
            for i in range(num_tasks):
                setup_times_i = f.readline().split(",")
                tasks[i].setup_times = list(map(int, setup_times_i))

            name = filepath.name

        print(f">>> Import of {name} successful!")
        return Graph(tasks, cycle_time, name)

    except FileNotFoundError as e:
        raise e
    except ValueError:
        tb = sys.exc_info()[2]
        raise ParseError(
            f"Error while parsing file {filepath}. Is the data in a valid IN2-format?"
        ).with_traceback(tb)
    except Exception as ex:
        raise ex
