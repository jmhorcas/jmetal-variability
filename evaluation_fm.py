from flamapy.metamodels.fm_metamodel.transformations import UVLReader, FlatFM
from flamapy.metamodels.fm_metamodel.operations import FMVariationPoints
from flamapy.metamodels.z3_metamodel.transformations import FmToZ3
from flamapy.metamodels.z3_metamodel.operations import Z3FeatureBounds

def main():
    fm = UVLReader('resources/jmetal/fm_models/jMetal.uvl').transform()
    flat_fm_op = FlatFM(fm)
    flat_fm_op.set_maintain_namespaces(False)
    flat_fm = flat_fm_op.transform()
    
    fm_variation_points = FMVariationPoints().execute(flat_fm).get_result()
    print(f'Variation Points: {len(fm_variation_points)}')
    print(f'Variants per Variation Point: {[len(v) for v in fm_variation_points.values()]}')
    print(f'Variants: {sum(len(v) for v in fm_variation_points.values())}')

    z3_model = FmToZ3(flat_fm).transform()
    
    numerical_features = flat_fm.get_numerical_features()
    print(f'Numerical Features: {len(numerical_features)}')
    for numerical_feature in numerical_features:
        print(f'Numerical Feature: {numerical_feature.name}')
        for ctc in flat_fm.get_constraints():
            if numerical_feature.name in ctc.get_features():
                print(f'--|{ctc.ast.pretty_str()}')
    string_features = flat_fm.get_string_features()
    print(f'String Features: {len(string_features)}')
    for string_feature in string_features:
        print(f'String Feature: {string_feature.name}')
        for ctc in flat_fm.get_constraints():
            if string_feature.name in ctc.get_features():
                print(f'--|{ctc.ast.pretty_str()}')

if __name__ == "__main__":
    main()
