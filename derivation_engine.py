import pathlib
import statistics

from uvengine import UVEngine

from utils.timer import Timer

from flamapy.metamodels.configuration_metamodel.models import Configuration
from flamapy.metamodels.configuration_metamodel.transformations import UVLSJSONReader
from flamapy.metamodels.fm_metamodel.transformations import UVLReader, FlatFM
from flamapy.metamodels.z3_metamodel.transformations import FmToZ3
from flamapy.metamodels.z3_metamodel.operations import Z3SatisfiableConfiguration


# jMetal example
template_dir = 'resources/jmetal/templates'
template_file = 'NSGAIIVar.java.jinja'
template_filepath = 'resources/jmetal/templates/NSGAIIVar.java.jinja'
fm_filepath = 'resources/jmetal/fm_models/jMetal.uvl'
config_filepath = 'resources/jmetal/configurations/NSGAIIDefaultConfiguration_Kursawe_scenario3.uvl.json'
#mapping_filepath = 'resources/jmetal/mapping_models/jMetal_mapping.csv'
mapping_filepath = None


def _check_satisfiable_configuration(z3_model, config_file, runs: int = 30) -> list[float]:
    configuration = UVLSJSONReader(config_file).transform()
    configuration.set_full(False)
    satisfiable_configuration_op = Z3SatisfiableConfiguration()
    satisfiable_configuration_op.set_configuration(configuration)
    
    sat_times_ms = []
    is_satisfiable = None

    # Benchmark loop for the specific execution line
    for _ in range(runs):
        with Timer(enabled=True, logger=None) as timer:
            is_satisfiable = satisfiable_configuration_op.execute(z3_model).get_result()
        
        sat_times_ms.append(timer.elapsed_time * 1000)

    print(f'Configuration: {configuration}')
    print(f'Is the configuration satisfiable? {is_satisfiable}')
    return sat_times_ms


def print_statistics(title: str, times_ms: list[float]) -> None:
    """Helper function to print benchmark statistics."""
    mean_time = statistics.mean(times_ms)
    stdev_time = statistics.stdev(times_ms) if len(times_ms) > 1 else 0.0
    min_time = min(times_ms)
    max_time = max(times_ms)

    print(f"\n--- {title} (30 runs) ---")
    print(f"Mean (Average): {mean_time:.6f} ms")
    print(f"Stdev (Standard Deviation): {stdev_time:.6f} ms")
    print(f"Min: {min_time:.6f} ms")
    print(f"Max: {max_time:.6f} ms")
    print("-" * (len(title) + 18) + "\n")


def main() -> None:
    uvengine = UVEngine(feature_model_path=fm_filepath,
                        configs_path=[config_filepath],
                        templates_paths=[template_filepath],
                        mapping_model_filepath=mapping_filepath)
    # Configure the name of the resulting class
    config_path = pathlib.Path(config_filepath)
    base_path = pathlib.Path('jmetal-var/src/main/java')
    name = config_path.name.removesuffix(''.join(config_path.suffixes))
    output_file = base_path / f'{name}.java'
    uvengine.configuration.elements['Filename'] = name

    # 1. Benchmark: Variability Resolution
    resolved_times_ms = []
    runs = 30

    for _ in range(runs):
        with Timer(enabled=True, logger=None) as timer:
            resolved_templates = uvengine.resolve_variability()
        resolved_times_ms.append(timer.elapsed_time * 1000)

    # Save the resolved templates to file (using the last execution data)
    for template_path, content in resolved_templates.items():
        outputfile = save_template(output_file, content)
        print(content)
        print(f'Resolved template saved to: {outputfile}')
    
    # 2. Setup FM and Z3 Models
    fm_model = UVLReader(fm_filepath).transform()
    flatFM_op = FlatFM(fm_model)
    flatFM_op.set_maintain_namespaces(False)
    fm_model = flatFM_op.transform()

    z3_model = FmToZ3(fm_model).transform()
    
    # 3. Benchmark: Satisfiable Configuration Check
    sat_times_ms = _check_satisfiable_configuration(z3_model, config_filepath, runs=runs)

    # 4. Print results side by side
    print_statistics("Variability Resolution Statistics", resolved_times_ms)
    print_statistics("Z3 Satisfiable Config Statistics", sat_times_ms)


def save_template(template_path: str, content: str) -> str:
    """Save the resolved template content to a file."""
    template_path = pathlib.Path(template_path)
    base_path = template_path.parent
    name = template_path.name.removesuffix(''.join(template_path.suffixes))
    suffixes = ''.join(template_path.suffixes).replace('.jinja', '')
    output_file = base_path / f'{name}{suffixes}'
    with open(output_file, 'w', encoding='utf-8') as file:
        file.write(content)
    return str(output_file)


if __name__ == '__main__':
    main()