import argparse
import json
import sys
import traceback
from invite import Invite


def execute(config_path):
    # loading config from json
    config = json.load(open(config_path))
    invite = Invite(
        config['distance_threshold'],
        config['intercom_latitude'],
        config['intercom_longitude'],
        config['output_file_path'],
        input_file_url=config['input_file_url'] if 'input_file_url' in config else None,
        input_file_path=config['input_file_path'] if 'input_file_path' in config else None
    )
    return invite.invite_customers()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Run System with config')
    parser.add_argument('config_path', help='Config json path')
    args = parser.parse_args()

    try:
        execute(args.config_path)
    except KeyError as ve:
        print("Invalid config")
        traceback.print_exc(file=sys.stdout)
    except Exception as e:
        print("Some error occurred")
        traceback.print_exc(file=sys.stdout)
