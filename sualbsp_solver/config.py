import json
from dataclasses import dataclass

@dataclass
class GraphConfig:
    data_dir: str
    graphs_file: str
    variants_file: str
    num_instances: int
    all_results_file: str
    
def read_config(config_file: str) -> GraphConfig:
    with open(config_file, 'r') as file:
        data = json.load(file)
        return GraphConfig(**data)
