from genie.harness.main import gRun
import yaml
import argparse


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--config_file',
                        dest='features_datafile',
                        default='pts_features.yaml')
    parser.add_argument('--after',
                        dest='after',
                        action='store_true')
    parser.set_defaults(after=False)

    args, unknown = parser.parse_known_args()
    # common definition of features to profile
    with open(args.features_datafile, 'r') as f:
        features = yaml.safe_load(f)
        features = features['features']

    if args.after:

        gRun(mapping_datafile='mapping_datafile.yaml',
             pts_datafile='pts_datafile.yaml',
             pts_features=features,
             subsection_datafile='subsection_datafile.yaml',
             pts_golden_config='pts')
    else:

        gRun(mapping_datafile='mapping_datafile.yaml',
             pts_datafile='pts_datafile.yaml',
             pts_features=features,
             subsection_datafile='subsection_datafile.yaml')
