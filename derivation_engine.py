import pathlib

from uvengine import UVEngine


# jMetal example
template_dir = 'resources/jmetal/templates'
template_file = 'NSGAIIVar.java.jinja'
template_filepath = 'resources/jmetal/templates/NSGAIIVar.java.jinja'
fm_filepath = 'resources/jmetal/fm_models/jMetal.uvl'
config_filepath = 'resources/jmetal/configurations/NSGAIIDefaultConfiguration.uvl.json'
#mapping_filepath = 'resources/jmetal/mapping_models/jMetal_mapping.csv'
mapping_filepath = None


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
    resolved_templates = uvengine.resolve_variability()
    # Save the resolved templates to file
    for template_path, content in resolved_templates.items():
        outputfile = save_template(output_file, content)
        print(content)
        print(f'Resolved template saved to: {outputfile}')


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
    # parser = argparse.ArgumentParser(description='UVengine: Variability resolution engine for UVL with Jinja templates.')
    # parser.add_argument('-fm', '--feature_model', dest='feature_model', type=str, required=False, 
    #                     help='Feature model in UVL (.uvl).')
    # parser.add_argument('-c', '--configs', dest='configs_dir', type=str, required=True, 
    #                     help='Directory with the configurations files (.json).')
    # parser.add_argument('-t', '--templates', dest='templates_dir', type=str, required=True, 
    #                     help='Template directory with templates files (.jinja) over which the variability is resolved.')
    # parser.add_argument('-m', '--mapping', dest='mapping_file', type=str, required=False, 
    #                     help='File with the mapping between the variation points and the templates (.csv).')
    # args = parser.parse_args()

    # # Get parameters
    # feature_model = args.feature_model
    # configurations_files = utils.get_filepaths(args.configs_dir, ['.json'])
    # templates_dir = utils.get_filepaths(args.templates_dir, ['.jinja'])
    # mapping_file = args.mapping_file

    main()    

